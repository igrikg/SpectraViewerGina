import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from matplotlib.widgets import Cursor, RectangleSelector
import matplotlib.pyplot as plt
import matplotlib.colors as colors


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        fig = Figure()
        super(MplCanvas, self).__init__(fig)
        self.axes = fig.add_subplot(111)

    def clear(self):
        self.axes.clear()

class PlotResult(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    def showPlot(self,data):
        self.canvas.axes.plot(data)

        self.canvas.draw()
    def clear(self):
        self.canvas.clear()


    def showPlots(self,listData,label):
        for data in listData:
            if data[0].shape[0]==1: continue
            self.canvas.axes.plot(data[0], data[1],label=label)
            self.canvas.axes.legend()
            self.canvas.draw()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PlotResult()
    w.show()
    app.exec_()