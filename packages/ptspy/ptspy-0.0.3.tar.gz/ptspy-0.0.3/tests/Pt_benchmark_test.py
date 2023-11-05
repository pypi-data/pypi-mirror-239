import pytest
from ptspy import Pt
import numpy as np


@pytest.mark.benchmark(group="addition")
def test_benchmark_pt_addition(benchmark):
    pt1 = Pt(np.random.rand(10))
    pt2 = Pt(np.random.rand(10))
    benchmark(pt1.add_, pt2)


@pytest.mark.benchmark(group="addition")
def test_benchmark_np_addition(benchmark):
    np1 = np.random.rand(10)
    np2 = np.random.rand(10)
    benchmark(np.add, np1, np2)


@pytest.mark.benchmark(group="addition")
def test_benchmark_pt_np_addition(benchmark):
    pt1 = Pt(np.random.rand(10))
    np2 = np.random.rand(10)
    benchmark(pt1.add_, np2)


# @pytest.mark.benchmark(group="addition")
# def test_benchmark_pt_var_addition(benchmark):
#     pt1 = Pt(np.random.rand(10))
#     benchmark(pt1.add_, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
