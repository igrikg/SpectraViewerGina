from matplotlib.widgets import EllipseSelector, RectangleSelector
import numpy as np
import matplotlib.pyplot as plt
import sys,os,glob
import matplotlib
matplotlib.use('Qt5Agg')
from DataClass import dataSpec, getScanNames
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])


class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        toolbar = NavigationToolbar(sc, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        self.setLayout(layout)
        self.show()
dirPath=os.getcwd()+"/data/"
listScanfile=getScanNames(dirPath)
a=dataSpec(dirPath,listScanfile[0])
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()