# -*- coding: utf-8 -*-

import sys
from ltlparser import parse
from buechiautomaton import BA
from maneuverautomaton import MA


def main(argv):
    ltl = parse('!obstace U goal')
    ba = BA(ltl)
    ma = MA()

if __name__ == '__main__':
    main(sys.argv[1:])
