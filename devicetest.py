# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:13:35 2015

@author: funkyman
"""

from speclib.device import StubController
from speclib.device import DeviceManager
m = DeviceManager(StubController(context))

chart = add_spec()
p = chart.addPlot("Plot 1")
m.controller.connect_device()
m.controller.dataSource.updated.connect(p.onInput)
m.run()