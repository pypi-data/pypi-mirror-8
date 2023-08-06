#! /usr/bin/env python

from __future__ import absolute_import, division, print_function

import nose
from nose.tools import *
from sknano.core.atoms import POAVAtom


def test_instantiation():
    from sknano.core.atoms import Atom, XAtom, KDTAtom
    atom = POAVAtom()
    assert_is_instance(atom, (Atom, XAtom, KDTAtom, POAVAtom))


def test_attributes():
    elements = ['H', 'He', 'B', 'C', 'N', 'O', 'Ar']
    for element in elements:
        atom = POAVAtom(element=element)
        assert_equals(atom.element, element)


if __name__ == '__main__':
    nose.runmodule()
