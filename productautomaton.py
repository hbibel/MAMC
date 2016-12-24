# -*- coding: utf-8 -*-

"""
We don't store the states of the product automaton explicitely, since their
number is infinite.
"""

from LTL import LTL


class PA(object):
    def __init__(self, ks, ma):
        self.ma = ma
        self.ks = ks

    def find_acc_run(self, max_depth=50):  # The 50 is rather arbitrary
        """
        Attempts to find an accepting run for the product automaton, using
        breadth-first search.
        Returns the trace of maneuvers, if an accepting run is found, or
        None otherwise.
        """
        depth = max_depth
        final_maneuver = None
        queue = [(self.ma.initial_state, self.ks.initial_state, [])]
        while final_maneuver is None and depth >= 0:
            qm, qk, trace = queue[0]
            # The atomic propositions that hold Frue for the duration of qm
            valid_aps = [ap for ap in self.ks.aps if qm.entails(ap, True)]
            print('productautomaton.py: ' + str(valid_aps))
            depth -= 1
        return trace
