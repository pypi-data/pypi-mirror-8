from __future__ import print_function
from numba.ctypes_support import *
import numpy
import numba.unittest_support as unittest
from numba._helperlib import c_helpers


class ArrayStruct3D(Structure):
    # Mimick the structure defined in numba.targets.arrayobj's make_array()
    _fields_ = [
        ("data", c_void_p),
        ("shape", (c_ssize_t * 3)),
        ("strides", (c_ssize_t * 3)),
        ("parent", c_void_p),
    ]


class TestArrayAdaptor(unittest.TestCase):
    def test_array_adaptor(self):
        arystruct = ArrayStruct3D()

        adaptorptr = c_helpers['adapt_ndarray']
        adaptor = PYFUNCTYPE(c_int, py_object, c_void_p)(adaptorptr)

        ary = numpy.arange(60).reshape(2, 3, 10)
        status = adaptor(ary, byref(arystruct))
        self.assertEqual(status, 0)
        self.assertEqual(arystruct.data, ary.ctypes.data)
        for i in range(3):
            self.assertEqual(arystruct.shape[i], ary.ctypes.shape[i])
            self.assertEqual(arystruct.strides[i], ary.ctypes.strides[i])

if __name__ == '__main__':
    unittest.main()
