# -*- coding: utf-8 -*-

from __future__ import division, print_function

import numpy as np
from .helpers import *


class DefGrad(np.ndarray):
    """class to store deformation gradient tensor derived from numpy.ndarray
    """
    def __new__(cls, array):
        # casting to our class
        assert np.shape(array) == (3, 3), 'DefGrad must be 3x3 2D array'
        obj = np.asarray(array).view(cls)
        return obj

    def __repr__(self):
        return 'DefGrad:\n' + str(self)

    def __mul__(self, other):
        assert np.shape(other) == (3, 3), 'DefGrad could by multiplied with 3x3 2D array'
        return np.dot(self, other)

    def __pow__(self, n):
        # cross product or power of magnitude
        assert np.isscalar(n), 'Exponent must be integer.'
        return np.linalg.matrix_power(self, n)

    def __eq__(self, other):
        # equal
        return bool(np.sum(abs(self-other)) < 1e-14)

    def __ne__(self, other):
        # not equal
        return not self == other

    @classmethod
    def from_axis(cls, vector, theta):
        x, y, z = vector.uv
        c, s = cosd(theta), sind(theta)
        xs, ys, zs = x*s, y*s, z*s
        xc, yc, zc = x*(1-c), y*(1-c), z*(1-c)
        xyc, yzc, zxc = x*yc, y*zc, z*xc
        return cls([
                [x*xc+c, xyc-zs, zxc+ys],
                [xyc+zs, y*yc+c, yzc-xs],
                [zxc-ys, yzc+xs, z*zc+c]])

    @classmethod
    def from_comp(cls,
                  xx=1, xy=0, xz=0,
                  yx=0, yy=1, yz=0,
                  zx=0, zy=0, zz=1):
        return cls([
                [xx, xy, xz],
                [yx, yy, yz],
                [zx, zy, zz]])

    @property
    def I(self):
        return np.linalg.inv(self)

    def rotate(self, vector, theta):
        R = DefGrad.from_axis(vector, theta)
        return R*self*R.T

