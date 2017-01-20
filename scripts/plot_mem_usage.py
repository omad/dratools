#!/usr/bin/env python3
"""
Display a plot and an image with minimal setup.
"""


import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtGui, QtCore
import psutil
import sys

proc = psutil.Process(int(sys.argv[1]))
proc_name = proc.name()


app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.resize(1000, 600)
win.setWindowTitle('Process memory and CPU usage')
win.show()

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

# Numpy arrays to store the data
mem_usage = np.empty(100)
cpu_usage = np.empty(100)
ptr = 1

# Process RAM Usage
# Use automatic downsampling and clipping to reduce the drawing load
mem_plot = win.addPlot(title="Process RSS (%s)" % proc_name)
mem_plot.setDownsampling(mode='peak')
mem_plot.setClipToView(True)
mem_plot.setLimits(xMax=0)
mem_plot.getAxis('left').setLabel(units='b')
mem_curve = mem_plot.plot()


# Process CPU Usage
win.nextRow()
cpu_plot = win.addPlot(title="Process CPU Usage")
cpu_plot.setDownsampling(mode='peak')
cpu_plot.setClipToView(True)
cpu_plot.setLimits(xMax=0)
cpu_plot.getAxis('left').setLabel(units='%')
cpu_curve = cpu_plot.plot()


def update_stats():
    global mem_usage, cpu_usage, ptr
    try:
        with proc.oneshot():
            mem_usage[ptr] = proc.memory_info().rss

            cpu_usage[ptr] = proc.cpu_percent()
    except psutil.Error:
        timer.stop()
    ptr += 1
    if ptr >= mem_usage.shape[0]:
        tmp = mem_usage
        mem_usage = np.empty(mem_usage.shape[0] * 2)
        mem_usage[:tmp.shape[0]] = tmp

        tmp = cpu_usage
        cpu_usage = np.empty(cpu_usage.shape[0] * 2)
        cpu_usage[:tmp.shape[0]] = tmp


def update_plots():
    mem_curve.setData(mem_usage[:ptr])
    mem_curve.setPos(-ptr, 0)

    cpu_curve.setData(cpu_usage[:ptr])
    cpu_curve.setPos(-ptr, 0)


def update():
    update_stats()
    update_plots()

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
