import sys,os,glob
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from functools import partial
icons={'folder':'./icons/folder.png','file':'./icons/spectrum.png'}

class StandardItem(QStandardItem):
    def __init__(self, txt='', image_path=''):
        super().__init__()
        self.setEditable(False)
        self.setText(txt)
        if image_path:
            image = QImage(image_path)
            image.size()
            self.setData(image, Qt.DecorationRole)
class view(QWidget):
    def __init__(self, dirPath):
        super(view, self).__init__()
        self.dirPath=dirPath
        self.data = []
        self.tree = QTreeView(self)
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Spectrums','Date','Path'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.tree.setColumnHidden(2,True)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.label.setText(self.dirPath)
        self.__getScanNames()
        self.importData()
        self.tree.expandAll()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.reload = QAction(self)
        self.reload.setText("ReLoad")
        self.doubleClickAction =QAction(self)

        #self.tree.doubleClicked.connect(self.doubleClickAction)
    def Update (self):
        pass
    def AddMultiToShowAction(self,listItems):
        pass

    def openMenu(self, position):
            indexes = self.sender().selectedIndexes()
            mdlIdx = self.tree.indexAt(position)

            if not mdlIdx.isValid():
                return
            item = self.model.itemFromIndex(mdlIdx)

            if len(indexes) > 0:
                level = 0
                index = indexes[0]
                while index.parent().isValid():
                    index = index.parent()
                    level += 1

            else:
                level = 0
            self.__right_click_menu = QMenu()
            if len(indexes) > 2:
                self.__AddMulti = self.__right_click_menu.addAction("AddMultiToShowAction")
                self.__AddMulti.triggered.connect(partial(self.AddMultiToShowAction,indexes))
            else:
                self.__AddSingle = self.__right_click_menu.addAction("AddToShowFile")
                self.__AddSingle.triggered.connect(partial(self.AddMultiToShowAction,indexes))
            self.__reload = self.__right_click_menu.addAction("Reload")
            self.__reload.triggered.connect(self.Update)
            self.__right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))


    def importData(self):
        self.model.setRowCount(0)
        parent = self.model.invisibleRootItem()
        seen = {}
        seen[0]=self.model.invisibleRootItem()

        values = deque(self.data)
        while values:
            value = values.popleft()
            pid = value['parent_id']
            if pid not in seen:
                values.append(value)
                continue
            parent = seen[pid]
            unique_id = value['unique_id']
            SI1 = StandardItem(value['Name'],icons[value['type']])
            SI1.setEditable(False)
            SI2 = QStandardItem(value['Date'])
            SI2.setEditable(False)
            SI3 = QStandardItem(value['Path'])
            SI3.setEditable(False)
            parent.appendRow([SI1,SI2,SI3])
            seen[unique_id] = parent.child(parent.rowCount() - 1)
    """Not working with folder parrents"""
    def __getScanNames(self):
        dirPath=self.dirPath
        dirPath = dirPath.replace('~', os.path.expanduser('~'), 1)
        dirPath = os.path.normpath(dirPath).replace('\\','/')
        if dirPath[-1] != '/': dirPath = dirPath+'/'
        unique_id = 1
        DictTempFolder = {}
        for filne in glob.iglob(dirPath + '/**/*.dat', recursive=True):
            filne = os.path.normpath(filne).replace('\\', '/')
            name_without_path = filne[len(dirPath):]
            listOfincluding = name_without_path.split('/')
            folder_in_list = 0
            for call in listOfincluding:
                addDict = {'unique_id': 1, 'parent_id': 0, 'Name': '', 'Date': '', 'type': 'Folder', 'Path': ''}
                if call.rfind('.dat') != -1:  # file
                    addDict['type'] = 'file'
                    addDict['Name'] = call.split('.dat')[0]
                    addDict['Path'] = dirPath[:-1] + ''.join(['/' + x for x in listOfincluding])
                else:  # folder
                    folder_in_list = folder_in_list + 1
                    addDict['Path'] = dirPath[:-1] + ''.join(['/' + x for x in listOfincluding[:folder_in_list]]) + '/'
                    addDict['type'] = 'folder'
                    addDict['Name'] = call
                # unique folder check
                pathToFolderOfTHisSolutions=dirPath[:-1] + ''.join(['/' + x for x in listOfincluding[:-1]])+'/'
                if dirPath == pathToFolderOfTHisSolutions:
                    addDict['parent_id'] = 0
                    # root
                    if addDict['type'] == 'folder' and addDict['Path'] not in DictTempFolder.keys():
                        DictTempFolder[addDict['Path']] = unique_id
                    elif addDict['type'] == 'folder':
                        continue
                else:
                    #somsing wrong here
                    if addDict['type'] == 'file':
                        if os.path.dirname(addDict['Path'][:-1]) + '/' in DictTempFolder.keys():
                            addDict['parent_id'] = DictTempFolder[os.path.dirname(addDict['Path'][:-1]) + '/']
                    if addDict['type'] == 'folder':
                        if os.path.dirname(addDict['Path'][:-1])+'/' in DictTempFolder.keys():
                            addDict['parent_id'] = DictTempFolder[os.path.dirname(addDict['Path'][:-1])+'/']
                        if addDict['Path'] not in DictTempFolder.keys():
                            DictTempFolder[addDict['Path']] = unique_id
                        else:
                            continue
                addDict['unique_id'] = unique_id
                addDict['Date'] = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime(os.path.getctime(addDict['Path'])))
                unique_id = unique_id + 1
                self.data.append(addDict)



import sys
import traceback





def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
#    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось


sys.excepthook = excepthook



















if __name__ == '__main__':
    if __name__ == '__main__':
        import platform, os

        if platform.system() == 'Windows':
            path_to_file = os.getcwd() + "/data/"
        else:
            path_to_file = '~/Documents/GinaSpectrum/'
    path_to_file = path_to_file.replace('~', os.path.expanduser('~'), 1)
    app = QApplication(sys.argv)
    view = view(path_to_file)

    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())