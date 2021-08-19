# -*- coding: utf-8 -*-

import pytest

from bookshelf.skeleton import fib

__author__ = "Mehdi EL KOUHEN"
__copyright__ = "Mehdi EL KOUHEN"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
