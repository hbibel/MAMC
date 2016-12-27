# -*- coding: utf-8 -*-
"""

@author: Hannes Bibel
"""

from LTL import LTL


WHITESPACES = ' \t\n\r\f'
TRUE = 'true'
FALSE = 'false'

"""
TODO: This grammar is open for discussion

Our LTL grammar:
formula
    : 'F' formula
    | 'G' formula
    | 'X' formula
    | '!' formula
    | orformula
    | atom
    ;

orformula
    : andformula ('|' andformula)*
    ;

andformula
    : uformula ('&' uformula)*
    ;

uformula
    : atom ('U' atom)?
    | atom ('R' atom)?
    ;

atom
    : '(' formula ')'
    | Boolean
    | Identifier
    ;

Boolean
    : 'tt'
    | 'ff'
    ;

Identifier
    : [a-zA-Z]+
"""


def parse(input_string):
    token_list = _lex(input_string)
    # Saving atomic propositions is not necessary for the current
    # state of this program, but if the need ever arises, this should be done
    # here
    return _parse_formula(token_list)


def _lex(input_string):
    """
    This function returns a list of all character sequences in input_string
    that are divided by whitespace or parentheses, including the
    parentheses themselves.

    >>> _lex('alice & (bob | carol)')
    ['alice', '&', '(', 'bob', '|', 'carol', ')']
    """
    token_list = []
    tmp = ''
    for c in input_string:
        if c not in ' ()!':
            tmp += str(c)
        elif c in '()!':
            if len(tmp) > 0:
                token_list.append(tmp)
                tmp = ''
            token_list.append(str(c))
        else:  # c is white space
            if len(tmp) > 0:
                token_list.append(tmp)
                tmp = ''
    if len(tmp) > 0:
        token_list.append(tmp)
    return token_list


def _parse_formula(token_list):
    if token_list[0] in 'FGX!':
        if len(token_list) == 1:
            raise Exception('Error while parsing: solitary LTL operator %s'
                            % token_list[0])
        return LTL(token_list[0], None, _parse_formula(token_list[1:]))
    elif len(token_list) == 1:
        return _parse_atom(token_list)
    else:
        return _parse_orformula(token_list)


def _parse_orformula(token_list):
    left, right, _ = _find_outer('|', token_list)
    if right is None:
        return _parse_andformula(left)
    return LTL('|', _parse_andformula(left), _parse_orformula(right))


def _parse_andformula(token_list):
    left, right, _ = _find_outer('&', token_list)
    if right is None:
        return _parse_uformula(left)
    return LTL('&', _parse_uformula(left), _parse_andformula(right))


def _parse_uformula(token_list):
    left, right, token = _find_outer('UR', token_list)
    if right is None:
        return _parse_atom(left)
    return LTL(token, _parse_atom(left), _parse_atom(right))


def _parse_atom(token_list):
    if len(token_list) == 1:
        return (LTL(token_list[0], None, None))
    last_index = len(token_list) - 1
    if token_list[0] != '(' or token_list[last_index] != ')':
        raise AssertionError('Unexpected atom %s. did you forget parentheses?'
                             % str(token_list))
    return _parse_formula(token_list[1:last_index])


def _find_outer(tokens, token_list):
    """
    This function finds the first occurrence of a token from tokens in
    token_list that is not within parentheses. It returns the partition of
    token_list by this occurrence, meaning that
    result[0] + [token] + result[1] == token_list.
    If there is no such occurrence it returns token_list, None.

    >>> _find_outer('|', ['a', '&', '(', 'b', '|', 'c', ')'])
    (['a', '&', '(', 'b', '|', 'c', ')'], None, None)

    >>> _find_outer('&', ['a', '&', '(', 'b', '|', 'c', ')'])
    (['a'], ['(', 'b', '|', 'c', ')'], '&')
    """
    depth = 0
    for i in range(len(token_list) - 1):
        if depth == 0 and token_list[i] in tokens:
            return (token_list[:i], token_list[i+1:], token_list[i])
        if token_list[i] == '(':
            depth += 1
        if token_list[i] == ')':
            depth -= 1
    return token_list, None, None
