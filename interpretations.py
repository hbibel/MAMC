# -*- coding: utf-8 -*-

from rectangle import Rectangle


def interpretation(ap):
    if ap.startswith('goal'):
        return Rectangle(10.0, (1.0, 0.0), (0.0, 1.0), 3.0, 3.0)
    if ap.startswith('obstacle'):
        return Rectangle(2.0, (1.0, 0.0), (0.0, 1.0), 2.0, 1.0)
    return None
