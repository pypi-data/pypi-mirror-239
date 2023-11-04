import pytest
import zerohertzPkg


def test_add():
    assert zerohertzPkg.add(2, 3) == 5
    assert zerohertzPkg.add(5, 5) == 10


def test_add_negative():
    assert zerohertzPkg.add(-1, -1) == -2
    assert zerohertzPkg.add(-1, 1) == 0
