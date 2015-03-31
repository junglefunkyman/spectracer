# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:10:06 2015

@author: funkyman
"""
for s in specs:
    spectracer.remove_spec(s)
chart1 = add_spec()
origChart = chart1.addPlot("Original spectrum")
source = dataSourceFactory.randomStream(1000)
source.updated.connect(origChart.onInput)
source.start()

chart2 = add_spec()
p1 = chart2.addPlot("Plot 1")
p2 = chart2.addPlot("Plot 2")
source.updated.connect(p1.onInput)

# source.timer.stop()