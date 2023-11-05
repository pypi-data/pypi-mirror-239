# Writing pytest test cases for the Pt class
import pytest
from ptspy import Pt
import numpy as np


# Test Pt constructor and basic add operation with various data types
@pytest.mark.parametrize(
    "pt1, pt2, expected",
    [
        (Pt(1, 2, 3), Pt(4, 5, 6), Pt([5, 7, 9])),
        (Pt(1, 2, 3), [4, 5, 6], Pt([5, 7, 9])),
        (Pt(1, 2, 3), (4, 5, 6), Pt([5, 7, 9])),
        (Pt(1, 2, 3), 3, Pt([4, 5, 6])),
        (Pt(1, 2, 3), np.array([4, 5, 6]), Pt([5, 7, 9])),
    ],
)
def test_add(pt1, pt2, expected):
    assert pt1.add(pt2).__repr__() == expected.__repr__()


# Test Pt with numpy functions that return scalar values
@pytest.mark.parametrize(
    "pt, expected",
    [
        (Pt([1, 2, 3]), 2.0),
    ],
)
def test_numpy_scalar(pt, expected):
    assert np.mean(pt) == expected


# Test Pt with numpy functions that return array values
@pytest.mark.parametrize(
    "pt, expected",
    [
        (Pt([1, 2, 3]), Pt([2, 4, 6])),
    ],
)
def test_numpy_array(pt, expected):
    assert np.multiply(pt, 2).__repr__() == expected.__repr__()


# Additional edge case: Pt with zero dimensions
def test_zero_dimensions():
    pt = Pt([])
    assert pt.add(3).__repr__() == Pt([]).__repr__()


# Additional edge case: Pt with high dimensions
def test_high_dimensions():
    pt = Pt(np.ones((3, 3, 3)))
    result = pt.add(np.ones((3, 3, 3)))
    expected = Pt(np.ones((3, 3, 3)) * 2)
    assert result.__repr__() == expected.__repr__()
