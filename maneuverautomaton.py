# -*- coding: utf-8 -*-

from math import pi, sin, cos
from rectangle import Rectangle
from util import interpretation


"""
Orientations range from 0 to 7, where 0 is in x direction, 2 is in y direction,
4 is in negative x direction and 6 is in negative y direction.
3 2 1
 \|/
4- -0
 /|\
5 6 7

turns are on a circle of radius 5/(pi/4) = 6.366...
straight maneuvers have a length of 5
"""


class MA(object):
    def __init__(self, init_position=(0.0, 0.0)):
        go_straight = MA.ManeuverType("straight")
        left_turn = MA.ManeuverType("left")
        right_turn = MA.ManeuverType("right")
        self.maneuver_types = [go_straight, left_turn, right_turn]
        # self.transitions = None
        self.initial_state = MA.Maneuver(go_straight, init_position, 2)
        self.accepting_states = None
        # self.orientation = None
        self.position = init_position

    def get_discrete_state(self):
        return (self.position, self.orientation)

    class ManeuverType(object):
        # useless wrapper for a string; can be designed out.
        def __init__(self, name):
            self.name = name

    class Maneuver(object):
        def __init__(self, t, start_pos, start_or):
            self.type = t
            self.starting_position = start_pos
            self.initial_orientation = start_or
            if self.type.name == "straight":
                # self.final_position = (start_pos[0] + cos(start_or*pi/4)*5,
                #                        start_pos[1] + sin(start_or*pi/4)*5)
                s = 5.0
                h = 0.0
                self.final_orientation = start_or
            elif self.type.name == "left":
                self.final_orientation = (start_or + 1) % 8
                h = 5/(pi/4)*(1-cos(pi/4))
                s = 5/(pi/4)*sin(pi/4)
            elif self.type.name == "right":
                self.final_orientation = (start_or - 1) % 8
                h = -5/(pi/4)*(1-cos(pi/4))
                s = 5/(pi/4)*sin(pi/4)
            self.final_position = (start_pos[0] + cos(start_or*pi/4)*s +
                                   (-sin(start_or*pi/4))*h,
                                   start_pos[1] + sin(start_or*pi/4)*s +
                                   cos(start_or*pi/4)*h)

        def successors(self):
            straight = MA.Maneuver(MA.ManeuverType("straight"),
                                   self.final_position, self.final_orientation)
            left = MA.Maneuver(MA.ManeuverType("left"), self.final_position,
                               self.final_orientation)
            right = MA.Maneuver(MA.ManeuverType("right"), self.final_position,
                                self.final_orientation)
            return [straight, left, right]

        def initial_occupancy(self):
            orientation = self.initial_orientation
            start_pos = self.starting_position
            # We overapproximate the occupancy by a rectangle
            return Rectangle(start_pos,
                             (cos(orientation*pi/4), sin(orientation*pi/4)),
                             (-sin(orientation*pi/4), cos(orientation*pi/4)),
                             0.5, 0.5)

        def overall_occupancy(self):
            """
            Returns a rectangle that overapproximates the occupancy of the
            maneuver
            """
            orientation = self.initial_orientation
            start_pos = self.starting_position
            # We overapproximate the occupancy by a rectangle
            if self.type.name == "straight":
                return Rectangle((start_pos[0] + 2.0*cos(orientation*pi/4),
                                  start_pos[1] + 2.0*sin(orientation*pi/4)),
                                 (cos(orientation*pi/4),
                                  sin(orientation*pi/4)),
                                 (-sin(orientation*pi/4),
                                  cos(orientation*pi/4)), 2.5, 0.5)
            elif self.type.name == "left":
                # geometry yadda yadda; hard to explain, better
                # draw it down and check for yourself if you doubt those
                # formulas (which you should, because I might have made
                # mistakes)
                r = 5/(pi/4)
                # cos(pi/4) == sin(pi/4)
                csp = sin(pi/4)
                seg_width = r*csp
                seg_height = r*(1-csp)
                wa = (0.5 + seg_width + 0.5*csp)/2
                ha = (seg_height + 0.5 + 0.5*csp)/2
                if self.initial_orientation == 0:
                    cx = start_pos[0] - 0.5 + wa
                    cy = start_pos[1] - 0.5 + ha
                    x_vec = (1.0, 0.0)
                    y_vec = (0.0, 1.0)
                elif self.initial_orientation == 1:
                    cx = start_pos[0] + wa*csp - ha*csp
                    cy = start_pos[1] - 0.5/csp + (ha + wa)*csp
                    x_vec = (csp, csp)
                    y_vec = (-csp, csp)
                elif self.initial_orientation == 2:
                    cx = start_pos[0] + 0.5 - ha
                    cy = start_pos[1] - 0.5 + wa
                    x_vec = (0.0, 1.0)
                    y_vec = (-1.0, 0.0)
                elif self.initial_orientation == 3:
                    cx = start_pos[0] + 0.5/csp - wa*csp - ha*csp
                    cy = start_pos[1] + wa*csp - ha*csp
                    x_vec = (-csp, csp)
                    y_vec = (-csp, -csp)
                elif self.initial_orientation == 4:
                    cx = start_pos[0] + 0.5 - wa
                    cy = start_pos[1] + 0.5 - ha
                    x_vec = -1.0, 0.0
                    y_vec = 0.0, -1.0
                elif self.initial_orientation == 5:
                    cx = start_pos[0] - wa*csp + ha*csp
                    cy = start_pos[1] + 0.5/csp - wa*csp - ha*csp
                    x_vec = -csp, -csp
                    y_vec = csp, -csp
                elif self.initial_orientation == 6:
                    cx = start_pos[0] - 0.5 + ha
                    cy = start_pos[1] + 0.5 - wa
                    x_vec = 0.0, -1.0
                    y_vec = 1.0, 0.0
                elif self.initial_orientation == 7:
                    cx = start_pos[0] - 0.5/csp + (wa + ha)*csp
                    cy = start_pos[1] + (ha - wa)*csp
                    x_vec = csp, -csp
                    y_vec = csp, csp
                center = (cx, cy)
                return Rectangle(center, x_vec, y_vec, wa, ha)
            elif self.type.name == "right":
                r = 5/(pi/4)
                # cos(pi/4) == sin(pi/4)
                csp = sin(pi/4)
                seg_width = r*csp
                seg_height = r*(1-csp)
                wa = (0.5 + seg_width + 0.5*csp)/2
                ha = (seg_height + 0.5 + 0.5*csp)/2
                if self.initial_orientation == 0:
                    cx = start_pos[0] - 0.5 + wa
                    cy = start_pos[1] + 0.5 - ha
                    x_vec = (1.0, 0.0)
                    y_vec = (0.0, 1.0)
                elif self.initial_orientation == 1:
                    cx = start_pos[0] - 0.5/csp + (ha + wa)*csp
                    cy = start_pos[1] + wa*csp - ha*csp
                    x_vec = (csp, csp)
                    y_vec = (-csp, csp)
                elif self.initial_orientation == 2:
                    cx = start_pos[0] - 0.5 + ha
                    cy = start_pos[1] - 0.5 + wa
                    x_vec = (0.0, 1.0)
                    y_vec = (-1.0, 0.0)
                elif self.initial_orientation == 3:
                    cx = start_pos[0] - wa*csp + ha*csp
                    cy = start_pos[1] - 0.5/csp + wa*csp + ha*csp
                    x_vec = (-csp, csp)
                    y_vec = (-csp, -csp)
                elif self.initial_orientation == 4:
                    cx = start_pos[0] + 0.5 - wa
                    cy = start_pos[1] - 0.5 + ha
                    x_vec = -1.0, 0.0
                    y_vec = 0.0, -1.0
                elif self.initial_orientation == 5:
                    cx = start_pos[0] + 0.5/csp - ha*csp - wa*csp
                    cy = start_pos[1] + ha*csp - wa*csp
                    x_vec = -csp, -csp
                    y_vec = csp, -csp
                elif self.initial_orientation == 6:
                    cx = start_pos[0] + 0.5 - ha
                    cy = start_pos[1] + 0.5 - wa
                    x_vec = 0.0, -1.0
                    y_vec = 1.0, 0.0
                elif self.initial_orientation == 7:
                    cx = start_pos[0] + wa*csp - ha*csp
                    cy = start_pos[1] + 0.5/csp - wa*csp - ha*csp
                    x_vec = csp, -csp
                    y_vec = csp, csp
                center = (cx, cy)
                return Rectangle(center, x_vec, y_vec, wa, ha)

        def entails(self, ap, entire_time_interval):
            if entire_time_interval:
                occupancy = self.overall_occupancy()
            else:
                occupancy = self.initial_occupancy()
            r = interpretation(ap.replace('$', ''))
            if ap.endswith('$'):
                if r.intersects(occupancy):
                    return False
                else:
                    return True
            else:
                if r.contains(occupancy):
                    return True
                else:
                    return False
