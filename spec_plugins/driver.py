from ctypes import cdll

from speclib.core import

lib = cdll.LoadLibrary('./spec_plugins/libdriver.so')

class Driver(object):
    def __init__(self):
        self.obj = lib.Driver_new()

    def connect(self):
        lib.Driver_connect(self.obj)

    def read(self):
        return lib.Driver_read(self.obj)