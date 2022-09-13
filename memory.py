import re
import os
import ctypes


from .process import get_process_id_by_name


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

    def __init__(self, process_name):
        self.process_name = process_name
        self.process_id   = get_process_id_by_name(process_name)
        self.mem_handle   = self.get_mem_handle()


    def get_mem_handle(self):
        return os.open(f'/proc/{self.process_id}/mem', os.O_RDWR)


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


    def read_pointer(self, address, offsets, ctype = 'int64'):
        for offset in offsets:
            address = self.read(address + offset, ctype)

        return address


    def get_module_base_address(self, module_name):
        pattern = f'([0-9a-f]+)-([0-9a-f]+)(.*{module_name}.*)'

        with open(f'/proc/{self.process_id}/maps', 'r') as f:
            for line in f.readlines():
                if (match := re.match(pattern, line)) != None:
                    return int(match.group(1), base = 16)


    def get_base_address(self):
        return self.get_module_base_address(self.process_name)
