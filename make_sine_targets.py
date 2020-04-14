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
def _sine_star(n,r0,r1,offsets, img, mask):
    s = 2*int(np.ceil(r1))
    #iterate over offsets
    for i in range(offsets.shape[0]):
        ox,oy = offsets[i]
        #iterate over pixels
        for j in range(s):
            py = j - s/2
            for k in range(s):
                px = k - s/2
                r = np.hypot(px+ox, py+oy)
                if r <= r1 and r >= r0:
                    a = np.arctan2(py+oy, px+ox)
                    img[j,k] += (1+np.cos(n*a))/2
                    mask[j,k] += 1
    for i in range(s):
        for j in range(s):
            m = mask[i,j]
            if m != 0:
                img[i,j] /= m
            mask[i,j] = m/len(offsets)

def sine_star(n, r0, r1, nss):
    """Make a sine star
    parameters
      n: number of cycles
      r0, r1: inner and outer radii, in pixels. May be fractional
      nss: sub-sampling grid size
    returns
        (img, mask)
            each is 2D ndarray with pattern
            shape (2*ceil(r1), 2*ceil(r1))
    """
    offsets = subsample_offsets(nss,jitter=None).reshape((-1,2))
    s = 2*int(np.ceil(r1))
    img = np.zeros((s,s))
    mask = np.zeros_like(img)
    
    _sine_star(n,r0,r1,offsets, img, mask)
    return img, mask

def to_byte(x):
    #evenly divides the range from 0 to 1 into 256 bins
    return np.floor(np.nextafter(256,0)*x).astype(np.uint8)

def mm_to_inches(x):
    """1 inch = 25.4 mm"""
    return x/25.4

if __name__ == '__main__':
    #subsample grid size
    nss = 10
    
    #how many pixels per cycle do we want, minimum?
    ppc = 20
    
    cycles = [36, 72, 144]
    for c in cycles:
        r0 = c*ppc/(2*np.pi)
        r1 = 3*r0
        print(f'Generate {c}-cycle sine star... ',end='',flush=True)
        img, mask = sine_star(c, r0, r1, nss)
        img, mask = to_byte(img), to_byte(mask)
        #rgba = np.stack((img, img, img, mask),-1)
        Image.fromarray(img,'L').save(f'radial-sine-{c}.png')
        print('DONE')
