import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import cm
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import numpy.typing as npt
from DataClass import dataSpec, getScanNames
from matplotlib.widgets import Cursor, RectangleSelector,CheckButtons
import matplotlib.pyplot as plt
import matplotlib.colors as colors



class DataArray():
    def __init__(self, data: npt.NDArray,X=None,Y=None):
        self.Z=data
        if X is None: X = np.arange(-self.Z.shape[0]/2, self.Z.shape[0]/2, 1)
        if Y is None: Y = np.arange(-self.Z.shape[1]/2, self.Z.shape[1]/2, 1)
        self.X, self.Y = np.meshgrid(X, Y)
        self.shape = data.shape
        self.Xminmax = (self.X.min(), self.X.max())
        self.Yminmax = (self.Y.min(), self.Y.max())
        self.Zminmax = (self.Z.min(), self.Z.max())
        self.Xslice=(X,np.sum(self.Z,0))
        self.Yslice=(Y,np.sum(self.Z,1))



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, data, parent=None):
        fig = Figure()
        self.data=DataArray(data)
        super(MplCanvas,self).__init__(fig)
        self.grid = plt.GridSpec(17, 17, hspace=1, wspace=1)
        #self.axes = fig.add_subplot()
        self.axes = fig.add_subplot(self.grid[5:, 5:])
        self.axes_x = fig.add_subplot(self.grid[0:4, 5:15])
        self.axes_y = fig.add_subplot(self.grid[5:, 0:3])
        #Map
        self.surf = self.axes.pcolormesh(self.data.X, self.data.Y, self.data.Z, cmap=cm.jet,
                              linewidth=5, antialiased=False)
        self.center = [
            self.axes.plot((self.data.Xminmax[0],self.data.Xminmax[1]),(0,0),color='cyan',linewidth=1.0),
            self.axes.plot((0,0),(self.data.Yminmax[0],self.data.Yminmax[1]),color='cyan',linewidth=1.0)]
        fig.colorbar(self.surf, ax=self.axes)
        #self.cursor = Cursor(self.axes, useblit=True, color='yellow', linewidth=2)
        self.selector=RectangleSelector(self.axes, self.select_callback,
                useblit=True,
                button=[1, 3],  # disable middle button
                minspanx=5, minspany=5,
                props=dict(facecolor='white', edgecolor='yellow', alpha=1.0, fill=False,linewidth=2),
                spancoords='pixels',
                interactive=True)
        self.mpl_connect('key_press_event', self.toggle_selector)
        # X plot
        self.plot_x = self.axes_x.plot(self.data.Xslice[0],self.data.Xslice[1])
        #  plot
        self.plot_y = self.axes_y.plot(self.data.Yslice[1], self.data.Yslice[0])
        self.axes_y.xaxis.set_inverted(True)
        self.cursor = (Cursor(self.axes_x, useblit=True, color='yellow', linewidth=2),
                       Cursor(self.axes_y, useblit=True, color='yellow', linewidth=2))
        #interactive
        self.axes_CheckBOX = fig.add_subplot(self.grid[0:3, 0:3])
        self.logGraph = [False, False, False]

        self.checkLog = CheckButtons(self.axes_CheckBOX, ["LogMap","LogX","LogY"], [False, False, False])
        self.checkLog.on_clicked(self.logfunc)



    def logfunc(self,label):
        if label == "LogMap":
            if self.logGraph[0]: self.surf.norm = colors.Normalize(vmin = self.data.Zminmax[0],vmax = self.data.Zminmax[1])
            else: self.surf.norm = colors.SymLogNorm(linthresh= 0.003,vmin = self.data.Zminmax[0],vmax = self.data.Zminmax[1])
            self.logGraph[0] = not self.logGraph[0]
        if label == "LogX":
            if self.logGraph[1]: self.axes_x.set_yscale('linear')
            else: self.axes_x.set_yscale('log')
            self.logGraph[1] = not self.logGraph[1]
        if label == "LogY":
            if self.logGraph[2]: self.axes_y.set_xscale('linear')
            else: self.axes_y.set_xscale('log')
            self.logGraph[2] = not self.logGraph[2]
        self.draw()

    def select_callback(self, eclick, erelease):
        """
        Callback for line selection.

        *eclick* and *erelease* are the press and release events.
        """
        self.selector_x1, self.selector_y1 = eclick.xdata, eclick.ydata
        self.selector_x2, self.selector_y2 = erelease.xdata, erelease.ydata
        self.selector_width = self.selector_x2 - self.selector_x1
        self.selector_heigth = self.selector_y2 - self.selector_y1

        self.selector_center_x = self.selector_width/2 + self.selector_x1
        self.selector_center_y = self.selector_heigth/2 + self.selector_y1

    def toggle_selector(self, event):
        print('Key pressed.')
        if event.key == 't':
            if self.selector.active:
                self.selector.set_active(False)
            else:
                self.selector.set_active(True)










class Plot2DWidget(QtWidgets.QWidget):

    def __init__(self, data):
        super(Plot2DWidget, self).__init__()
        self.canvas = MplCanvas(data,self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.show()

if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    import platform, os
    if platform.system() == 'Windows':
            DirPath = os.getcwd() + "/data/"
    else:
            DirPath = '~/Documents/GinaSpectrum/'

    ScanList = getScanNames(DirPath)
    a = dataSpec(DirPath, ScanList[0])
    a.update()
    ScanList = getScanNames(DirPath)
    ScanData = dataSpec(DirPath, "Spectrum_3266857")
    ARRAY=ScanData.ResultSpectra[0];
    w = Plot2DWidget(ARRAY)
    app.exec_()