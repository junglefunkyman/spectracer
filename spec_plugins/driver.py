from ctypes import cdll, c_void_p
import numpy as np
from speclib.core import DataSource

from speclib.device import Controller

lib = cdll.LoadLibrary('./spec_plugins/libdriver.so')
lib.Driver_read.argtypes = [c_void_p]

class Driver(Controller):
    def __init__(self, context):
        self.obj = lib.Driver_new()
        self.connected = 0
        self.dataSource = DataSource(context)
        self.size = 1024

    def connect_device(self):
        lib.Driver_connect(self.obj)
        self.connected = 1

    def scan(self):
        if not self.connected:
            raise Exception('Not connected')
        print "scanning..."
        data = np.ones(self.size, dtype=np.int32)
        lib.Driver_read(self.obj, data.ctypes, self.size)
        print data
        self.dataSource.spectrum.data = dict(enumerate(data.tolist()))
        self.dataSource.refresh()

    def close(self):
        self.connected = 0

    def isConnected(self):
        return self.connected

    def configure(self, config):
        raise Exception("Not implemented")

    def stopMeasurement(self):
        pass

    def getDeviceParameters(self):
        pass

    def getCalibration(self):
        pass