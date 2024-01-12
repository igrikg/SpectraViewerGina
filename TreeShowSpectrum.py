import sys,os,glob
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from functools import partial


class ShowTreeView(QWidget):
    def __init__(self,parent=None):
        super(ShowTreeView, self).__init__()

        self.tree = QTreeView(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Spectrum','Path'])
        self.tree.setModel(self.model)
        self.tree.setColumnHidden(1,True)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.expandAll()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.tree.customContextMenuRequested.connect(self.openMenu)

    def Update (self):
        pass

    def AddMultiToShowAction(self,listItems):
        pass

    def AddSingleToShowAction(self, listItems):
        pass

    def openMenu(self, position):
            indexes = self.sender().selectedIndexes()
            mdlIdx = self.tree.indexAt(position)
            if not mdlIdx.isValid():
                return
            item = self.model.itemFromIndex(mdlIdx)
            self.__right_click_menu = QMenu()
            if len(indexes) > 1:
                self.__AddMulti = self.__right_click_menu.addAction("Show plot")
                self.__AddMulti.triggered.connect(partial(self.AddMultiToShowAction,indexes))
            else:
                self.__AddMulti = self.__right_click_menu.addAction("Show plot")
                self.__AddMulti.triggered.connect(partial(self.AddMultiToShowAction,indexes))
                self.__AddSingle = self.__right_click_menu.addAction("Show map")
                self.__AddSingle.triggered.connect(partial(self.AddSingleToShowAction, indexes))
            self.__reload = self.__right_click_menu.addAction("Clear")
            self.__reload.triggered.connect(self.Update)
            self.__right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))


    def import_data(self,dataList):
        self.data = dataList
        self.model.setRowCount(0)
        parent=self.model.invisibleRootItem()
        values = deque(self.data)
        while values:
            value = values.popleft()
            SI1 = QStandardItem(value['Name'])
            SI1.setEditable(False)
            SI3 = QStandardItem(value['Path'])
            SI3.setEditable(False)
            parent.appendRow([SI1,SI3])

    def addDataWithUpdate(self, dataList):
        self.data.extend(dataList)



if __name__ == '__main__':
    data=[
        {'Name': 'Spectrum1', 'Path' : "asdasdfasdfasdfasdfasdfasdf"},
        {'Name': 'Spectrum2', 'Path' : "asdfasdsdfsdfdfasdfasdf"},
        {'Name': 'Spectrum3', 'Path' : "asdfsdffasdfasdfasdfasdf"}
    ]
    app = QApplication(sys.argv)
    view = ShowTreeView(data)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())