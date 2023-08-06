# Copyright (C) 2013-2014 Science and Technology Facilities Council.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import healpy
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np

def plot_moc(moc, order=None, antialias=0, filename=None,
        projection='cart', color='blue', title='', coord_sys='C',
        graticule=True, **kwargs):
    """Plot a MOC using Healpy.
    """

    # Process arguments.
    plotargs = {'xsize': 3200, 'cbar': False, 'notext': True}

    if order is None:
        order = moc.order

    if projection.startswith('cart'):
        plotter = healpy.visufunc.cartview
    elif projection.startswith('moll'):
        plotter = healpy.visufunc.mollview
    elif projection.startswith('gnom'):
        plotter = healpy.visufunc.gnomview
    else:
        raise ValueError('Unknown projection: {0}'.format(projection))

    if color == 'blue':
        plotargs['cmap'] = LinearSegmentedColormap.from_list(
                            'white-blue', ['#FFFFFF', '#0000AA'])
    elif color == 'green':
        plotargs['cmap'] = LinearSegmentedColormap.from_list(
                            'white-green', ['#FFFFFF', '#008800'])
    elif color == 'red':
        plotargs['cmap'] = LinearSegmentedColormap.from_list(
                            'white-red', ['#FFFFFF', '#FF0000'])
    elif color == 'black':
        plotargs['cmap'] = LinearSegmentedColormap.from_list(
                            'white-black', ['#FFFFFF', '#000000'])
    else:
        raise ValueError('Unknown color: {0}'.format(color))

    if coord_sys == 'C':
        pass
    elif coord_sys == 'G':
        plotargs['coord'] = ('C', 'G')
    elif coord_sys == 'E':
        plotargs['coord'] = ('C', 'E')
    else:
        raise ValueError('Unknown coordinate system: {0}'.format(coord_sys))

    # Any other arguments are passed the Healpy plotter directly.
    plotargs.update(kwargs)

    # Create a Numpy array which is zero for points outside the MOC and one
    # for points inside the MOC.
    map = np.zeros(12 * 4 ** order)
    antialias_shift = 2 * antialias

    for cell in moc.flattened(order + antialias):
        map[cell >> antialias_shift] += 1.0

    # Plot the Numpy array using Healpy.
    plotter(map, nest=True, title=title, **plotargs)

    if graticule:
        healpy.visufunc.graticule()

    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()
