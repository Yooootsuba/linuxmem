import os
import ctypes


buffers = {
    'uint8'  : ctypes.c_uint8(),
    'uint16' : ctypes.c_uint16(),
    'uint32' : ctypes.c_uint32(),
    'uint64' : ctypes.c_uint64(),

    'int8'   : ctypes.c_int8(),
    'int16'  : ctypes.c_int16(),
    'int32'  : ctypes.c_int32(),
    'int64'  : ctypes.c_int64(),

    'float'  : ctypes.c_float(),
    'double' : ctypes.c_double(),
}


libc = ctypes.CDLL('libc.so.6')


class Memory:

    def __init__(self, pid):
        self.pid        = pid
        self.mem_handle = self.get_mem_handle()


    def get_mem_handle(self):
        return os.open(f'/proc/{self.pid}/mem', os.O_RDWR)


    def read(self, address, ctype):
        libc.pread(
            self.mem_handle,
            ctypes.pointer(buffers[ctype]),
            ctypes.sizeof(buffers[ctype]),
            ctypes.c_int64(address)
        )

        return buffers[ctype].value


    def write(self, address, ctype, value):
        buffers[ctype].value = value

        libc.pwrite(
            self.mem_handle,
            ctypes.pointer(buffers[ctype]),
            ctypes.sizeof(buffers[ctype]),
            ctypes.c_int64(address)
        )
