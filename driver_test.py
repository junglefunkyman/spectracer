# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:33:16 2015

@author: funkyman
"""

from spec_plugins.driver import Driver
d = Driver(context)
d.connect_device()

chart = add_spec()
p = chart.addPlot("Plot 1")
d.dataSource.updated.connect(p.onInput)

d.scan()