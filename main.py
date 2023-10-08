import os.path
import toml
from DataClass import dataSpec
from Tree import view
from TreeShowSpectrum import ShowTreeView
from PLot2dWidget import Plot2DWidget
from Plot import PlotResult
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        with open('config.toml', 'r') as f:
            self.configDict = toml.load(f)
        self.TreeWidget = view(self.configDict["Path"]["FolderSpectra"], self)
        self.ShowTreeWidget = ShowTreeView()
        self.PlotMapWidget = Plot2DWidget()
        self.PlotMapWidget.canvas.setRectangeSelector(list(map(lambda x: float(x), self.configDict["SumRange"]["SpectraSignal"])))
        self.PlotMapWidget.canvas.XrecalcValue = self.configDict["Detector"]["XtoDeg"]
        self.PlotMapWidget.canvas.YrecalcValue = self.configDict["Detector"]["YtoDeg"]
        self.PlotResultWidget = PlotResult()
        grid = QGridLayout()
        self.setLayout(grid)
        self.TreeWidget.setMaximumWidth(400)
        self.ShowTreeWidget.setMaximumWidth(400)
        grid.addWidget(self.TreeWidget,0,0,1,1)
        grid.addWidget(self.ShowTreeWidget,1,0,1,1)
        grid.addWidget(self.PlotMapWidget,0,1,1,5)
        grid.addWidget(self.PlotResultWidget,1,1,1,5)


        self.setWindowTitle("Gina Spectrum")


        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.startTimer()
        self.show()

    def closeEvent(self, event):
        if not self.PlotMapWidget.canvas.RectangleSelectorCordinats is [0, 0, 0, 0]:
            self.PlotMapWidget.toolbar.XrecToDegCheckBox.setCheckState(False)
            self.PlotMapWidget.toolbar.YrecToDegCheckBox.setCheckState(False)
            self.configDict["SumRange"]["SpectraSignal"] = \
                list(map(lambda x: str(x), self.PlotMapWidget.canvas.RectangleSelectorCordinats))

        with open('config.toml', 'w') as f:
            toml.dump(self.configDict, f)
        event.accept()

    def doubleClickAction(self, dataList):
        self.ShowTreeWidget.importData(dataList)
        self.listDataClass=[]
        for line in dataList:
            self.listDataClass.append(dataSpec(os.path.dirname(line['Path']), line['Name']))
        self.PlotMapWidget.ShowDataSpectrums(self.listDataClass[0])
        self.PlotResultWidget.clear()
        for Spectra in self.listDataClass:
            plots1d=Spectra.getSumPlot(self.PlotMapWidget.canvas.getRangeSum())

            self.PlotResultWidget.showPlots(plots1d,Spectra.ScanName)


    def updateTimer(self):
        self.TreeWidget.Update()

    def startTimer(self):
        self.timer.start(1000)
    def endTimer(self):
        self.timer.stop()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
