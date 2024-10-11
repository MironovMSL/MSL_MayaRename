try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\SuffixPrefixWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class SuffixPrefixWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SuffixPrefixWidget, self).__init__(parent)

        self.setObjectName("SuffixPrefixWidget")

        self.FixedHeight = 25
        self.PrefixHolder = "prefix_"
        self.SuffixHolder = "_suffix"

        self.setFixedHeight(self.FixedHeight)


        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):

        Width = 90
        # button add prefix
        self.prefix_add_btn = QtWidgets.QPushButton("+")
        self.prefix_add_btn.setFixedWidth(25)

        # QlineEdit prefix
        self.prefix_Editline = QtWidgets.QLineEdit()
        self.prefix_Editline.setPlaceholderText(self.PrefixHolder)
        self.prefix_Editline.setMinimumWidth(Width)

        # label type of selection
        self.typeSelection = QtWidgets.QLabel()
        svg_path = os.path.join(new_root, "resources", "icon", "crab-svgrepo-com.svg")
        svg_renderer = QtSvg.QSvgRenderer(svg_path)

        pixmap = QtGui.QPixmap(25, 25)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        # Устанавливаем QPixmap в QLabel
        self.typeSelection.setPixmap(pixmap)
        self.typeSelection.resize(25, 25)


        # button add suffix
        self.suffix_add_btn = QtWidgets.QPushButton("+")
        self.suffix_add_btn.setFixedWidth(25)

        # QlineEdit suffix
        self.suffix_Editline = QtWidgets.QLineEdit()
        self.suffix_Editline.setPlaceholderText(self.SuffixHolder)
        self.suffix_Editline.setMinimumWidth(Width)

        # # button functions
        # self.Auto_suffix = QtWidgets.QPushButton("AS")
        # self.Auto_suffix.setFixedWidth(25)
        # # lt_ rt_ mid_
        # self.Auto_pref = QtWidgets.QPushButton("AP")
        # self.Auto_pref.setFixedWidth(25)


    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.prefix_add_btn)
        self.main_layout.addWidget(self.prefix_Editline)
        self.main_layout.addWidget(self.typeSelection)
        self.main_layout.addWidget(self.suffix_Editline)
        self.main_layout.addWidget(self.suffix_add_btn)
        # self.main_layout.addWidget(self.Auto_suffix)
        # self.main_layout.addWidget(self.Auto_pref)

    def create_connections(self):
        pass
