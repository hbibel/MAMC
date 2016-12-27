# -*- coding: utf-8 -*-

"""
We don't store the states of the product automaton explicitely, since their
number is infinite.
"""

from LTL import LTL
from copy import deepcopy


class PA(object):
    def __init__(self, ks, ma):
        self.ma = ma
        self.ks = ks

    def find_witness(self, max_iterations=50000):
        """
        Attempts to find an accepting run for the product automaton, using
        breadth-first search.
        Returns the trace of maneuvers, if an accepting run is found, or
        None otherwise.
        """
        depth = max_iterations
        final_maneuver = None
        queue = [(self.ma.initial_state, self.ks.initial_state, [])]
        while final_maneuver is None and depth >= 0 and len(queue) > 0:
            qm, qk, trace = queue[0]
            # The atomic propositions that hold true in the beginning of qm
            valid_aps = [ap for ap in self.ks.aps if qm.entails(ap, False)]
            if (self.ks.states[qk.readletter(frozenset(valid_aps))].label ==
                    LTL('false', None, None)):
                # Found counterexample, return witness trajectory
                return True, trace
            # We need a deep copy here, since the trace differs for every
            # maneuver
            newtrace = deepcopy(trace)
            newtrace.append(qm)
            # The atomic propositions that hold true for the duration of qm
            valid_aps = [ap for ap in self.ks.aps if qm.entails(ap, True)]
            # The next state in the Kripke structure after reading the
            # valid atomic propositions
            qk_next = self.ks.states[qk.readletter(frozenset(valid_aps))]
            if len(queue) > 0:
                queue = queue[1:]
            depth -= 1
            if (qk_next.label == LTL('true', None, None)):
                continue
            # The successor maneuvers of qm
            qm_sms = qm.successors()
            for qm_next in qm_sms:
                queue.append((qm_next, qk_next, newtrace))
        return False, None
