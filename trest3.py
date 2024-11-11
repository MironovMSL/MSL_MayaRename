try:
    # Qt5
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
except:
    # Qt6
    from PySide6 import QtCore
    from PySide6 import QtWidgets
    from shiboken6 import wrapInstance

import sys
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class ToolDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super().__init__(parent)
        
        self.setWindowTitle("Common Widgets")
        self.setMinimumSize(300, 120)
        
        # On macOS make the window a Tool to keep it on top of Maya
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
        self.update_text(self.combo_box.currentText())
        self.update_index(self.combo_box.currentIndex())
    
    def create_widgets(self):
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItem("Item 01", 22)
        self.combo_box.addItem("Item 02", "A string")
        self.combo_box.addItem("Item 03", [22, 33, 44])
        self.combo_box.addItem("Item 04", self)
        
        self.selected_text_label = QtWidgets.QLabel()
        self.selected_index_label = QtWidgets.QLabel()
        self.selected_data_label = QtWidgets.QLabel()
    
    def create_layout(self):
        combo_box_layout = QtWidgets.QHBoxLayout()
        combo_box_layout.setContentsMargins(0, 0, 0, 0)
        combo_box_layout.addWidget(QtWidgets.QLabel("Item Select:"))
        combo_box_layout.addWidget(self.combo_box)
        combo_box_layout.addStretch()
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(combo_box_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.selected_text_label)
        main_layout.addWidget(self.selected_index_label)
        main_layout.addWidget(self.selected_data_label)
    
    def create_connections(self):
        self.combo_box.currentTextChanged.connect(self.update_text)
        self.combo_box.currentIndexChanged.connect(self.update_index)
    
    def update_text(self, text):
        self.selected_text_label.setText(f"Selected Text: {text}")
        
        data = self.combo_box.currentData()
        self.selected_data_label.setText(f"Selected Data: {data}")
        
        if data == self:
            print(data.windowTitle())
    
    def update_index(self, index):
        self.selected_index_label.setText(f"Selected Index: {index}")


if __name__ == "__main__":
    try:
        win.close()  # pylint: disable=E0601
        win.deleteLater()
    except:
        pass
    
    win = ToolDialog()
    win.show()


class NumberSliderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Position Slider")

        # Текст, в который будем вставлять число
        self.text = "This is a number: ____ and it can move."
        self.number = 42  # Число, которое будем двигать
        self.number_position = 16  # Начальная позиция для числа в строке

        # Метка с текстом
        self.label_var = tk.StringVar()
        self.update_label_text()

        self.label = ttk.Label(self.root, textvariable=self.label_var, font=("Arial", 16))
        self.label.pack(pady=20)

        # Слайдер для управления позицией числа
        self.slider = ttk.Scale(self.root, from_=0, to=len(self.text)-len(str(self.number)), orient="horizontal", command=self.slider_moved)
        self.slider.set(self.number_position)  # Устанавливаем начальную позицию слайдера
        self.slider.pack(pady=20)

    def update_label_text(self):
        # Обновляем текст метки с учётом новой позиции числа
        number_str = str(self.number)
        updated_text = self.text[:self.number_position] + number_str + self.text[self.number_position + len(number_str):]
        self.label_var.set(updated_text)

    def slider_moved(self, value):
        # Когда слайдер двигается, меняем позицию числа
        self.number_position = int(float(value))  # Позиция на основе слайдера
        self.update_label_text()  # Обновляем метку


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSliderApp(root)
    root.mainloop()

#------------------------------------
#------------------------------------
#------------------------------------
#------------------------------------
#------------------------------------
#------------------------------------
#------------------------------------
import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class PopUpWindow(QtWidgets.QWidget):

    def __init__(self, name, parent=None):
        super(PopUpWindow, self).__init__(parent)

        self.setWindowTitle("{0} Options".format(name))

        self.setWindowFlags(QtCore.Qt.Popup)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.size_sb = QtWidgets.QSpinBox()
        self.size_sb.setRange(1, 100)
        self.size_sb.setValue(12)

        self.opacity_sb = QtWidgets.QSpinBox()
        self.opacity_sb.setRange(0, 100)
        self.opacity_sb.setValue(100)

    def create_layout(self):
        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Size:", self.size_sb)
        layout.addRow("Opacity:", self.opacity_sb)


class ToolboxButton(QtWidgets.QPushButton):

    def __init__(self, name, parent=None):
        super(ToolboxButton, self).__init__(parent)

        self.pop_up_window = PopUpWindow(name, self)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_pop_up_window)

    def show_pop_up_window(self, pos):
        pop_up_pos = self.mapToGlobal(QtCore.QPoint(8, self.height() + 8))
        self.pop_up_window.move(pop_up_pos)

        self.pop_up_window.show()


class ToolboxDialog(QtWidgets.QDialog):

    IMAGE_DIR = "D:/Temp/Patreon"

    def __init__(self, parent=maya_main_window()):
        super(ToolboxDialog, self).__init__(parent)

        self.setWindowTitle("Toolbox")
        self.setFixedSize(150,40)

        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.pencil_btn = ToolboxButton("Pencil")
        self.pencil_btn.setFixedSize(30, 30)
        self.pencil_btn.setCheckable(True)
        self.pencil_btn.setChecked(True)
        self.pencil_btn.setFlat(True)
        self.pencil_btn.setIcon(QtGui.QIcon("{0}/pencil.png".format(ToolboxDialog.IMAGE_DIR)))

        self.brush_btn = ToolboxButton("Brush")
        self.brush_btn.setFixedSize(30, 30)
        self.brush_btn.setCheckable(True)
        self.brush_btn.setFlat(True)
        self.brush_btn.setIcon(QtGui.QIcon("{0}/brush.png".format(ToolboxDialog.IMAGE_DIR)))

        self.eraser_btn = ToolboxButton("Eraser")
        self.eraser_btn.setFixedSize(30, 30)
        self.eraser_btn.setCheckable(True)
        self.eraser_btn.setFlat(True)
        self.eraser_btn.setIcon(QtGui.QIcon("{0}/eraser.png".format(ToolboxDialog.IMAGE_DIR)))

        self.text_btn = ToolboxButton("Text")
        self.text_btn.setFixedSize(30, 30)
        self.text_btn.setCheckable(True)
        self.text_btn.setFlat(True)
        self.text_btn.setIcon(QtGui.QIcon("{0}/text.png".format(ToolboxDialog.IMAGE_DIR)))

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.pencil_btn)
        main_layout.addWidget(self.brush_btn)
        main_layout.addWidget(self.eraser_btn)
        main_layout.addWidget(self.text_btn)
        main_layout.addStretch()

    def create_connections(self):
        self.pencil_btn.clicked.connect(self.on_checked_state_changed)
        self.brush_btn.clicked.connect(self.on_checked_state_changed)
        self.eraser_btn.clicked.connect(self.on_checked_state_changed)
        self.text_btn.clicked.connect(self.on_checked_state_changed)

    def on_checked_state_changed(self):
        button = self.sender()

        self.pencil_btn.setChecked(button == self.pencil_btn)
        self.brush_btn.setChecked(button == self.brush_btn)
        self.eraser_btn.setChecked(button == self.eraser_btn)
        self.text_btn.setChecked(button == self.text_btn)


if __name__ == "__main__":

    try:
        toolbox_dialog.close() # pylint: disable=E0601
        toolbox_dialog.deleteLater()
    except:
        pass

    toolbox_dialog = ToolboxDialog()
    toolbox_dialog.show()

import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class DragAndDropNodeListWidget(QtWidgets.QListWidget):
    nodes_dropped = QtCore.Signal(list)
    
    def __init__(self, parent=None):
        super(DragAndDropNodeListWidget, self).__init__(parent)
        
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
    
    def startDrag(self, supported_actions):
        items = self.selectedItems()
        nodes = []
        for item in items:
            nodes.append(item.data(QtCore.Qt.UserRole))
        
        nodes_str = " ".join(nodes)
        
        mime_data = QtCore.QMimeData()
        
        if sys.version_info.major >= 3:
            mime_data.setData("zurbrigg/node_list", nodes_str.encode())
        else:
            mime_data.setData("zurbrigg/node_list", QtCore.QByteArray(str(nodes_str)))
        
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        
        drag.exec_()
    
    def dragEnterEvent(self, drag_event):
        if drag_event.mimeData().hasFormat("zurbrigg/node_list"):
            drag_event.acceptProposedAction()
    
    def dragMoveEvent(self, drag_event):
        pass
    
    def dropEvent(self, drop_event):
        mime_data = drop_event.mimeData()
        
        if mime_data.hasFormat("zurbrigg/node_list"):
            nodes_byte_array = mime_data.data("zurbrigg/node_list")
            
            if sys.version_info.major >= 3:
                nodes_str = nodes_byte_array.data().decode()
            else:
                nodes_str = str(nodes_byte_array)
            
            nodes = nodes_str.split(" ")
            
            self.nodes_dropped.emit(nodes)


class MeshVisibilityDialog(QtWidgets.QDialog):
    WINDOW_TITLE = "Mesh Visibility"
    
    def __init__(self, parent=maya_main_window()):
        super(MeshVisibilityDialog, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
        self.refresh_lists()
    
    def create_widgets(self):
        self.visible_mesh_list_wdg = DragAndDropNodeListWidget()
        self.visible_mesh_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.hidden_mesh_list_wdg = DragAndDropNodeListWidget()
        self.hidden_mesh_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.hide_btn = QtWidgets.QPushButton(">>")
        self.hide_btn.setFixedWidth(24)
        self.show_btn = QtWidgets.QPushButton("<<")
        self.show_btn.setFixedWidth(24)
        
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")
    
    def create_layout(self):
        visible_mesh_layout = QtWidgets.QVBoxLayout()
        visible_mesh_layout.addWidget(QtWidgets.QLabel("Visible Meshes:"))
        visible_mesh_layout.addWidget(self.visible_mesh_list_wdg)
        
        hidden_mesh_layout = QtWidgets.QVBoxLayout()
        hidden_mesh_layout.addWidget(QtWidgets.QLabel("Hidden Meshes:"))
        hidden_mesh_layout.addWidget(self.hidden_mesh_list_wdg)
        
        show_hide_button_layout = QtWidgets.QVBoxLayout()
        show_hide_button_layout.addStretch()
        show_hide_button_layout.addWidget(self.hide_btn)
        show_hide_button_layout.addWidget(self.show_btn)
        show_hide_button_layout.addStretch()
        
        list_layout = QtWidgets.QHBoxLayout()
        list_layout.addLayout(visible_mesh_layout)
        list_layout.addLayout(show_hide_button_layout)
        list_layout.addLayout(hidden_mesh_layout)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(4)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(list_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def create_connections(self):
        self.hide_btn.clicked.connect(self.hide_selected)
        self.show_btn.clicked.connect(self.show_selected)
        
        self.visible_mesh_list_wdg.nodes_dropped.connect(self.show_nodes)
        self.hidden_mesh_list_wdg.nodes_dropped.connect(self.hide_nodes)
        
        self.refresh_btn.clicked.connect(self.refresh_lists)
        self.close_btn.clicked.connect(self.close)
    
    def refresh_lists(self):
        self.visible_mesh_list_wdg.clear()
        self.hidden_mesh_list_wdg.clear()
        
        meshes = cmds.ls(type="mesh", long=True)
        meshes.sort()
        
        for mesh in meshes:
            transform_short_name = cmds.listRelatives(mesh, parent=True, type="transform")[0]
            transform_long_name = cmds.listRelatives(mesh, parent=True, type="transform", fullPath=True)[0]
            
            item = QtWidgets.QListWidgetItem(transform_short_name)
            item.setData(QtCore.Qt.UserRole, transform_long_name)
            
            if self.is_node_visible(transform_long_name):
                self.visible_mesh_list_wdg.addItem(item)
            else:
                self.hidden_mesh_list_wdg.addItem(item)
    
    def is_node_visible(self, name):
        return cmds.getAttr("{0}.visibility".format(name))
    
    def set_node_visible(self, name, visible):
        cmds.setAttr("{0}.visibility".format(name), visible)
    
    def show_nodes(self, nodes):
        for node in nodes:
            self.set_node_visible(node, True)
        
        self.refresh_lists()
        
        for i in range(self.visible_mesh_list_wdg.count()):
            item = self.visible_mesh_list_wdg.item(i)
            if item.data(QtCore.Qt.UserRole) in nodes:
                self.visible_mesh_list_wdg.setCurrentRow(i, QtCore.QItemSelectionModel.Select)
    
    def hide_nodes(self, nodes):
        for node in nodes:
            self.set_node_visible(node, False)
        
        self.refresh_lists()
        
        for i in range(self.hidden_mesh_list_wdg.count()):
            item = self.hidden_mesh_list_wdg.item(i)
            if item.data(QtCore.Qt.UserRole) in nodes:
                self.hidden_mesh_list_wdg.setCurrentRow(i, QtCore.QItemSelectionModel.Select)
    
    def show_selected(self):
        nodes = []
        selected_items = self.hidden_mesh_list_wdg.selectedItems()
        
        for item in selected_items:
            nodes.append(item.data(QtCore.Qt.UserRole))
        
        self.show_nodes(nodes)
    
    def hide_selected(self):
        nodes = []
        selected_items = self.visible_mesh_list_wdg.selectedItems()
        for item in selected_items:
            nodes.append(item.data(QtCore.Qt.UserRole))
        
        self.hide_nodes(nodes)


if __name__ == "__main__":
    
    try:
        mesh_dialog.close()  # pylint: disable=E0601
        mesh_dialog.deleteLater()
    except:
        pass
    
    mesh_dialog = MeshVisibilityDialog()
    mesh_dialog.show()
    
    
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TextEditor(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

    def open_file(self, file_path):
        if file_path:
            file_info = QtCore.QFileInfo(file_path)
            if file_info.exists() and file_info.isFile():

                f = QtCore.QFile(file_info.absoluteFilePath())
                if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                    text_stream = QtCore.QTextStream(f)
                    text_stream.setCodec("UTF-8")

                    text = text_stream.readAll()

                    f.close()

                    self.setPlainText(text)

    def dragEnterEvent(self, drag_event):
        if drag_event.mimeData().hasText() or drag_event.mimeData().hasUrls():
            drag_event.acceptProposedAction()

    def dropEvent(self, drop_event):
        if drop_event.mimeData().hasUrls():
            urls = drop_event.mimeData().urls()

            file_path = urls[0].toLocalFile()
            self.open_file(file_path)

            return

        super(TextEditor, self).dropEvent(drop_event)


class TextEditorDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "File Explorer Drag and Drop"

    def __init__(self, parent=maya_main_window()):
        super(TextEditorDialog, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(800, 400)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.editor = TextEditor()

        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.close_btn = QtWidgets.QPushButton("Close")

        self.create_tree_view()

    def create_tree_view(self):
        root_path = "{0}scripts".format(cmds.internalVar(userAppDir=True))

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(root_path)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(3)
        self.tree_view.setColumnWidth(0, 240)
        self.tree_view.setFixedWidth(360)

        self.tree_view.setDragEnabled(True)

        self.model.setNameFilters(["*.py"])
        self.model.setNameFilterDisables(False)

    def create_layout(self):
        side_bar_layout = QtWidgets.QHBoxLayout()
        side_bar_layout.addWidget(self.tree_view)
        side_bar_layout.addWidget(self.editor)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(4)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addLayout(side_bar_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.tree_view.doubleClicked.connect(self.open_file)

        self.clear_btn.clicked.connect(self.clear_editor)
        self.close_btn.clicked.connect(self.close)

    def clear_editor(self):
        self.editor.setPlainText("")

    def open_file(self, index):
        if not self.model.isDir(index):
            file_path = self.model.filePath(index)
            self.editor.open_file(file_path)


if __name__ == "__main__":

    try:
        text_editor_dialog.close() # pylint: disable=E0601
        text_editor_dialog.deleteLater()
    except:
        pass

    text_editor_dialog = TextEditorDialog()
    text_editor_dialog.show()



