# -*- coding: utf-8 -*-

"""
We don't store the states of the product automaton explicitely, since their
number is infinite.
"""

from LTL import LTL
from util import draw_dot


class PA(object):
    def __init__(self, ks, ma):
        self.ma = ma
        self.ks = ks

# TODO remove canvas from method signature
    def find_witness(self, canvas, max_iterations=5000):
        """
        Attempts to find an accepting run for the product automaton, using
        breadth-first search.
        Returns the trace of maneuvers, if an accepting run is found, or
        None otherwise.
        """
        depth = max_iterations
        final_maneuver = None
        queue = [(self.ma.initial_state, self.ks.initial_state, [])]
        while final_maneuver is None and depth >= 0:
            qm, qk, trace = queue[0]
            print('pa.py: ' + str(qm.starting_position[0]) + ', ' + str(qm.starting_position[1]))
            draw_dot(canvas, qm.starting_position[0], qm.starting_position[1])
            # The atomic propositions that hold true in the beginning of qm
            valid_aps = [ap for ap in self.ks.aps if qm.entails(ap, False)]
            if (self.ks.states[qk.readletter(frozenset(valid_aps))].label ==
                    LTL('false', None, None)):
                # Found counterexample, return witness trajectory
                print('pa.py: steps: ' + str(depth))
                return True, trace
            trace.append(qm)
            # The atomic propositions that hold true for the duration of qm
            valid_aps = [ap for ap in self.ks.aps if qm.entails(ap, True)]
            # The next state in the Kripke structure after reading the
            # valid atomic propositions
            qk_next = self.ks.states[qk.readletter(frozenset(valid_aps))]
            # The successor maneuvers of qm
            qm_sms = qm.successors()
            for q in qm_sms:
                queue.append((q, qk_next, trace))
            queue = queue[1:]
            depth -= 1
        return False, None
