from __future__ import print_function, absolute_import

from ctypes import c_int, sizeof
from numba.cuda.cudadrv.driver import driver, host_to_device, device_to_host
from numba.cuda.testing import unittest

ptx1 = '''
    .version 1.4
    .target sm_10, map_f64_to_f32

    .entry _Z10helloworldPi (
    .param .u64 __cudaparm__Z10helloworldPi_A)
    {
    .reg .u32 %r<3>;
    .reg .u64 %rd<6>;
    .loc	14	4	0
$LDWbegin__Z10helloworldPi:
    .loc	14	6	0
    cvt.s32.u16 	%r1, %tid.x;
    ld.param.u64 	%rd1, [__cudaparm__Z10helloworldPi_A];
    cvt.u64.u16 	%rd2, %tid.x;
    mul.lo.u64 	%rd3, %rd2, 4;
    add.u64 	%rd4, %rd1, %rd3;
    st.global.s32 	[%rd4+0], %r1;
    .loc	14	7	0
    exit;
$LDWend__Z10helloworldPi:
    } // _Z10helloworldPi
'''

ptx2 = '''
.version 3.0
.target sm_20
.address_size 64

    .file	1 "/tmp/tmpxft_000012c7_00000000-9_testcuda.cpp3.i"
    .file	2 "testcuda.cu"

.entry _Z10helloworldPi(
    .param .u64 _Z10helloworldPi_param_0
)
{
    .reg .s32 	%r<3>;
    .reg .s64 	%rl<5>;


    ld.param.u64 	%rl1, [_Z10helloworldPi_param_0];
    cvta.to.global.u64 	%rl2, %rl1;
    .loc 2 6 1
    mov.u32 	%r1, %tid.x;
    mul.wide.u32 	%rl3, %r1, 4;
    add.s64 	%rl4, %rl2, %rl3;
    st.global.u32 	[%rl4], %r1;
    .loc 2 7 2
    ret;
}
'''


class TestCudaDriver(unittest.TestCase):
    def setUp(self):
        self.assertTrue(driver.get_device_count())
        device = driver.get_device()
        ccmajor, _ = device.compute_capability
        if ccmajor >= 2:
            self.ptx = ptx2
        else:
            self.ptx = ptx1
        self.context = device.get_or_create_context()

    def test_cuda_driver_basic(self):
        module = self.context.create_module_ptx(self.ptx)
        print(module.info_log)
        function = module.get_function('_Z10helloworldPi')

        array = (c_int * 100)()

        memory = self.context.memalloc(sizeof(array))

        host_to_device(memory, array, sizeof(array))

        function = function.configure((1,), (100,))
        function(memory)

        device_to_host(array, memory, sizeof(array))
        for i, v in enumerate(array):
            self.assertEqual(i, v)

        module.unload()

    def test_cuda_driver_stream(self):
        module = self.context.create_module_ptx(self.ptx)
        print(module.info_log)
        function = module.get_function('_Z10helloworldPi')

        array = (c_int * 100)()

        stream = self.context.create_stream()

        with stream.auto_synchronize():
            memory = self.context.memalloc(sizeof(array))
            host_to_device(memory, array, sizeof(array), stream=stream)

            function = function.configure((1,), (100,), stream=stream)
            function(memory)

        device_to_host(array, memory, sizeof(array), stream=stream)

        for i, v in enumerate(array):
            self.assertEqual(i, v)


if __name__ == '__main__':
    unittest.main()

