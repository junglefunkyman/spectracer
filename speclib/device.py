import time
import threading

from PySide.QtCore import QThread

from speclib.core import *


class Controller:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect_device(self):
        return

    @abstractmethod
    def close(self):
        return

    @abstractmethod
    def scan(self):
        return

    @abstractmethod
    def isConnected(self):
        return

    @abstractmethod
    def stopMeasurement(self):
        return

    @abstractmethod
    def configure(self, config):
        return

    @abstractmethod
    def getDeviceParameters(self):
        return

    @abstractmethod
    def getCalibration(self):
        return

class DeviceConfig(QObject):
     def __init__(self, integrationTime, numberOfScans, parent=None):
        super(DeviceConfig, self).__init__(parent)
        self.numberOfScans = numberOfScans
        self.integrationTime = integrationTime

class DeviceParameters(QObject):
     def __init__(self, pixels, canProvideCalibration, parent=None):
        super(DeviceParameters, self).__init__(parent)
        self.canProvideCalibration = canProvideCalibration
        self.pixels = pixels

class DeviceReadController:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        return

    @abstractmethod
    def stop(self):
        return

    @abstractmethod
    def read(self):
        return

    @abstractmethod
    def inRun(self):
        return

class M_DeviceManager(DeviceReadController, Controller):
    pass

class DeviceRunTread (QThread):
    def __init__(self, lock, deviceManager):
        super(DeviceRunTread, self).__init__()
        self.deviceManager = deviceManager

    @Slot()
    def stop(self):
        self.stopped = 1

    def run(self):
        self.stopped = 0
        try:
            while self.stopped == 0:
                self.deviceManager.read()
                time.sleep(1)
        except:
            print "Exception occurred"
            self.stop()

class DeviceReadTread (QThread):
    def __init__(self, deviceManager):
        super(DeviceReadTread, self).__init__()
        self.deviceManager = deviceManager

    def run(self):
        self.deviceManager.scan()

class DeviceManager(QObject):
    stoppedSignal = Signal()
    def __init__(self, controller, parent=None):
        super(DeviceManager, self).__init__(parent)
        self.controller = controller
        self.dataSource = controller.dataSource
        self.stopped = 1
        self.lock = threading.Lock()
        self.run_thread = None

    def configure(self, config):
        self.controller.configure(config)

    def run(self):
        # self.lock.acquire()
        self.stopped = 0
        # self.lock.release()
        self.run_thread = DeviceRunTread(self.lock, self)
        # if self.run_thread:
        #     self.stoppedSignal.disconnect(self.run_thread)
        self.stoppedSignal.connect(self.run_thread.stop)
        self.run_thread.start()

    def stop(self):
        self.stoppedSignal.emit()

    def read(self):
        try:
            time.sleep(1)
            self.read_thread = DeviceReadTread(self)
            self.read_thread.start()
        except Exception as e:
            print e.message
            # time.sleep(1)
            if self.inRun():
                print 'Stopping because of an exception'
                self.stop()

    def inRun(self):
        self.lock.acquire()
        stopped = self.stopped
        self.lock.release()
        return not stopped

    # Controller
    def connect_device(self):
        self.controller.connect_device()

    def close(self):
        self.controller.close()

    def scan(self):
        return self.controller.scan()

    def isConnected(self):
        return self.controller.isConnected()

    def stopMeasurement(self):
        self.controller.stopMeasurement()

    def getDeviceParameters(self):
        return self.controller.getDeviceParameters()

    def getCalibration(self):
        return self.controller.getCalibration()

Controller.register(DeviceManager)
DeviceReadController.register(DeviceManager)

class StubController(Controller):
    def __init__(self, parent=None):
        # super(QObject, self).__init__(parent)
        self.dataSource = DataSourceFactory(parent).randomStream(1000)
        self.connected = 0

    def connect_device(self):
        self.connected = 1

    def close(self):
        self.connected = 0

    def scan(self):
        if not self.connected:
            raise Exception('Not connected')
        print "scanning..."
        # time.sleep(1)
        return self.dataSource.generate()

    def isConnected(self):
        return self.connected

    def configure(self, config):
        raise Exception("Not implemented")

    def stopMeasurement(self):
        return

    def getDeviceParameters(self):
        return None

    def getCalibration(self):
        return None