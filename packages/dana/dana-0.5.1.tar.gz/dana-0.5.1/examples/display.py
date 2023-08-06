#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright INRIA
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#
# DANA is a computing framework for the simulation of distributed,
# asynchronous, numerical and adaptive models.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info/index.en.html.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# -----------------------------------------------------------------------------
'''
This is a set of plot functions dedicated to DANA. They allow to show
connections when user click on a unit and to display unit activity when mouse is
over a unit.
'''
from dana import *
from functools import partial
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def format_coord(axis, x, y):
    ''' Display coordinates and values of data '''
    Z = axis.get_array()
    if x is None or y is None or Z is None:
        return ''
    x,y = int(x), int(y)
    if 0 <= x < Z.shape[1] and 0 <= y < Z.shape[0]:
        return '[%d,%d]: %s' % (x,y, Z[y,x])
    return ''

def update(G=None, x=-1, y=-1):
    ''' '''
    mgr = plt.get_current_fig_manager()
    if G is None:
        for axis,group,data,cb,subplot in mgr.subplots:
            if hasattr(group, 'mask'):
                D = np.where(group.mask,data,np.NaN)
            else:
                D = data
            axis.set_data(D)
            vmin, vmax= cb.original_clim
            axis.vmin, axis.vmax = vmin, vmax
            axis.cmap = cb.original_cmap
            cb.set_clim(vmin, vmax)
            cb.set_cmap(axis.cmap)
            cb.set_ticks([vmin, vmax])
            cb.update_normal(axis)
            for label in cb.ax.get_xticklabels():
                label.set_fontsize('x-small')
    else:
        for axis,group,data,cb,subplot in mgr.subplots:
            axis.set_data(np.empty_like(data)*np.NaN)
            axis.cmap = plt.cm.bone
            axis.vmin, axis.vmax = 0,1
            cb.set_clim(0, 1)
            cb.set_cmap(plt.cm.bone)
            cb.set_ticks([0, 1])
            cb.update_normal(axis)
            for label in cb.ax.get_xticklabels():
                label.set_fontsize('x-small')
        if hasattr(G, '_connections'):
            for C in G._connections:
                for axis,group,data,cb,subplot in mgr.subplots:
                    if C._actual_source is data:
                        try:
                            V = C[y,x]
                            v = max(abs(V[~np.isnan(V)].min()),
                                    abs(V[~np.isnan(V)].max()))
                            axis.set_data(V)
                            vmin, vmax= -v, v
                            axis.vmin, axis.vmax = vmin, vmax
                            axis.cmap = plt.cm.PuOr_r
                            cb.set_clim(vmin, vmax)
                            cb.set_cmap(plt.cm.PuOr_r)
                            cb.set_ticks([vmin, vmax])
                            cb.update_normal(axis)
                            for label in cb.ax.get_xticklabels():
                                label.set_fontsize('x-small')
                        except NotImplementedError:
                            pass

def button_press_event(event):
    G,x,y = None, -1, -1
    if event.inaxes and event.button == 1:
        G = event.inaxes.group
        x,y = int(event.xdata), int(event.ydata)
    update(G, x, y)
    plt.draw()


def plot(subplot, data, title='', *args, **kwargs):
     mgr = plt.get_current_fig_manager()
     a,b = 0.75, 1.0
     chessboard = np.array(([a,b]*16 + [b,a]*16)*16)
     chessboard.shape = 32,32
     if isinstance(data, Group):
         group = data #.base
         data = data[data.keys[0]]
     else:
         group = data
         data = data
     plt.imshow(chessboard, cmap=plt.cm.gray, interpolation='nearest',
                extent=[0,group.shape[1],0,group.shape[0]],
                vmin=0, vmax=1)
     plt.hold(True)
     if hasattr(group, 'mask'):
         D = np.where(group.mask,data,np.NaN)
     else:
         D = data
     axis = plt.imshow(D, interpolation='nearest',
                       #cmap=plt.cm.bone,
                       #cmap= plt.cm.PuOr_r,
                       #vmin=-1, vmax=1,
                       origin='lower',
                       extent=[0,group.shape[1],0,group.shape[0]],
                       *args, **kwargs)

     subplot.format_coord = partial(format_coord, axis)
     subplot.group = group
     plt.xticks([]), plt.yticks([])
     x,y,w,h = axis.get_axes().bbox.bounds
     dw = 0*float(group.shape[1]-1)/w
     dh = 0*float(group.shape[0]-1)/h
     plt.axis([-dw,group.shape[1]+dw,-dh,group.shape[0]+dh])

     if title:
         t = plt.title(title, position=(0,1.01),
                       verticalalignment = 'baseline',
                       horizontalalignment = 'left')

     axins = inset_axes(subplot, width="35%", height="2.5%", loc=2,
                        bbox_to_anchor=(0.65, 0.05, 1, 1),
                        bbox_transform=subplot.transAxes, borderpad = 0)
     cb = plt.colorbar(axis, cax=axins, orientation="horizontal", format='%.2f', ticks=[])
     vmin,vmax = cb.get_clim()
     cb.set_ticks([vmin,vmax])
     cb.original_cmap = cb.get_cmap()
     cb.original_clim = vmin,vmax
     axins.xaxis.set_ticks_position('top')
     for label in cb.ax.get_xticklabels():
         label.set_fontsize('x-small')
     if not hasattr(mgr, 'subplots'):
         mgr.subplots = []
     mgr.subplots.append((axis,group,data,cb,subplot))



if __name__ == '__main__':
    Z = np.random.random((40,40))
    fig = plt.figure(figsize=(8,8), facecolor='white')
    plot(plt.subplot(1,1,1), Z, 'A group', cmap=ice_and_fire)
    plt.connect('button_press_event', button_press_event)
    plt.show()
