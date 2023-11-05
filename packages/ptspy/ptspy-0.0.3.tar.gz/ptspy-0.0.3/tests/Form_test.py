from ptspy import Pt
from ptspy.util import toARGBInt
import numpy as np


def test_toARGBInt():
    c1 = toARGBInt(255, 0, 0, 255)
    c2 = toARGBInt(255, 0, 0)
    c3 = toARGBInt((255, 0, 0))
    c4 = toARGBInt((255, 0, 0, 255))
    c5 = toARGBInt([255, 0, 0, 255])
    c6 = toARGBInt([255, 0, 0])
    c7 = toARGBInt(np.array([255, 0, 0]))
    c8 = toARGBInt(np.array([255, 0, 0, 255]))
    c9 = toARGBInt(0xFF0000FF)
    assert c1 == c2 == c3 == c4 == c5 == c6 == c7 == c8 == c9


def test_toARGBInt_notEqual():
    c1 = toARGBInt(255, 0, 0, 0)
    c2 = toARGBInt(255, 0, 0)
    assert c1 != c2
