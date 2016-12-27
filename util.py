# -*- coding: utf-8 -*-

# Author: Hannes Bibel (bibel@in.tum.de)

from rectangle import Rectangle


def interpretation(ap):
    if ap.startswith('goal'):
        return Rectangle((32.0, 40.0), (1.0, 0.0), (0.0, 1.0), 3.0, 3.0)
    if ap.startswith('obstacle'):
        return Rectangle((32.0, 16.0), (1.0, 0.0), (0.0, 1.0), 2.0, 1.0)
    return None


red = '#f00'
green = '#0f0'
blue = '#00f'
transp = ''


def draw_rectangle(canvas, rect, outline, fill):
    # a, b, c, d: Corner points of the rectangle
    ax = rect.center[0] + rect.x_unit[0]*rect.w + rect.y_unit[0]*rect.h
    ay = rect.center[1] + rect.x_unit[1]*rect.w + rect.y_unit[1]*rect.h
    bx = rect.center[0] + rect.x_unit[0]*rect.w - rect.y_unit[0]*rect.h
    by = rect.center[1] + rect.x_unit[1]*rect.w - rect.y_unit[1]*rect.h
    cx = rect.center[0] - rect.x_unit[0]*rect.w - rect.y_unit[0]*rect.h
    cy = rect.center[1] - rect.x_unit[1]*rect.w - rect.y_unit[1]*rect.h
    dx = rect.center[0] - rect.x_unit[0]*rect.w + rect.y_unit[0]*rect.h
    dy = rect.center[1] - rect.x_unit[1]*rect.w + rect.y_unit[1]*rect.h
    canvas.create_polygon(ax*20, ay*20, bx*20, by*20, cx*20, cy*20, dx*20,
                          dy*20, outline=outline, fill=fill)


def draw_dot(canvas, x, y):
    canvas.create_oval(x*20-4, y*20-4, x*20+4, y*20+4, fill='#3d0')


def draw_line(canvas, x1, y1, x2, y2):
    canvas.create_line(x1*20, y1*20, x2*20, y2*20)
