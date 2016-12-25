# -*- coding: utf-8 -*-

import sys
from ltlparser import parse
from LTL import LTL
from maneuverautomaton import MA
from productautomaton import PA
from kripkestructure import KripkeStructure
from tkinter import Tk, Canvas, mainloop
from util import interpretation, draw_rectangle, red, green, blue, transp


def non_gui_stuff(canvas):  # TODO Half of the stuff in here is GUI though
    phi = parse('(!obstacle) U goal')
    notphi = LTL('!', None, phi).toSafeLTL()
    ks = KripkeStructure(notphi)
    ma = MA(init_position=(32.0, 2.0))
    pa = PA(ks, ma)
    draw_rectangle(canvas, interpretation('goal'), green, transp)
    draw_rectangle(canvas, interpretation('obstacle'), red, red)
    # draw_rectangle(canvas, ma.initial_state.initial_occupancy(), blue, transp)
    # draw_rectangle(canvas, ma.initial_state.overall_occupancy(), blue, transp)
    witness_found, trace = pa.find_witness(canvas)
    if witness_found:
        for qm in trace:
            draw_rectangle(canvas, qm.initial_occupancy(), blue, transp)
            draw_rectangle(canvas, qm.overall_occupancy(), blue, transp)
    else:
        print('No witness trajectory found')


def main(argv):
    master = Tk()
    canvas_width = 640
    canvas_height = 480
    canvas = Canvas(master,
                    width=canvas_width,
                    height=canvas_height)
    canvas.pack()
    master.after(0, non_gui_stuff, canvas)
    mainloop()

if __name__ == '__main__':
    main(sys.argv[1:])
