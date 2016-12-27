# -*- coding: utf-8 -*-

# Author: Hannes Bibel (bibel@in.tum.de)


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

    def toSafeLTL(self):
        """
        Transforms an LTL formula to syntactically safe form.
        In SSF, similarly to negated normal form, negations (!) appear only in
        front of atomic propisitions.
        Additionally, this method rewrites a formula such that it only uses
        &, |, G, X, U and R.
        """
        if self.operand in ['true', 'false']:
            return self
        elif self.operand == 'X':
            return LTL(self.operand, None, self.right.toSafeLTL())
        elif self.operand == 'G':
            return LTL(self.operand, None, self.right.toSafeLTL())
        elif self.operand == 'F':
            # F phi = true U phi
            return LTL('U', LTL('true', None, None), self.right.toSafeLTL())
        elif self.operand in 'UR&|':
            return LTL(self.operand, self.left.toSafeLTL(),
                       self.right.toSafeLTL())
        elif self.operand == '!':
            if self.right.operand == '!':
                return self.right.right.toSafeLTL()
            elif self.right.operand == 'G':
                # !(G phi) = F (!phi) = true U (!phi)
                notphi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('U', LTL('true', None, None), notphi)
            elif self.right.operand == 'F':
                # !(F phi) = G(!phi)
                notphi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('G', notphi)
            elif self.right.operand == 'X':
                # !(X phi) = X (!phi)
                notphi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('X', None, notphi)
            elif self.right.operand == 'U':
                # !(phi U psi) = (!phi) R (!psi)
                notphi = LTL('!', None, self.right.left).toSafeLTL()
                notpsi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('R', notphi, notpsi)
            elif self.right.operand == 'R':
                # !(phi R psi) = (!phi) U (!psi)
                notphi = LTL('!', None, self.right.left).toSafeLTL()
                notpsi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('U', notphi, notpsi)
            elif self.right.operand == '&':
                # !(phi & psi) == (!phi) | (!psi)
                notphi = LTL('!', None, self.right.left).toSafeLTL()
                notpsi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('|', notphi, notpsi)
            elif self.right.operand == '|':
                # !(phi | psi) == (!phi) & (!psi)
                notphi = LTL('!', None, self.right.left).toSafeLTL()
                notpsi = LTL('!', None, self.right.right).toSafeLTL()
                return LTL('&', notphi, notpsi)
            elif self.right.operand == 'true':
                return LTL('false')
            elif self.right.operand == 'false':
                return LTL('true')
            else:
                # self is an atomic proposition
                return self
        else:
            # self is an atomic proposition
            return self
