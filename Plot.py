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
        self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])


class PlotResult(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PlotResult()
    w.show()
    app.exec_()