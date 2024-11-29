try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore

from MSL_MayaRename.core.common import *
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryButtonMode import LibraryButtonMode
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.CustomScrollArea import CustomScrollArea
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.CacheWidget import CacheWidget

import os
import maya.cmds as cmds

class QuickListButtonNameWidget(QtWidgets.QWidget):

    itShowCahe = QtCore.Signal(bool)
    itClickedCache = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(QuickListButtonNameWidget, self).__init__(parent)
        
        self.resources = Resources.get_instance()
        # Attribute---------------------------
        self.FixedHeight = 60
        # Setting---------------------------
        self.setObjectName("QuickListButtonNameID")
        self.setFixedHeight(self.FixedHeight)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):
        self.library_BTN = LibraryButtonMode(25, 25)
        self.Scroll_Area = CustomScrollArea()
        self.cache_area  = CacheWidget()

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.QuickButtonlayount = QtWidgets.QHBoxLayout(self)
        self.QuickButtonlayount.setContentsMargins(0, 0, 0, 0)
        self.QuickButtonlayount.setSpacing(0)

        self.QuickButtonlayount.addWidget(self.Scroll_Area)
        self.QuickButtonlayount.addWidget(self.library_BTN)
        self.QuickButtonlayount.setAlignment(self.library_BTN, QtCore.Qt.AlignTop)
        
        self.main_layout.addLayout(self.QuickButtonlayount)
        self.main_layout.addWidget(self.cache_area)
        
        self.main_layout.addStretch()


    def create_connections(self):
        self.library_BTN.itShowCache.connect(self.show_cache)
        self.cache_area.itClickedCache.connect(lambda name: self.itClickedCache.emit(name))
    
    def add_cache(self, name):
        all_name = self.resources.all_item_json
        found = False

        if name not in all_name:
            for i in range(self.library_BTN.Library_Win.MainScrollArea.scroll_area_widget.main_layout.count()):
                item = self.library_BTN.Library_Win.MainScrollArea.scroll_area_widget.main_layout.itemAt(i).widget()
                if item and hasattr(item, 'name') and item.name == "Cache":
                    found = True
                    break
                    
            if not found:
                self.library_BTN.Library_Win.add_category("Cache")
                self.parent().RenameWidget.LineEditor.word_list.append("Cache")
            
            
            button = self.library_BTN.Library_Win.add_subCategory(name=name, category="Cache")
            if button:
                self.parent().RenameWidget.LineEditor.word_list.append(name)
            
            self.parent().RenameWidget.LineEditor.update_words()
        
        self.cache_area.scroll_area.scroll_area_widget.add_button(name)
        
        self.library_BTN.Library_Win.save_library()

    def show_cache(self, state):
        self.cache_area.setVisible(state)
        
        if state:
            self.FixedHeight = 60
        else:
            self.FixedHeight = 30
        
        self.setFixedHeight(self.FixedHeight)
        self.cache_area.setVisible(state)
        
        self.itShowCahe.emit(state)
        