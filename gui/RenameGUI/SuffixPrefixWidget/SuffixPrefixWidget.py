try:
    from PySide2 import QtWidgets, QtGui, QtCore, QtSvg
except:
    from PySide6 import QtWidgets, QtGui, QtCore, QtSvg

from MSL_MayaRename.gui.RenameGUI.SuffixPrefixWidget.LineEditorPrefSufWidget import LineEditorPrefSufWidget
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.core.config import Configurator
import os
import maya.cmds as cmds

root_ = os.path.dirname(__file__) #...\SuffixPrefixWidget
new_root = os.path.abspath(os.path.join(root_, '..', '..')) # ...\gui

class SuffixPrefixWidget(QtWidgets.QWidget):
    itEditPrefix = QtCore.Signal(str)
    itEditSuffix = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(SuffixPrefixWidget, self).__init__(parent)

        self.setObjectName("SuffixPrefixWidget")
        self.resources = Resources.get_instance()
        self.QSettings = QtCore.QSettings(self.resources.config_path, QtCore.QSettings.IniFormat)

        self.FixedHeight = 25
        self.PrefixHolder = "prefix_"
        self.SuffixHolder = "_suffix"

        self.prefix = self.QSettings.value("startup/prefix", str)
        self.suffix = self.QSettings.value("startup/suffix", str)


        self.setFixedHeight(self.FixedHeight)


        self.create_Widgets()
        self.create_layouts()
        self.create_connections()

    def create_Widgets(self):

        Width = 120
        # button add prefix
        self.prefix_add_btn = QtWidgets.QPushButton("+")
        self.prefix_add_btn.setFixedWidth(25)
        # QlineEdit prefix
        self.prefix_Editline = LineEditorPrefSufWidget(self.PrefixHolder, Width)
        self.prefix_Editline.AutoComplete_line_edit.setText(self.prefix)
        # ---------------------------------
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
        #---------------------------------
        # button add suffix
        self.suffix_add_btn = QtWidgets.QPushButton("+")
        self.suffix_add_btn.setFixedWidth(25)
        # QlineEdit suffix
        self.suffix_Editline = LineEditorPrefSufWidget(self.SuffixHolder, Width)
        self.suffix_Editline.AutoComplete_line_edit.setText(self.suffix)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.prefix_add_btn)
        self.main_layout.addWidget(self.prefix_Editline)
        self.main_layout.addWidget(self.typeSelection)
        self.main_layout.addWidget(self.suffix_Editline)
        self.main_layout.addWidget(self.suffix_add_btn)

    def create_connections(self):
        self.prefix_Editline.AutoComplete_line_edit.textEdited.connect(self.edit_prefix)
        self.suffix_Editline.AutoComplete_line_edit.textEdited.connect(self.edit_suffix)

    def edit_prefix(self, prefix):
        self.QSettings.setValue("startup/prefix", prefix)
        self.itEditPrefix.emit(prefix)

    def edit_suffix(self, suffix):
        self.QSettings.setValue("startup/suffix", suffix)
        self.itEditSuffix.emit(suffix)


