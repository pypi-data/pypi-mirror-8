#! /usr/bin/env python

from __future__ import absolute_import, division, print_function

import nose
from nose.tools import *
from sknano.core.atoms import XAtom


def test_instantiation():
    from sknano.core.atoms import Atom
    xatom = XAtom()
    assert_is_instance(xatom, (Atom, XAtom))


def test_attributes():
    elements = ['H', 'He', 'B', 'C', 'N', 'O', 'Ar']
    for element in elements:
        xatom = XAtom(element=element)
        assert_equals(xatom.element, element)


if __name__ == '__main__':
    nose.runmodule()
