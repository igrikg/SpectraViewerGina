import sys
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib import cm
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

from DataClass import dataSpec, getScanNames, DataArray
from matplotlib.widgets import Cursor, RectangleSelector,CheckButtons
import matplotlib.pyplot as plt
import matplotlib.colors as colors



class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, data=None, parent=None):
        fig = Figure()
        if data is None:
            data = np.zeros((145,145))
        self.XrecalcValue=2.0
        self.YrecalcValue = 4.0
        self.parent = parent
        self.data = DataArray(data)
        super(MplCanvas, self).__init__(fig)
        self.grid = plt.GridSpec(17, 17, hspace=0.2, wspace=1)
        #self.axes = fig.add_subplot()
        self.axes = fig.add_subplot(self.grid[5:, 5:])
        self.axes_x = fig.add_subplot(self.grid[0:4, 5:15])
        self.axes_y = fig.add_subplot(self.grid[5:, 0:3])
        #Map

        self.surf = self.axes.pcolormesh(self.data.X, self.data.Y, self.data.Z, cmap=cm.rainbow,
                              linewidth=5, antialiased=False)
        self.center = [
            self.axes.plot((self.data.Xminmax[0],self.data.Xminmax[1]),(0,0),color='cyan',linewidth=1.0),
            self.axes.plot((0,0),(self.data.Yminmax[0],self.data.Yminmax[1]),color='cyan',linewidth=1.0)]
        self.colorbar=self.figure.colorbar(self.surf, ax=self.axes)
        self.selector=RectangleSelector(self.axes, self.select_callback,
                useblit=True,
                button=[1, 3],  # disable middle button
                minspanx=5, minspany=5,
                props=dict(facecolor='white', edgecolor='yellow', alpha=1.0, fill=False,linewidth=2),
                spancoords='pixels',
                interactive=True,
                use_data_coordinates=True, drawtype='box')
        self.RectangleSelectorCordinats = [0, 0, 0, 0]
        self.__RectangleSelectorCordinats = [0, 0, 0, 0]
        self.drawRectangleSelector()


        # X plot
        self.plot_x = self.axes_x.plot(self.data.Xslice[0],self.data.Xslice[1])
        self.plot_y = self.axes_y.plot(self.data.Yslice[1], self.data.Yslice[0])
        self.axes_y.xaxis.set_inverted(True)
        self.cursor = (Cursor(self.axes_x, useblit=True, color='yellow', linewidth=2),
                       Cursor(self.axes_y, useblit=True, color='yellow', linewidth=2))
        #interactive
        self.axes_CheckBOX = fig.add_subplot(self.grid[0:5, 0:3])
        self.logGraph = [False, False, False]
        self.checkLog = CheckButtons(self.axes_CheckBOX, ["LogMap","LogX","LogY"], [False, False, False])
        self.checkLog.on_clicked(self.logfunc)


    def connectToSpinbox(self):
        if not self.parent is None:
            self.parent.toolbar.Xleft.valueChanged.connect(self.changeDspinChanges)
            self.parent.toolbar.Xrigth.valueChanged.connect(self.changeDspinChanges)
            self.parent.toolbar.Yleft.valueChanged.connect(self.changeDspinChanges)
            self.parent.toolbar.Yrigth.valueChanged.connect(self.changeDspinChanges)
            self.parent.toolbar.binaryCheckBox.stateChanged.connect(self.binaryMode)
            self.parent.toolbar.XrecToDegCheckBox.stateChanged.connect(self.useDecalculate)
            self.parent.toolbar.YrecToDegCheckBox.stateChanged.connect(self.useDecalculate)

    def useDecalculate(self):

        if self.parent.toolbar.XrecToDegCheckBox.isChecked():
            XrecValue = self.XrecalcValue
            # copy to saving x
            self.__RectangleSelectorCordinats[0] = self.RectangleSelectorCordinats[0]
            self.__RectangleSelectorCordinats[1] = self.RectangleSelectorCordinats[1]
            self.RectangleSelectorCordinats[0] = self.RectangleSelectorCordinats[0] * XrecValue
            self.RectangleSelectorCordinats[1] = self.RectangleSelectorCordinats[1] * XrecValue
        else:
            XrecValue = None
            if self.sender() == self.parent.toolbar.XrecToDegCheckBox:
                if self.RectangleSelectorCordinats[0] == self.__RectangleSelectorCordinats[0] * self.XrecalcValue:
                    self.RectangleSelectorCordinats[0] = self.__RectangleSelectorCordinats[0]
                else:
                    self.RectangleSelectorCordinats[0] = self.RectangleSelectorCordinats[0] / self.XrecalcValue

                if self.RectangleSelectorCordinats[1] == self.__RectangleSelectorCordinats[1] * self.XrecalcValue:
                    self.RectangleSelectorCordinats[1] = self.__RectangleSelectorCordinats[1]
                else:
                    self.RectangleSelectorCordinats[1] = self.RectangleSelectorCordinats[1] / self.XrecalcValue

        if self.parent.toolbar.YrecToDegCheckBox.isChecked():
            YrecValue = self.YrecalcValue
            # copy to saving y
            self.__RectangleSelectorCordinats[2] = self.RectangleSelectorCordinats[2]
            self.__RectangleSelectorCordinats[3] = self.RectangleSelectorCordinats[3]
            self.RectangleSelectorCordinats[2] = self.RectangleSelectorCordinats[2] * YrecValue
            self.RectangleSelectorCordinats[3] = self.RectangleSelectorCordinats[3] * YrecValue
        else:
            if self.sender() == self.parent.toolbar.YrecToDegCheckBox:
                if self.RectangleSelectorCordinats[2] == self.__RectangleSelectorCordinats[2]*self.YrecalcValue:
                    self.RectangleSelectorCordinats[2] = self.__RectangleSelectorCordinats[2]
                else:
                    self.RectangleSelectorCordinats[2] = self.RectangleSelectorCordinats[2]/self.YrecalcValue
                if self.RectangleSelectorCordinats[3] == self.__RectangleSelectorCordinats[3]*self.YrecalcValue:
                    self.RectangleSelectorCordinats[3] = self.__RectangleSelectorCordinats[3]
                else:
                    self.RectangleSelectorCordinats[3] = self.RectangleSelectorCordinats[3]/self.YrecalcValue

            YrecValue = None
        self.data.recalculationXY(XrecValue,YrecValue)
        self.setRectangeSelector(self.RectangleSelectorCordinats)
        self.ShowData()



    def changeDspinChanges(self):
        listspinbox = [self.parent.toolbar.Xleft, self.parent.toolbar.Xrigth,
                       self.parent.toolbar.Yleft, self.parent.toolbar.Yrigth]
        self.RectangleSelectorCordinats[listspinbox.index(self.sender())]=self.sender().value()
        self.drawRectangleSelector()

    def changeRectangeSelectorByMouse(self):
        if not self.parent is None:
            self.parent.toolbar.Xleft.setValue(self.RectangleSelectorCordinats[0])
            self.parent.toolbar.Xrigth.setValue(self.RectangleSelectorCordinats[1])
            self.parent.toolbar.Yleft.setValue(self.RectangleSelectorCordinats[2])
            self.parent.toolbar.Yrigth.setValue(self.RectangleSelectorCordinats[3])

    def setRectangeSelector(self,RectangleSelectorCordinats):
        self.RectangleSelectorCordinats=RectangleSelectorCordinats
        self.changeRectangeSelectorByMouse()

    def drawRectangleSelector(self):
        x1, x2, y1, y2 = self.RectangleSelectorCordinats
        x1, x2 = sorted([round(x1,2), round(x2,2)])
        y1, y2 = sorted([round(y1,2), round(y2,2)])
        width = x2 - x1
        heigth = y2 - y1
        xc = x1 + width/2
        yc = y1 + heigth/2
        self.selector._draw_shape([x1,x2,y1,y2])
        self.selector._corner_handles.set_data([[x1, x1, x2, x2], [y1, y2, y2, y1]])
        self.selector._edge_handles.set_data([[x1, xc, x2, xc], [yc, y2, yc, y1]])
        self.selector._center_handle.set_data([xc, yc])
        self.selector.set_visible(True)
        self.selector.set_active(True)

    def ShowData(self,data=None):
        if not data is None:
            self.data = DataArray(data)
        self.axes.clear()
        self.surf = self.axes.pcolormesh(self.data.X, self.data.Y, self.data.Z, cmap=cm.rainbow,
                                                 linewidth=5, antialiased=False)
        self.center = [
            self.axes.plot((self.data.Xminmax[0], self.data.Xminmax[1]), (0, 0), color='cyan', linewidth=1.0),
            self.axes.plot((0, 0), (self.data.Yminmax[0], self.data.Yminmax[1]), color='cyan', linewidth=1.0)]
        self.axes_x.clear()
        self.plot_x = self.axes_x.plot(self.data.Xslice[0], self.data.Xslice[1])
        self.axes_y.clear()
        self.plot_y = self.axes_y.plot(self.data.Yslice[1], self.data.Yslice[0])
        self.axes_y.xaxis.set_inverted(True)
        self.logGraph = [False, False, False]

        for i, status in enumerate(self.checkLog.get_status()):
           if status:
               self.checkLog.set_active(i)
        self.colorbar.update_normal(self.surf)
        self.drawRectangleSelector()
        self.draw()
    def getRangeSum(self):
        Xindex = np.argwhere(np.logical_and(self.data.X[0] >= self.RectangleSelectorCordinats[0],
                                            self.data.X[0] <= self.RectangleSelectorCordinats[1]))
        Yindex = np.argwhere(np.logical_and(np.transpose(self.data.Y)[0] >= self.RectangleSelectorCordinats[2],
                                            np.transpose(self.data.Y)[0] <= self.RectangleSelectorCordinats[3]))

        return [Xindex[0][0],Xindex[-1][0], Yindex[0][0],Yindex[-1][0]]


    def binaryMode(self):
            if self.sender().isChecked():
                self.surf = self.axes.pcolormesh(self.data.X, self.data.Y, (self.data.Z>0).astype(int), cmap=cm.gray,
                                             linewidth=5, antialiased=False)
            else:
                self.surf = self.axes.pcolormesh(self.data.X, self.data.Y, self.data.Z, cmap=cm.rainbow,
                                                 linewidth=5, antialiased=False)
                self.logGraph[0]= not self.logGraph[0]
                self.logfunc("LogMap")
            self.draw()

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
        self.selector_x1, self.selector_y1 = eclick.xdata, eclick.ydata
        self.selector_x2, self.selector_y2 = erelease.xdata, erelease.ydata
        self.selector_width = self.selector_x2 - self.selector_x1
        self.selector_heigth = self.selector_y2 - self.selector_y1
        self.selector_center_x = self.selector_width/2 + self.selector_x1
        self.selector_center_y = self.selector_heigth/2 + self.selector_y1
        self.RectangleSelectorCordinats = [round(self.selector_x1,2),round(self.selector_x2,2),round(self.selector_y1,2),round(self.selector_y2,2)]
        self.changeRectangeSelectorByMouse()


class MyQLineEdit(QtWidgets.QDoubleSpinBox):
    def __init__(self):
        QtWidgets.QDoubleSpinBox.__init__(self)
        self.setRange(-100,100)
        self.setDecimals(2)

class MyNavigationToolbar(NavigationToolbar):
    def __init__(self, plotCanvas,parent=None):
        NavigationToolbar.__init__(self,plotCanvas, parent)
        Label1=QtWidgets.QLabel("X left:")
        Label2 = QtWidgets.QLabel("X rigth:")
        Label3 = QtWidgets.QLabel("Y left:")
        Label4 = QtWidgets.QLabel("Y rigth:")

        self.Xleft = MyQLineEdit()
        self.Xrigth = MyQLineEdit()
        self.Yleft = MyQLineEdit()
        self.Yrigth = MyQLineEdit()
        self.binaryCheckBox = QtWidgets.QCheckBox("Binary")
        self.XrecToDegCheckBox = QtWidgets.QCheckBox("XToDeg")
        self.YrecToDegCheckBox = QtWidgets.QCheckBox("YToDeg")
        self.addWidget(Label1)
        self.addWidget(self.Xleft)
        self.addWidget(Label2)
        self.addWidget(self.Xrigth)
        self.addWidget(Label3)
        self.addWidget(self.Yleft)
        self.addWidget(Label4)
        self.addWidget(self.Yrigth)
        self.addWidget(self.binaryCheckBox)
        self.addWidget(self.XrecToDegCheckBox)
        self.addWidget(self.YrecToDegCheckBox)



class ChangeNumberOfSpectraWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ChangeNumberOfSpectraWidget, self).__init__()
        self.SliderSpectra = QtWidgets.QSlider(self, orientation = QtCore.Qt.Orientation.Horizontal)
        self.LeftButton = QtWidgets.QPushButton("<", self)
        self.RigthButton = QtWidgets.QPushButton(">", self)
        self.NumberSpectra = QtWidgets.QSpinBox(self)
        self.LabelValue = QtWidgets.QLabel("ROI:", self)
        self.ValueOffSpectra = QtWidgets.QLineEdit("ROI", self)

        self.ValueOffSpectra.setEnabled(False)
        self.ValueOffSpectra.setMaximumWidth(50)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.LeftButton)
        layout.addWidget(self.SliderSpectra)
        layout.addWidget(self.RigthButton)
        layout.addWidget(self.NumberSpectra)
        layout.addWidget(self.LabelValue)
        layout.addWidget(self.ValueOffSpectra)
        self.setLayout(layout)
        self.setNumberOfSpectra(0)

    def setNumberOfSpectra(self, Number):
        self.SliderSpectra.setMaximum(Number)
        self.SliderSpectra.setMinimum(0)
        self.NumberSpectra.setMinimum(0)
        self.NumberSpectra.setMaximum(Number)
        self.SliderSpectra.setMinimum(0)




class Plot2DWidget(QtWidgets.QWidget):

    def __init__(self, data=None):
        super(Plot2DWidget, self).__init__()
        self.canvas = MplCanvas(data,self)
        self.toolbar = MyNavigationToolbar(self.canvas, self)
        self.canvas.connectToSpinbox()
        self.toolbarScanSpectra = ChangeNumberOfSpectraWidget(self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbarScanSpectra)
        self.setLayout(layout)
        self.data = data
        self.dataListNumber = []



        self.toolbarScanSpectra.NumberSpectra.valueChanged.connect(self.shangeNumber)
        self.toolbarScanSpectra.SliderSpectra.valueChanged.connect(self.sliderMove)
        self.toolbarScanSpectra.LeftButton.clicked.connect(self.pushLeftButton)
        self.toolbarScanSpectra.RigthButton.clicked.connect(self.pushRigthButton)

    def ShowDataSpectrums(self, data):
        self.data = data
        self.dataListScan = data.getListOfFirstColums()
        self.NameColums= data.getListOfScanColums()
        self.updateNumberOfSpectrum()
        self.showNextSpectrum(0)

    def updateNumberOfSpectrum(self):
        if len(self.NameColums)==1:
            self.toolbarScanSpectra.LabelValue.setText("ROI")
            self.toolbarScanSpectra.ValueOffSpectra.setText("OK")
            self.toolbarScanSpectra.setNumberOfSpectra(0)

        else:
            self.toolbarScanSpectra.setNumberOfSpectra(len(self.dataListScan)-1)
            self.toolbarScanSpectra.LabelValue.setText(self.NameColums[0])
            self.toolbarScanSpectra.ValueOffSpectra.setText(str(self.dataListScan[0]))
        self.toolbarScanSpectra.SliderSpectra.setValue(0)
        self.toolbarScanSpectra.NumberSpectra.setValue(0)

    def showNextSpectrum(self, Number):
        self.ShowSingleData(self.data.ResultSpectra[Number])
        self.toolbarScanSpectra.ValueOffSpectra.setText(str(self.dataListScan[Number]))

    def pushLeftButton(self):
        value = self.toolbarScanSpectra.SliderSpectra.value() - 1
        if value >= self.toolbarScanSpectra.SliderSpectra.minimum():
            self.toolbarScanSpectra.SliderSpectra.setValue(value)

    def pushRigthButton(self):
        value = self.toolbarScanSpectra.SliderSpectra.value()+1
        if value<=self.toolbarScanSpectra.SliderSpectra.maximum():
            self.toolbarScanSpectra.SliderSpectra.setValue(value)

    def shangeNumber(self):
        self.toolbarScanSpectra.SliderSpectra.setValue(self.toolbarScanSpectra.NumberSpectra.value())

    def sliderMove(self):
        value = self.toolbarScanSpectra.SliderSpectra.value()
        self.showNextSpectrum(value)
        self.toolbarScanSpectra.NumberSpectra.setValue(value)






    def ShowSingleData(self, data):
        self.canvas.ShowData(data)






import traceback

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
sys.excepthook = excepthook


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
    ScanData = dataSpec(DirPath, "Spectrum_3277570")
    ARRAY=ScanData.ResultSpectra[0]
    w = Plot2DWidget()
    w.ShowDataSpectrums(a)
    w.show()
    app.exec_()