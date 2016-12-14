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
    def __init__(self, center, x_unit_vec, y_unit_vec, wa, ha):
        # The center point of the rectangle
        self.center = center
        # the unit vectors in local x and y direction:
        self.x_unit = x_unit_vec
        self.y_unit = y_unit_vec
        # half width of the rectangle in local x direction:
        self.wa = wa
        # half width of the rectangle in local y direction:
        self.ha = ha

    def intersects(self, other):
        # TODO implement seperating axis theorem
