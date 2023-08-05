import os
import subprocess
import numpy as np
from astropy.utils.console import ProgressBar
from astropy import log
from astropy.extern import six

try:
    import yt
    from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
    ytOK = True
except ImportError:
    ytOK = False

class ytCube(object):
    """ Light wrapper of a yt object with ability to translate yt<->wcs
    coordinates """

    def __init__(self, cube, dataset, spectral_factor=1.0):
        self.cube = cube
        self.wcs = cube.wcs
        self.dataset = dataset
        self.spectral_factor = spectral_factor


    def world2yt(self, world_coord, first_index=0):
        """
        Convert a position in world coordinates to the coordinates used by a
        yt dataset that has been generated using the ``to_yt`` method.

        Parameters
        ----------
        world_coord: `astropy.wcs.WCS.wcs_world2pix`-valid input
            The world coordinates
        first_index: 0 or 1
            The first index of the data.  In python and yt, this should be
            zero, but for the FITS coordinates, use 1
        """
        yt_coord = self.wcs.wcs_world2pix([world_coord], first_index)[0]
        yt_coord[2] = (yt_coord[2] - 0.5)*self.spectral_factor+0.5
        return yt_coord

    def yt2world(self, yt_coord, first_index=0):
        """
        Convert a position in yt's coordinates to world coordinates from a
        yt dataset that has been generated using the ``to_yt`` method.

        Parameters
        ----------
        world_coord: `astropy.wcs.WCS.wcs_pix2world`-valid input
            The yt pixel coordinates to convert back to world coordinates
        first_index: 0 or 1
            The first index of the data.  In python and yt, this should be
            zero, but for the FITS coordinates, use 1
        """
        yt_coord = np.array(yt_coord) # stripping off units
        yt_coord[2] = (yt_coord[2] - 0.5)/self.spectral_factor+0.5
        world_coord = self.wcs.wcs_pix2world([yt_coord], first_index)[0]
        return world_coord


    def quick_render_movie(self, outdir, size=256, nframes=30,
                           camera_angle=(0,0,1), north_vector=(0,0,1),
                           rot_vector=(1,0,0),
                           colormap='doom',
                           cmap_range='auto',
                           transfer_function='auto',
                           log=False,
                           rescale=True):
        """
        Create a movie rotating the cube 360 degrees from
        PP -> PV -> PP -> PV -> PP

        Parameters
        ----------
        outdir: str
            The output directory in which the individual image frames and the
            resulting output mp4 file should be stored
        size: int
            The size of the individual output frame in pixels (i.e., size=256
            will result in a 256x256 image)
        nframes: int
            The number of frames in the resulting movie
        camera_angle: 3-tuple
            The initial angle of the camera
        north_vector: 3-tuple
            The vector of 'north' in the data cube.  Default is coincident with
            the spectral axis
        rot_vector: 3-tuple
            The vector around which the camera will be rotated
        colormap: str
            A valid colormap.  See `yt.show_colormaps`
        transfer_function: 'auto' or `yt.visualization.volume_rendering.TransferFunction`
            Either 'auto' to use the colormap specified, or a valid
            TransferFunction instance
        log: bool
            Should the colormap be log scaled?
        rescale: bool
            If True, the images will be rescaled to have a common 95th
            percentile brightness, which can help reduce flickering from having
            a single bright pixel in some projections

        Returns
        -------


        """
        if not ytOK:
            raise IOError("yt could not be imported.  Cube renderings are not possible.")

        scale = np.max(self.cube.shape)

        if not os.path.exists(outdir):
            os.makedirs(outdir)
        elif not os.path.isdir(outdir):
            raise OSError("Output directory {0} exists and is not a directory.".format(outdir))

        if cmap_range == 'auto':
            upper = self.cube.max().value
            lower = self.cube.std().value * 3
            cmap_range = [lower,upper]

        if transfer_function == 'auto':
            tfh = self.auto_transfer_function(cmap_range, log=log)
            tfh.tf.map_to_colormap(cmap_range[0], cmap_range[1], colormap=colormap)
            tf = tfh.tf
        else:
            tf = transfer_function

        center = self.dataset.domain_center
        cam = self.dataset.h.camera(center, camera_angle, scale, size, tf,
                                    north_vector=north_vector, fields='flux')

        im  = cam.snapshot()
        images = [im]

        pb = ProgressBar(nframes)
        for ii,im in enumerate(cam.rotation(2 * np.pi, nframes,
                                            rot_vector=rot_vector)):
            images.append(im)
            im.write_png(os.path.join(outdir,"%04i.png" % (ii)), rescale=False)
            pb.update(ii)

        if rescale:
            _rescale_images(images, outdir)

        pipe = _make_movie(outdir)
        
        return images

    def auto_transfer_function(self, cmap_range, log=False, colormap='doom',
                               **kwargs):

        tfh = TransferFunctionHelper(self.dataset)
        tfh.set_field('flux')
        tfh.set_bounds(bounds=cmap_range)
        tfh.set_log(log)
        tfh.build_transfer_function()
        return tfh

    def quick_isocontour(self, level='3 sigma', title='', description='',
                         color_map='hot', color_log=False):
        """
        Export isocontours to sketchfab

        Requires that you have an account on https://sketchfab.com and are
        logged in

        Parameters
        ----------
        level: str or float
            The level of the isocontours to create.  Can be specified as
            n-sigma with strings like '3.3 sigma' or '2 sigma' (there must be a
            space between the number and the word)
        title: str
            A title for the uploaded figure
        description: str
            A short description for the uploaded figure
        color_map: str
            Any valid colormap.  See `yt.show_colormaps`
        color_log: bool
            Whether the colormap should be log scaled.  With the default
            parameters, this has no effect.

        Returns
        -------
        The result of the `yt.surface.export_sketchfab` function
        """
        if isinstance(level, six.string_types):
            sigma = self.cube.std().value
            level = float(level.split()[0]) * sigma

        self.dataset.periodicity = (True,True,True)
        surface = self.dataset.surface(self.dataset.all_data(),
                                       "flux",
                                       level)
        return surface.export_sketchfab(title=title, description=description,
                                        color_map=color_map,
                                        color_log=color_log)

def _rescale_images(images, prefix):
    """
    Save a sequence of images, at a common scaling
    Reduces flickering
    """
 
    cmax = max(np.percentile(i[:, :, :3].sum(axis=2), 99.5) for i in images)
    amax = max(np.percentile(i[:, :, 3], 95) for i in images)
 
    for i, image in enumerate(images):
        image = image.rescale(cmax=cmax, amax=amax).swapaxes(0,1)
        image.write_png(os.path.join(prefix, "%04i.png" % (i)), rescale=False)

def _make_movie(moviepath, overwrite=True):
    """
    Use ffmpeg to generate a movie from the image series
    """

    outpath = os.path.join(moviepath,'out.mp4')

    if os.path.exists(outpath) and overwrite:
        command = ['ffmpeg', '-y', '-r','5','-i',
                   os.path.join(moviepath,'%04d.png'),
                   '-r','30','-pix_fmt', 'yuv420p',
                   outpath]
    elif os.path.exists(outpath):
        log.info("File {0} exists - skipping".format(outpath))
    else:
        command = ['ffmpeg', '-r', '5', '-i',
                   os.path.join(moviepath,'%04d.png'),
                   '-r','30','-pix_fmt', 'yuv420p',
                   outpath]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)

    pipe.wait()

    return pipe
