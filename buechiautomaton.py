# -*- coding: utf-8 -*-

from ltlparser import parse


class BA(object):
    class State(object):
        def __init__(self, id):
            self.id = id
            self.transitions = dict()

        def add_transition(self, aps, to_id):
            """
            aps: set of atomic propositions
            to_id: id of the target state
            """
            self.transitions[aps] = to_id

        def readletter(self, letter):
            """
            Returns the id of the target state after reading the letter.
            A letter is a frozenset of atomic propositions
            """
            if letter not in self.transitions.keys():
                return None
            return self.transitions[letter]

    def __init__(self, ltl):
        """
        This is merely a mock of an actual constructor
        """
        if (ltl == parse('!obstace U goal')):
            # Note that this automaton is not deterministic
            self.states = [BA.State(0), BA.State(1)]
            self.states[0].add_transition(frozenset(), 0)
            self.states[0].add_transition(frozenset(['goal', 'obstacle']), 1)
            self.states[0].add_transition(frozenset(['goal']), 1)
            self.states[1].add_transition(frozenset([]), 1)
            self.states[1].add_transition(frozenset(['goal']), 1)
            self.states[1].add_transition(frozenset(['obstacle']), 1)
            self.states[1].add_transition(frozenset(['goal', 'obstacle']), 1)
            self.aps = set(['goal', 'obstacle'])
            self.initial_state = self.states[0]
