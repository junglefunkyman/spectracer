from PySide import QtCore
from PySide.QtCore import QObject, Slot, Signal
from abc import ABCMeta, abstractmethod
from pyqtgraph import GraphicsLayoutWidget

import numpy as np

from os import listdir
from os.path import isfile, join


class Plugin:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, dataSourceFactory, chartManager):
        return


class Spectrum:
    def __init__(self, data):
        self.data = data

    def Data(self):
        return self.data


class DataSource(QObject):
    def __init__(self, spectrum, parent=None):
        super(DataSource, self).__init__(parent)
        self.spectrum = spectrum

    updated = Signal(object)

    def getSpectrum(self):
        return self.spectrum

    @Slot()
    def refresh(self):
        self.updated.emit(self.getSpectrum())


class Receiver(QObject):
    def __init__(self, parent=None):
        super(Receiver, self).__init__(parent)

    @Slot(object)
    def onInput(self, spectrum):
        print "Received data: " + spectrum.data.__str__()


class Filter(DataSource, Receiver):
    def filter(self, spectrum):
        return spectrum

    def onInput(self, spectrum):
        # super.onInput(spectrum)
        filtered = self.filter(spectrum)
        self.updated.emit(filtered)


class RandomGenerator(DataSource):
    def __init__(self, interval, parent=None):
        super(RandomGenerator, self).__init__(Spectrum([]), parent)
        self.interval = interval
        self.ptr = 0
        self.xs = np.linspace(1, 100, num=100)
        self.ys = np.random.normal(size=(10, 1000))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.generate)

    def start(self):
        self.timer.start(self.interval)
        print "Starting generator with interval " + self.interval.__str__()

    @Slot()
    def generate(self):
        data = dict(map(lambda x, y: (x, y), self.xs, self.ys[self.ptr % 10]))
        self.spectrum.data = data
        self.ptr += 1
        self.refresh()


class DataSourceFactory(QObject):
    def __init__(self, parent=None):
        super(DataSourceFactory, self).__init__(parent)

    def file(self, filename):
        # TODO parse the file
        return DataSource(Spectrum({1: 500, 2: 600, 3: 550, 4: 580}), self.parent())

    def randomStream(self, interval):
        print 'Creating random stream...\n'
        return RandomGenerator(interval, self.parent())



class Painter(Receiver):
    def __init__(self, chart, parent=None):
        super(Painter, self).__init__(parent)
        self.chart = chart
        self.curve = self.chart.plot(pen='y')

    def onInput(self, spectrum):
        self.curve.setData(list(map(lambda (x, y): y, spectrum.data.iteritems())))


class ChartManager:
    def __init__(self, parent, widget):
        self.parent = parent
        self.widget = widget

    def createChart(self, title):
        chart = self.widget.addPlot(title=title)
        return Painter(chart, self.parent)
