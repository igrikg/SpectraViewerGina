import sys,os,glob
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
iconFolder='/home/nsluser/PycharmProjects/SpectraViewerGina/icons/folder.png'

class StandardItem(QStandardItem):
    def __init__(self, txt='', image_path=''):
        super().__init__()
        self.setEditable(False)
        self.setText(txt)
        if image_path:
            print(image_path)
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
        self.__getScanNames()
        self.importData()
        self.tree.expandAll()




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
            SI1 = StandardItem(value['Name'],iconFolder)
            SI1.setEditable(False)
            SI2 = QStandardItem(value['Date'])
            SI2.setEditable(False)
            SI3 = QStandardItem(value['Path'])
            SI3.setEditable(False)
            parent.appendRow([SI1,SI2,SI3])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    def __getScanNames(self):
        dirPath=self.dirPath
        dirPath = dirPath.replace('~', os.path.expanduser('~'), 1)
        unique_id = 1
        for filne in glob.iglob(dirPath + '/**/*.dat', recursive=True):
            name_without_path = filne[len(dirPath):]
            listOfincluding = name_without_path.split('/')
            folder_in_list = 0
            parent_id = unique_id - 1
            for call in listOfincluding:
                addDict = {'unique_id': 1, 'parent_id': 0, 'Name': '', 'Date': '', 'type': 'Folder', 'Path': ''}
                if call.rfind('.dat') != -1:  # file
                    addDict['parent_id'] = parent_id
                    addDict['type'] = 'file'
                    addDict['Name'] = call.split('.dat')[0]
                    addDict['Path'] = dirPath[:-1] + ''.join(['/' + x for x in listOfincluding])
                else:  # folder
                    parent_id = parent_id + 1
                    if folder_in_list == 0:
                        addDict['parent_id'] = 0
                    else:
                        addDict['parent_id'] = parent_id - folder_in_list
                    folder_in_list = folder_in_list + 1
                    addDict['type'] = 'folder'
                    addDict['Name'] = call
                    addDict['Path'] = dirPath[:-1] + ''.join(['/' + x for x in listOfincluding[:folder_in_list]]) + '/'
                addDict['unique_id'] = unique_id
                addDict['Date'] = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime(os.path.getctime(addDict['Path'])))
                unique_id = unique_id + 1
                self.data.append(addDict)


if __name__ == '__main__':

    path_to_file = '~/Documents/GinaSpectrum/'
    path_to_file = path_to_file.replace('~', os.path.expanduser('~'), 1)
    app = QApplication(sys.argv)
    view = view(path_to_file)
    view.setGeometry(300, 100, 600, 300)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())