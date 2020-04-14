# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:11:53 2020

generate linear and radial sine patterns

@author: sam
"""

import numpy as np
from numba import jit
from PIL import Image

def subsample_offsets(n, d=2, jitter=None):
    """return coordinates of bin centres, evenly spaced between 0 and 1
    n: number of bins
    d: dimensions
    jitter: if not None,
        adjust centers by multivariate normal distribution with unit covariance
        scaled by jitter/n
    """
    dx = 1/n
    x = np.linspace(0,1,n,endpoint=False) + 0.5*dx #centers
    x = np.stack(np.meshgrid(*([x]*d)), axis=-1) #replicate to d dimensions
    if jitter is not None and jitter != 0.0:
        x += jitter*dx*np.random.multivariate_normal([0.0]*d, np.eye(d),x.shape[:-1])
    return x

@jit
def _sine_star(n,x,y,offsets):
    img = 0
    for ox,oy in offsets:
        a = np.arctan2(y+oy,x+ox)
        img += np.cos(n*a)
    img /= len(offsets)
    return (1+img)/2

def sine_star(n, w, naa):
    """Make a sine star
    n: number of cylcles
    w: width, in pixels
    naa: anti-aliasing grid size
    """
    dx = 2/w
    x = np.linspace(-1,1,w,endpoint=False) #pixel corners
    x,y = np.meshgrid(x,x)
    offsets = dx*subsample_offsets(naa,jitter=None).reshape((-1,2))
    
    return _sine_star(n,x,y,offsets)

def to_byte(x):
    #evenly divides the range from 0 to 1 into 256 bins
    return np.floor(np.nextafter(256,0)*x).astype(np.uint8)

def mm_to_inches(x):
    """1 inch = 25.4 mm"""
    return x/25.4

if __name__ == '__main__':
    #calculate how big the image should be to match the printer's resolution
    dpi = 1200
    #set the width such that the circumference is about 600 mm
    width = int(np.ceil(dpi*mm_to_inches(600/np.pi)))
    naa = 10
    cycles = [36, 72, 144]
    for c in cycles:
        print(f'Generate {c}-cycle sine star at {dpi} dpi (width={width})... ',end='',flush=True)
        img = sine_star(c, width, naa)
        Image.fromarray(to_byte(img),'L').save(f'sine-target-{c}-{dpi}.png')
        print('DONE')
