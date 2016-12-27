# -*- coding: utf-8 -*-

from ltlparser import parse
from LTL import LTL


class KripkeStructure(object):
    class State(object):
        def __init__(self, id, label):
            """
            id: Unique positive integer id for the state
            label: LTL formula
            """
            self.id = id
            self.label = label
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
            If the letter does not transition into another state, -1 is
            returned.
            A letter is a frozenset of atomic propositions
            """
            if letter not in self.transitions.keys():
                return -1
            return self.transitions[letter]

    def __init__(self, ltl):
        """
        This is merely a mock for an actual constructor
        """
        if (ltl == parse('obstacle R (!goal)')):
            self.states = [KripkeStructure.State(0, ltl),
                           KripkeStructure.State(1, LTL('true', None, None)),
                           KripkeStructure.State(2, LTL('false', None, None))]
            # The interpretation of an atomic proposition with a '$' at the end
            # is the opposite of the interpretation of the atomic proposition
            # without the '$'. E.g. the interpretation of 'goal$' is everything
            # but the interpretation of 'goal'.
            self.aps = set(['goal', 'goal$', 'obstacle', 'obstacle$'])
            self.states[0].add_transition(frozenset(), 0)
            self.states[0].add_transition(frozenset(['goal']), 2)
            self.states[0].add_transition(frozenset(['obstacle']), 1)
            self.states[0].add_transition(frozenset(['goal$']), 1)
            self.states[0].add_transition(frozenset(['obstacle$']), 0)
            self.states[0].add_transition(frozenset(['goal$', 'obstacle$']), 0)
            self.states[0].add_transition(frozenset(['goal$', 'obstacle']), 1)
            self.states[0].add_transition(frozenset(['goal', 'obstacle$']), 2)
            self.states[0].add_transition(frozenset(['goal', 'obstacle']), 2)
            self.states[1].add_transition(frozenset(), 1)
            self.states[1].add_transition(frozenset(['goal']), 1)
            self.states[1].add_transition(frozenset(['obstacle']), 1)
            self.states[1].add_transition(frozenset(['goal$']), 1)
            self.states[1].add_transition(frozenset(['obstacle$']), 1)
            self.states[1].add_transition(frozenset(['goal$', 'obstacle$']), 1)
            self.states[1].add_transition(frozenset(['goal$', 'obstacle']), 1)
            self.states[1].add_transition(frozenset(['goal', 'obstacle$']), 1)
            self.states[1].add_transition(frozenset(['goal', 'obstacle']), 1)
            self.states[2].add_transition(frozenset(), 2)
            self.states[2].add_transition(frozenset(['goal']), 2)
            self.states[2].add_transition(frozenset(['obstacle']), 2)
            self.states[2].add_transition(frozenset(['goal$']), 2)
            self.states[2].add_transition(frozenset(['obstacle$']), 2)
            self.states[2].add_transition(frozenset(['goal$', 'obstacle$']), 2)
            self.states[2].add_transition(frozenset(['goal$', 'obstacle']), 2)
            self.states[2].add_transition(frozenset(['goal', 'obstacle$']), 2)
            self.states[2].add_transition(frozenset(['goal', 'obstacle']), 2)
            self.initial_state = self.states[0]
