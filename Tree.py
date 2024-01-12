import os
import time
import glob
from functools import partial
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


icons={'folder':'./icons/folder.png','file':'./icons/spectrum.png'}


class StandardItem(QStandardItem):
    """Item of tree with image"""
    def __init__(self, txt='', image_path=''):
        super().__init__()
        self.setEditable(False)
        self.setText(txt)
        if image_path:
            image = QImage(image_path)
            image.size()
            self.setData(image, Qt.DecorationRole)


class TreeOfDataFolder(QWidget):
    """
        Working folder Tree class
        :param dir_path: folder path
        :param parent: class of main widget class
        """
    def __init__(self, dir_path, parent=None):
        super(TreeOfDataFolder, self).__init__()
        super().__init__(parent)
        self.parent=parent
        self.dir_path=dir_path
        self.data = []
        self.tree = QTreeView(self)
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Spectrum','Date','Path'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.tree.setColumnHidden(2,True)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.label.setText(self.dir_path)
        self.update_data()

        self.tree.expandAll()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)
        self.tree.doubleClicked.connect(self.doubleClickAction)

    def update_data (self):
        number_of_data = len(self.data)
        data=self.__get_scan_names()
        if number_of_data < len(data):
            self.data = data
            self.import_data()

    def AddMultiToShowAction(self,listItems):
        items = self.tree.selectedIndexes()
        items = self.__clear_folder_from_indexes(items)
        self.__show_spectrum(items)


    def doubleClickAction(self, index):
        items = self.tree.selectedIndexes()
        items = self.__clear_folder_from_indexes(items)
        self.__show_spectrum(items)

    def __show_spectrum(self, selected_indexes_list):
        result = []
        if self.parent is None:
            return

        for i in range(0, len(selected_indexes_list), 2):
            result.append({'Name': self.model.data(selected_indexes_list[i]),
                           'Date': self.model.data(selected_indexes_list[i + 1]),
                           'Path': self.model.data(selected_indexes_list[i].siblingAtColumn(2))
                           })
        self.parent.show_new_spectrum(result)

    def __clear_folder_from_indexes(self, indexes: list):
        return [index for index in indexes if os.path.isfile(self.model.data(index.siblingAtColumn(2)))]

    def openMenu(self, position):
            indexes = self.sender().selectedIndexes()
            indexes = self.__clear_folder_from_indexes(indexes)
            mdl_idx = self.tree.indexAt(position)

            if not mdl_idx.isValid():
                return

            if not indexes:
                return

            self.__right_click_menu = QMenu()

            if len(indexes) > 2:
                self.__AddMulti = self.__right_click_menu.addAction("AddMultiToShowAction")
                self.__AddMulti.triggered.connect(partial(self.AddMultiToShowAction,indexes))
            else:
                self.__AddSingle = self.__right_click_menu.addAction("AddToShowFile")
                self.__AddSingle.triggered.connect(partial(self.AddMultiToShowAction,indexes))
            self.__reload = self.__right_click_menu.addAction("Reload")
            self.__reload.triggered.connect(self.update_data)
            self.__right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def import_data(self):
        self.model.setRowCount(0)
        seen = {0: self.model.invisibleRootItem()}
        values = deque(self.data)
        while values:
            value = values.popleft()
            pid = value['parent_id']
            if pid not in seen:
                values.append(value)
                continue
            parent = seen[pid]
            unique_id = value['unique_id']
            seen_item_1, seen_item_2, seen_item_3 = (StandardItem(value['Name'],icons[value['type']]),
                                                     QStandardItem(value['Date']),
                                                     QStandardItem(value['Path'])
                                                     )
            seen_item_1.setEditable(False)
            seen_item_2.setEditable(False)
            seen_item_3.setEditable(False)

            parent.appendRow([seen_item_1, seen_item_2, seen_item_3])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

    def __get_scan_names(self):
        result = []
        dir_path = self.dir_path
        dir_path = dir_path.replace('~', os.path.expanduser('~'), 1)
        dir_path = os.path.normpath(dir_path).replace('\\','/')
        if dir_path[-1] != '/': dir_path = dir_path+'/'
        unique_id = 1
        dict_temp_folder = {}
        for file_path in glob.iglob(dir_path + '/**/*.dat', recursive=True):
            file_path = os.path.normpath(file_path).replace('\\', '/')
            name_without_path = file_path[len(dir_path):]
            list_of_including = name_without_path.split('/')
            folder_in_list = 0
            for call in list_of_including:
                add_dict = {'unique_id': 1, 'parent_id': 0, 'Name': '', 'Date': '', 'type': 'Folder', 'Path': ''}
                if call.rfind('.dat') != -1:  # file
                    add_dict['type'] = 'file'
                    add_dict['Name'] = call.split('.dat')[0]
                    add_dict['Path'] = dir_path[:-1] + ''.join(['/' + x for x in list_of_including])
                else:  # folder
                    folder_in_list = folder_in_list + 1
                    add_dict['Path'] = dir_path[:-1] + ''.join(['/' + x for x in list_of_including[:folder_in_list]]) + '/'
                    add_dict['type'] = 'folder'
                    add_dict['Name'] = call
                # unique folder check
                path_to_folder_of_this_solutions=dir_path[:-1] + ''.join(['/' + x for x in list_of_including[:-1]])+'/'

                if dir_path == path_to_folder_of_this_solutions:
                    add_dict['parent_id'] = 0
                    # root
                    if add_dict['type'] == 'folder' and add_dict['Path'] not in dict_temp_folder.keys():
                        dict_temp_folder[add_dict['Path']] = unique_id
                    elif add_dict['type'] == 'folder':
                        continue
                else:
                    #somsing wrong here
                    if add_dict['type'] == 'file':
                        if os.path.dirname(add_dict['Path'][:-1]) + '/' in dict_temp_folder.keys():
                            add_dict['parent_id'] = dict_temp_folder[os.path.dirname(add_dict['Path'][:-1]) + '/']
                    if add_dict['type'] == 'folder':
                        if os.path.dirname(add_dict['Path'][:-1])+'/' in dict_temp_folder.keys():
                            add_dict['parent_id'] = dict_temp_folder[os.path.dirname(add_dict['Path'][:-1])+'/']
                        if add_dict['Path'] not in dict_temp_folder.keys():
                            dict_temp_folder[add_dict['Path']] = unique_id
                        else:
                            continue
                add_dict['unique_id'] = unique_id
                add_dict['Date'] = time.strftime("%d-%b-%Y %H:%M:%S", time.gmtime(os.path.getctime(add_dict['Path'])))
                unique_id = unique_id + 1
                result.append(add_dict)
        return result






















if __name__ == '__main__':
        import platform, os

        if platform.system() == 'Windows':
            path_to_file = os.getcwd() + "/data/"
        else:
            path_to_file = '~/Documents/GinaSpectrum/'
        path_to_file = path_to_file.replace('~', os.path.expanduser('~'), 1)
        app = QApplication(sys.argv)
        view = TreeOfDataFolder(path_to_file)

        view.setWindowTitle('QTreeview Example')
        view.show()
        sys.exit(app.exec_())