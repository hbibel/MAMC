# -*- coding: utf-8 -*-

"""
We encode rectangles like this:
    <------wa------->
    +------------------------------+ ^
    |                              | |
    |               ^ y_unit       | ha
    |               |              | |
    |          center--> x_unit    | v
    |                              |
    |                              |
    |                              |
    +------------------------------+

"""


class Rectangle(object):
    def __init__(self, center, x_unit_vec, y_unit_vec, halfwidth, halfheight):
        # The center point of the rectangle
        self.center = center
        # the unit vectors in local x and y direction:
        self.x_unit = x_unit_vec
        self.y_unit = y_unit_vec
        # half width of the rectangle in local x direction:
        self.w = halfwidth
        # half width of the rectangle in local y direction:
        self.h = halfheight

    def intersects(self, other):
        # t: vector from other.center to self.center
        t = self.center[0] - other.center[0], self.center[1] - other.center[1]
        # The unit vectors in local x and y direction are the candidates
        # for separating axes:
        sa_candidates = [self.x_unit, self.y_unit, other.x_unit, other.y_unit]
        for l in sa_candidates:
            # |t * l|
            tl = abs(t[0]*l[0] + t[1]*l[1])
            # |self.w * self.x_unit * l|
            self_wxl = abs(self.w*(self.x_unit[0]*l[0] + self.x_unit[1]*l[1]))
            # |self.h * self.y_unit * l|
            self_hyl = abs(self.h*(self.y_unit[0]*l[0] + self.y_unit[1]*l[1]))
            # |other.w * other.x_unit * l|
            o_wxl = abs(other.w*(other.x_unit[0]*l[0] + other.x_unit[1]*l[1]))
            # |other.h * other.y_unit * l|
            o_hyl = abs(other.h*(other.y_unit[0]*l[0] + other.y_unit[1]*l[1]))
            if tl > self_wxl + self_hyl + o_wxl + o_hyl:
                return True
        return False

    def contains(self, other):
        # a, b, c, d: The 4 corner points of the other rectangle, in local
        # coordinates
        a = self.convert_to_local_cs(other.center[0]+other.w,
                                     other.center[1]+other.h)
        b = self.convert_to_local_cs(other.center[0]+other.w,
                                     other.center[1]-other.h)
        c = self.convert_to_local_cs(other.center[0]-other.w,
                                     other.center[1]-other.h)
        d = self.convert_to_local_cs(other.center[0]-other.w,
                                     other.center[1]+other.h)
        abcd_in_self = True
        for p in [a, b, c, d]:
            abcd_in_self = (abcd_in_self and
                            abs(p[0]) <= self.w and
                            abs(p[1]) <= self.h)
        return abcd_in_self

    def convert_to_local_cs(self, vec):
        v = (vec[0]-self.center[0], vec[1]-self.center[1])
        c = 1/(self.x_unit[0]*self.y_unit[1] - self.y_unit[0]*self.x_unit[1])
        x = c*(v[0]*self.y_unit[1] + v[1]*self.y_unit[0])
        y = c*(-v[0]*self.x_unit[1] + v[1]*self.x_unit[0])
        return x, y
