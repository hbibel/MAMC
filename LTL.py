# -*- coding: utf-8 -*-
"""
@author: Hannes Bibel
"""


class LTL(object):

    def __init__(self, operand, left, right):
        # Operands can be
        # - LTL operands: G, F, X, U, R, &, |, !, true, false
        # - tokens: any terminal symbol
        self.operand = operand
        # For U, & and | formulas, left is the LTL object left of the operand.
        # Otherwise, it is None.
        self.left = left
        # For G, F, X, U, & and | formulas, right is the LTL formula right of
        # the operand.
        # Otherwise, it is None.
        self.right = right

    def __repr__(self):
        l = ''
        r = ''
        o = self.operand
        if self.left is not None:
            l = '(' + repr(self.left) + ')'
        if self.right is not None:
            r = '(' + repr(self.right) + ')'
        return l + ' ' + o + ' ' + r

    def __eq__(self, other):
        """
        Checks for structural equality, not logical equivalence
        """
        return (self.operand == other.operand and
                self.left == other.left and
                self.right == other.right)

    def toNNF(self):
        """
        Transforms an LTL formula to negated normal form.
        In NNF, negations (!) appear only in front of atomic propisitions.
        Additionally, this method rewrites a formula such that it only uses
        G, &, |, X, R and U.
        """
        if self.operand in ['true', 'false']:
            return self
        elif self.operand == 'X':
            return LTL(self.operand, None, self.right.toNNF())
        elif self.operand == 'G':
            # G phi = false R phi
            return LTL('R', LTL('false'), self.right.toNNF())
        elif self.operand == 'F':
            # F phi = true U phi
            return LTL('U', LTL('true', None, None), self.right.toNNF())
        elif self.operand in 'UR&|':
            return LTL(self.operand, self.left.toNNF(), self.right.toNNF())
        elif self.operand == '!':
            if self.right.operand == '!':
                return self.right.right.toNNF()
            elif self.right.operand == 'G':
                # !(G phi) = F (!phi) = true U (!phi)
                notphi = LTL('!', None, self.right.right).toNNF()
                return LTL('U', LTL('true', None, None), notphi)
            elif self.right.operand == 'F':
                # !(F phi) = G(!phi) = false R (!phi)
                notphi = LTL('!', None, self.right.right).toNNF()
                return LTL('R', LTL('false', None, None), notphi)
            elif self.right.operand == 'X':
                notphi = LTL('!', None, self.right.right).toNNF()
                return LTL('X', None, notphi)
            elif self.right.operand == 'U':
                # !(phi U psi) = (!phi) R (!psi)
                notphi = LTL('!', None, self.right.left).toNNF()
                notpsi = LTL('!', None, self.right.right).toNNF()
                return LTL('R', notphi, notpsi)
            elif self.right.operand == 'R':
                # !(phi R psi) = (!phi) U (!psi)
                notphi = LTL('!', None, self.right.left).toNNF()
                notpsi = LTL('!', None, self.right.right).toNNF()
                return LTL('U', notphi, notpsi)
            elif self.right.operand == '&':
                # !(phi & psi) == (!phi) | (!psi)
                notphi = LTL('!', None, self.right.left).toNNF()
                notpsi = LTL('!', None, self.right.right).toNNF()
                return LTL('|', notphi, notpsi)
            elif self.right.operand == '|':
                # !(phi | psi) == (!phi) & (!psi)
                notphi = LTL('!', None, self.right.left).toNNF()
                notpsi = LTL('!', None, self.right.right).toNNF()
                return LTL('&', notphi, notpsi)
            elif self.right.operand == 'true':
                return LTL('false')
            elif self.right.operand == 'false':
                return LTL('true')
            else:
                return self
        else:
            return self
