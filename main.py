import os.path

import numpy as np
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
        mailVLayout = QVBoxLayout(self)
        firstHLayout = QHBoxLayout(self)

        firstHLayout.addWidget(self.TreeWidget)

        firstHLayout.addWidget(self.PlotMapWidget)
        mailVLayout.addLayout(firstHLayout)
        self.setWindowTitle("Hello World")
        self.setLayout(mailVLayout)
        mailVLayout.addWidget(self.PlotResultWidget)
        mailVLayout.addWidget(self.ShowTreeWidget)
        self.show()

    def closeEvent(self, event):

        if not self.PlotMapWidget.canvas.RectangleSelectorCordinats is [0, 0, 0, 0]:
            self.configDict["SumRange"]["SpectraSignal"] = self.PlotMapWidget.canvas.RectangleSelectorCordinats
        with open('config.toml', 'w') as f:
            toml.dump(self.configDict, f)
        event.accept()

    def doubleClickAction(self, dataList):
        self.ShowTreeWidget.importData(dataList)
        self.listDataClass=[]
        for line in dataList:
            self.listDataClass.append(dataSpec(os.path.dirname(line['Path']), line['Name']))
        self.PlotMapWidget.ShowDataSpectrums(self.listDataClass[0])




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
