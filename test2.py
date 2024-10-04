import sys

from PySide6 import QtCore
from PySide6 import QtWidgets

class StandaloneWindow(QtWidgets.QWidget):

    CONFIG_PATH = "{0}/QSettingsExample/config.ini".format(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation))

    def __init__(self):
        super(StandaloneWindow, self).__init__(parent=None)

        self.setWindowTitle("QSettings Example")
        self.setMinimumSize(400, 300)

        self.create_widgets()
        self.create_layout()

        self.load_settings()
        print(self.CONFIG_PATH)

    def create_widgets(self):
        self.temp_dir_le = QtWidgets.QLineEdit()
        self.temp_dir_browse_btn = QtWidgets.QPushButton("Browse...")

        self.cache_size_sb = QtWidgets.QSpinBox()
        self.cache_size_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.cache_size_sb.setMinimum(256)
        self.cache_size_sb.setMaximum(8192)
        self.cache_size_sb.setValue(1024)
        self.cache_size_sb.setFixedWidth(40)

        self.resize_to_fit_cb = QtWidgets.QCheckBox("Resize to fit video")
        self.endless_mouse_cb = QtWidgets.QCheckBox("Endless mouse scrub")

    def create_layout(self):
        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.temp_dir_le)
        file_layout.addWidget(self.temp_dir_browse_btn)

        file_grp = QtWidgets.QGroupBox("Temp Directory")
        file_grp.setLayout(file_layout)

        cache_size_layout = QtWidgets.QHBoxLayout()
        cache_size_layout.addWidget(self.cache_size_sb)
        cache_size_layout.addStretch()

        cache_layout = QtWidgets.QFormLayout()
        cache_layout.addRow("Size: ", cache_size_layout)

        cache_grp = QtWidgets.QGroupBox("Cache")
        cache_grp.setLayout(cache_layout)

        options_layout = QtWidgets.QVBoxLayout()
        options_layout.addWidget(self.resize_to_fit_cb)
        options_layout.addWidget(self.endless_mouse_cb)

        options_grp = QtWidgets.QGroupBox("Options")
        options_grp.setLayout(options_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(file_grp)
        main_layout.addWidget(cache_grp)
        main_layout.addWidget(options_grp)
        main_layout.addStretch()

    def closeEvent(self, event):
        self.save_settings()

    def save_settings(self):
        s = QtCore.QSettings(StandaloneWindow.CONFIG_PATH, QtCore.QSettings.IniFormat)
        print("Saving to {0}".format(s.fileName()))

        s.beginGroup("main")
        s.setValue("window_geometry", self.geometry())
        s.setValue("temp_dir", self.temp_dir_le.text())
        s.endGroup()

        s.beginGroup("cache")
        s.setValue("cache_size", self.cache_size_sb.value())
        s.endGroup()

        s.beginGroup("options")
        s.setValue("resize_to_fit", self.resize_to_fit_cb.isChecked())
        s.setValue("endless_mouse", self.endless_mouse_cb.isChecked())
        s.endGroup()

    def load_settings(self):
        s = QtCore.QSettings(StandaloneWindow.CONFIG_PATH, QtCore.QSettings.IniFormat)
        print("Reading from {0}".format(s.fileName()))

        s.beginGroup("main")
        self.setGeometry(s.value("window_geometry", QtCore.QRect()))
        self.temp_dir_le.setText(s.value("temp_dir", str(), str))
        s.endGroup()

        s.beginGroup("cache")
        self.cache_size_sb.setValue(s.value("cache_size", 1024, int))
        s.endGroup()

        s.beginGroup("options")
        self.resize_to_fit_cb.setChecked(s.value("resize_to_fit", False, bool))
        self.endless_mouse_cb.setChecked(s.value("endless_mouse", False, bool))
        s.endGroup()

if __name__ == "__main__":
    # Create the main Qt application
    app = QtWidgets.QApplication(sys.argv)

    window = StandaloneWindow()
    window.show()

    # Enter Qt main loop (start event handling)
    app.exec_()
