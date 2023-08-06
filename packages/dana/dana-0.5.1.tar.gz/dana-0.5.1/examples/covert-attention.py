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
This is a demonstration of covert attention using dynamic neural fields. The
goal for the model is to focus successively on each ot the three stimuli. As
soon as a stimulus if focused, it entered the working memory where a virtual
"link" is made with the visual input. The focus may be considered as a gate
allowing the working memory to make a specific bind ith the visual input.

A switch is made by setting the switch group to a very high value that
disinhibit the striatum group which in turn inhibit the focus group. Since the
working memory is also continuously inhibiting the focus group, the focus can
only be made on never focused stimuli.

If you run the demo (python covert-attention), you will see three switched and
then you'll be allowed to click on any group to see different connections
between groups.
'''
from dana import *

# Simulation parameters
# ---------------------
n = 40
dt = 0.5
r = 0.7
theta = np.array([0.0 , 2.0 * np.pi/3.0 , - 2.0 * np.pi/3.0])
dtheta = np.pi/300.0

# Build groups
# ------------
visual = np.zeros((n,n))
focus = zeros((n,n), '''dV/dt = -V+(L+Iv+Is)/30 -0.05 : float
                        U = np.maximum(V,0) : float
                        L : float; Iv: float; Is: float''')
wm  = zeros((n,n), '''dV/dt = -V+(L+Iv+If)/31 - 0.2 : float
                      U = np.minimum(np.maximum(V,0),1) : float
                      L : float; Iv: float; If: float''')
striatum = zeros((n,n), '''dV/dt = -V+(L+Iw+Ir)/28 - 0.3 : float
                           U = np.maximum(V,0) : float
                           L : float; Iw: float; Ir: float''')
switch = zeros((1,1), '''dV/dt = -0.1*V : float
                         U = np.maximum(V,0) : float''')

# Connections
# -----------
s = (2*n+1,2*n+1)
SharedConnection(visual,        focus('Iv'),    +0.25*gaussian(s, 0.05))
SharedConnection(striatum('U'), focus('Is'),    -0.20*gaussian(s, 0.10))
SharedConnection(focus('U'),    focus('L'),     +1.70*gaussian(s, 0.10)
                                                -0.65*gaussian(s, 1.00))
SharedConnection(visual,        wm('Iv'),       +0.35*gaussian(s, 0.05))
SharedConnection(focus('U'),    wm('If'),       +0.20*gaussian(s, 0.05))
SharedConnection(wm('U'),       wm('L'),        +3.00*gaussian(s, 0.05)
                                                -0.50*gaussian(s, 0.10))
SharedConnection(wm('U'),       striatum('Iw'), +0.50*gaussian(s, 0.0625))
DenseConnection(switch('U'),    striatum('Ir'), +20.00)
SharedConnection(striatum('U'), striatum('L'),  +2.50*gaussian(s, 0.05)
                                                -1.00*gaussian(s, 0.10))

def rotate():
    global theta, visual
    theta += dtheta
    visual[...] = 0
    for i in range(theta.size):
        x, y = r*np.cos(theta[i]), r*np.sin(theta[i])
        visual += gaussian((n,n), 0.2, (x,y))
    visual += (2*rnd.random((n,n))-1)*.05

def iterate(t=100):
    mgr = plt.get_current_fig_manager()
    for i in range(t):
        rotate()
        run(time=.5,dt=.5)
        update()
        plt.draw()

def demo(t=1000):
    iterate(100)
    for i in range(2):
        switch['V'] = 1.0
        print "Switch now"
        iterate(100)

if __name__ == '__main__':
    from display import *

    plt.ion()
    fig = plt.figure(figsize=(8,10), facecolor='white')
    plot(plt.subplot(2,2,1), visual, 'Visual')
    plot(plt.subplot(2,2,2), focus('U'), 'Focus')
    plot(plt.subplot(2,2,3), wm('U'), 'Working memory')
    plot(plt.subplot(2,2,4), striatum('U'), 'Striatum')
    plt.connect('button_press_event', button_press_event)
    plt.draw()
    demo()
    plt.show()
