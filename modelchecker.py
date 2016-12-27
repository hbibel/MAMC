# -*- coding: utf-8 -*-

# Author: Hannes Bibel (bibel@in.tum.de)

import sys
from ltlparser import parse
from LTL import LTL
from maneuverautomaton import MA
from productautomaton import PA
from kripkestructure import KripkeStructure
from tkinter import Tk, Canvas, mainloop
from util import interpretation, draw_rectangle, red, green, blue, transp
from util import draw_line, draw_dot


def run_model_checker(canvas):
    phi = parse('(!obstacle) U goal')
    notphi = LTL('!', None, phi).toSafeLTL()
    ks = KripkeStructure(notphi)
    ma = MA(init_position=(32.0, 2.0))
    pa = PA(ks, ma)
    draw_rectangle(canvas, interpretation('goal'), green, green)
    draw_rectangle(canvas, interpretation('obstacle'), red, red)
    witness_found, trace = pa.find_witness()
    if witness_found:
        for qm in trace:
            xs, ys = qm.starting_position
            xf, yf = qm.final_position
            draw_dot(canvas, xs, ys)
            draw_dot(canvas, xf, yf)
            draw_line(canvas, xs, ys, xf, yf)
            draw_rectangle(canvas, qm.initial_occupancy(), blue, transp)
            draw_rectangle(canvas, qm.overall_occupancy(), blue, transp)
    else:
        print('No witness trajectory found')


def main(argv):
    master = Tk()
    canvas_width = 1280
    canvas_height = 960
    canvas = Canvas(master,
                    width=canvas_width,
                    height=canvas_height)
    canvas.pack()
    master.after(0, run_model_checker, canvas)
    mainloop()

if __name__ == '__main__':
    main(sys.argv[1:])
