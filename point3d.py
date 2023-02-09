#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: Point3D.py
# 2015.07.08 --
# 2014.04.21 -- transfered into khgeom.py
# 2017.01.08 -- 'transl' -> 'translate'

import numbers
import numpy as np
from numpy.linalg import norm as norm
import scipy as sp
import Vector3D as v3d

filename = 'Point3D.py'

# d2r = np.pi/180
pi = np.pi

# ###/ Point3D /### #


class Point3D:
    """ A 3D point for sun-path diagram and shading calculations.
    credit -- http://codereview.stackexchange.com/questions/12261/what-could-be-improved-in-this-implementation-of-a-vector3d-class
    """

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, name = '',
                 distant = False, size = 20,
                 color = (0, 0, 0)):
        for arg in (x, y, z):
            if not isinstance(arg, numbers.Number):
                raise TypeError
        self.coords = (x, y, z)
        self.coordsAr = [x, y, z]
        self.distant = distant
        self.size = size
        self.__name__ = name
        self.__clr__ = color

    @property
    def x(self):
        return self.coords[0]
    @x.setter
    def x(self, number):
        self.coords = (number, self.coords[1], self.coords[2])
        self.coordsAr = [number, self.coords[1], self.coords[2]]

    @property
    def y(self):
        return self.coords[1]
    @y.setter
    def y(self, number):
        self.coords = (self.coords[0], number, self.coords[2])
        self.coordsAr = [self.coords[0], number, self.coords[2]]

    @property
    def z(self):
        return self.coords[2]
    @z.setter
    def z(self, number):
        self.coords = (self.coords[0], self.coords[1], number)
        self.coordsAr = [self.coords[0], self.coords[1], number]

    @property
    def name(self):
        return self.__name__
    @name.setter
    def name(self, text):
        self.__name__ = text

    @property
    def color(self):
        return self.__clr__
    @color.setter
    def color(self, color=(0, 0, 0)):
        self.__clr__ = color

    @property
    def azimuth(self):
        """Returns the solar azimuth of the point (with respect to (0, 0, 0)"""

        result = 'error'
        #GeoGebra:
        # dFi = If(yY ≥ 0, 180°, If((yY < 0) ∧ (xX > 0), 360°, 0°))
        # atancXY = atand(xX / yY) + dFi
        # (in kh world)
        if self.coords[1]>=0:
            dFi = pi
        elif self.coords[1]<0 and self.coords[0]>0:
            dFi = 2*pi
        else:
            dFi = 0
        try:
            result = np.rad2deg(np.arctan(self.coords[0]/self.coords[1])+dFi)
        except ZeroDivisionError:
            result = 270
        return result

    @property
    def altitude(self):
        """Returns the solar altitude of the point (with respect to (0, 0, 0)"""

        d = np.sqrt(self.coords[0]**2 + self.coords[1]**2)
        return np.rad2deg(np.arctan(self.coords[2]/d))

    @property
    def getCPoint(self):
        """Returns a pair of values: solar azimuth and solar altitude"""

        return (self.azimuth, self.altitude)

    def getPoint0(self):
        """Gets horizontal projection of the point itself"""

        x = self.coords[0]
        y = self.coords[1]
        name = self.name + '_0'
        return Point3D(x, y, 0, name)

    def distance(self, other):
        """Distance between two points"""

        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        d = np.sqrt(x**2 + y**2 + z**2)
        return d

    def translate(self, dx=0, dy=0, dz=0, name='_t', orgName=False, **kwargs):
        """transl(dx, dy, dz) -- translation of the point.
        input: dx, dy, dz, or v - translation vector
        return: point translated by (dx, dy, dz), or (v.x, v.y, v.z)
        """

        if 'v' not in kwargs:
            #print('type of self.x: ' + str(type(self.x)))
            #print('type of dx: ' + str(type(dx)))
            newX = self.x + dx
            newY = self.y + dy
            newZ = self.z + dz
        elif 'v' in kwargs: # 2016.05.17
            v = kwargs['v']
            newX = self.x + v.x
            newY = self.y + v.y
            newZ = self.z + v.z
        if orgName==False:
            newName = name
        else:
            newName = name + '<-(' + self.__name__ + ')'
        distant=False
        if 'distant' in kwargs:
            distant = kwargs['distant']
        return Point3D(newX, newY, newZ, name=newName, distant=distant)

    def rot0(self, fi, name='_rot'):
        """rot(fi) -- rotation of the point about (0, 0).
        input: fi - rotation angle
        return: point rotated by fi
        !!!http://math.stackexchange.com/questions/2429/rotate-a-point-in-circle-about-an-angle
        https://en.wikipedia.org/wiki/Rotation_%28mathematics%29#Two_dimensions
        """

        x = self.x; y = self.y; z = self.z
        newName = self.__name__ + name + '(' + str(fi) + ')'
        newX = x*np.cos(np.deg2rad(fi)) + y*np.sin(np.deg2rad(fi)) ## c. out: 2016.10.3
        newY = y*np.cos(np.deg2rad(fi)) - x*np.sin(np.deg2rad(fi))  ## c. out: 2016.10.3
        return Point3D(newX, newY, z, name=newName)

    def rot(self, other, fi, name='', color=(0, 0, 1)):
        """Point rotation about arbitrary point 'other'"""

        trV = v3d.Vector3D(end=(other.x, other.y, other.z))
        Pp = self.translate(v=trV*(-1))
        Pb = Pp.rot0(fi)
        Presult = Pb.translate(v=trV)
        Presult.color = color
        Presult.__name__ = name
        return Presult

    def getCTPoint(self, other):

        dotProd = np.dot(other.coordsAr, self.coordsAr)
        magnProd = norm(other.coordsAr)*norm(self.coordsAr)
        acos = dotProd/magnProd
        ttAngle = np.rad2deg(np.arccos(acos))
        return (self.azimuth, ttAngle)

    def getRange(self, other, dens):

        ptDif = (other - self)*(1/dens)
        rangeLs = list([self])
        for i in range(1, dens):
            interP = self + ptDif*i
            interP.name = "P"
            rangeLs.append(interP)
        rangeLs.append(other)
        return rangeLs

    def getMidpoint(self, other):
        """Gets the midpoint between self and the other
        Argument: other, Point3D; returned new Point3D"""

        newX = (self.x + other.x)/2
        newY = (self.y + other.y)/2
        newZ = (self.z + other.z)/2
        return Point3D(newX, newY, newZ, 'midP')

    def getCoordsAr(self):

        return self.coordsAr

    def getCoordsArSt(self):

        coordsAr = self.coordsAr
        return '[{: .2f}, {: .2f}, {: .2f}]'.format(coordsAr[0], coordsAr[1],
                                                    coordsAr[2])

    def getX(self):

        return self.x

    def getName(self):

        return self.name

    def scatter3D(self, ax, s=None, nameOffset=None):
        """Scattering the point, ax -- 3D axes. nameOffset = (x, y)"""

        if s is None:
            s = self.size
        if nameOffset is not None:
            tX = nameOffset[0]
            tY = nameOffset[1]
            ax.scatter(self.x, self.y, self.z, s=s, color=self.__clr__)
            ax.text(x=self.x+tX, y=self.y+tY, z=self.z, s=self.name)
        # ~ if ax.is_figure_set():
        ax.scatter(self.x, self.y, self.z, s=s, color=self.__clr__)

    def scatter2D(self, ax, s=20):
        """Scattering the point, ax -- 2D axes"""

        ax.scatter(self.x, self.y, s=s, color=self.__clr__)

    def __getitem__(self, index):

        return self.coordsAr[index]

    def __add__(self, other):

        if isinstance(other, Point3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, numbers.Number):
            return Point3D(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):

        if isinstance(other, Point3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, numbers.Number):
            return Point3D(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):

        if isinstance(other, Point3D):
            return Point3D(self.x*other.x, self.y*other.y, self.z*other.z)
        if isinstance(other, numbers.Number):
            return Point3D(self.x*other, self.y*other, self.z*other)

    def __truediv__(self, other):

        results = list([])
        if isinstance(other, Point3D):
            for i in range(len(self.coords)):
                try:
                    results.append(self.coords[i]/other.coords[i])
                except ZeroDivisionError:
                    print('Division by zero')
                    results.append(float('inf'))
            return Point3D(results[0], results[1], results[2])
        if isinstance(other, numbers.Number):
            for i in range(len(self.coords)):
                try:
                    results.append(self.coords[i]/other)
                except ZeroDivisionError:
                    print('Division by 0')
                    results.append(float('inf'))
            return Point3D(results[0], results[1], results[2])

    def __invert__(self):
        #!!! 1/0 !!!

        return Point3D(1/self.x, 1/self.y, 1/self.z, name='inv' + self.nm)

    def __neg__(self):

        coords = self.coords
        x = coords[0]
        y = coords[1]
        z = coords[2]
        Pres = Point3D(-x, -y, -z, name=self.name + '_neg')
        return Pres

    def __repr__(self):

        if not self.distant:
            distS = ', not distant'
        else:
            distS = ', distant'
        # return 'Point ' + self.name + ' = ({0: .2f}, {1: .2f}, {2: .2f}){3}'.\
        #        format(self.coords[0], self.coords[1], self.coords[2], distS)
        return (f"Point {self.name:5} = ({self.coords[0]: .2f}, "
                f"{self.coords[1]: .2f}, {self.coords[2]: .2f}){distS}")

# ###/ Point3D /### #


if __name__ == '__main__':
    print(filename + ' demo')
    from Point3D import Point3D
    import scipy as sp

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #ax.view_init(elev=elev, azim=azim)
    # ~ ax.set_aspect('equal')

    dens = .1
    xes = [x for x in np.arange(-np.pi, np.pi, dens)]
    yes = [np.cos(x) for x in xes]
    zes = [np.cos(x)**2 for x in xes]
    #yes = [0 for x in xes]
    #zes = [np.sin(x) for x in xes]
    points = []
    for i in range(len(xes)):
        P = Point3D(xes[i], yes[i], zes[i])
        points.append(P)
    for P in points:
        P.scatter3D(ax)
    dl = 0.3
    ax.set_xlim([min(xes)-dl, max(xes)+dl])
    ax.set_ylim([min(yes)-dl, max(yes)+dl])
    ax.set_zlim([min(zes)-dl, max(zes)+dl])
    plt.show()
