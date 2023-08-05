from __future__ import print_function, absolute_import
import numpy as np
from numba import cuda, int32, float32
from numba.cuda.testing import unittest


def useless_sync(ary):
    i = cuda.grid(1)
    cuda.syncthreads()
    ary[i] = i


def simple_smem(ary):
    N = 100
    sm = cuda.shared.array(N, int32)
    i = cuda.grid(1)
    if i == 0:
        for j in range(N):
            sm[j] = j
    cuda.syncthreads()
    ary[i] = sm[i]


def coop_smem2d(ary):
    i, j = cuda.grid(2)
    sm = cuda.shared.array((10, 20), float32)
    sm[i, j] = (i + 1) / (j + 1)
    cuda.syncthreads()
    ary[i, j] = sm[i, j]


def dyn_shared_memory(ary):
    i = cuda.grid(1)
    sm = cuda.shared.array(0, float32)
    sm[i] = i * 2
    cuda.syncthreads()
    ary[i] = sm[i]


class TestCudaSync(unittest.TestCase):
    def test_useless_sync(self):
        compiled = cuda.jit("void(int32[::1])")(useless_sync)
        nelem = 10
        ary = np.empty(nelem, dtype=np.int32)
        exp = np.arange(nelem, dtype=np.int32)
        compiled[1, nelem](ary)
        self.assertTrue(np.all(ary == exp))

    def test_simple_smem(self):
        compiled = cuda.jit("void(int32[::1])")(simple_smem)
        nelem = 100
        ary = np.empty(nelem, dtype=np.int32)
        compiled[1, nelem](ary)
        self.assertTrue(np.all(ary == np.arange(nelem, dtype=np.int32)))

    def test_coop_smem2d(self):
        compiled = cuda.jit("void(float32[:,::1])")(coop_smem2d)
        shape = 10, 20
        ary = np.empty(shape, dtype=np.float32)
        compiled[1, shape](ary)
        exp = np.empty_like(ary)
        for i in range(ary.shape[0]):
            for j in range(ary.shape[1]):
                exp[i, j] = (i + 1) / (j + 1)
        self.assertTrue(np.allclose(ary, exp))

    def test_dyn_shared_memory(self):
        compiled = cuda.jit("void(float32[::1])")(dyn_shared_memory)
        shape = 50
        ary = np.empty(shape, dtype=np.float32)
        compiled[1, shape, 0, ary.size * 4](ary)
        self.assertTrue(np.all(ary == 2 * np.arange(ary.size, dtype=np.int32)))


if __name__ == '__main__':
    unittest.main()
