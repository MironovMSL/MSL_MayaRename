import tkinter as tk
from tkinter import ttk

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
