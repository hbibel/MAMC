# -*- coding: utf-8 -*-

import sys
from ltlparser import parse
from LTL import LTL
from buechiautomaton import BA
from maneuverautomaton import MA
from productautomaton import PA
from kripkestructure import KripkeStructure


def main(argv):
    phi = parse('(!obstacle) U goal')
    notphi = LTL('!', None, phi).toSafeLTL()
    ks = KripkeStructure(notphi)
    ma = MA()
    pa = PA(ks, ma)
    pa.find_acc_run(max_depth=1)

if __name__ == '__main__':
    main(sys.argv[1:])
