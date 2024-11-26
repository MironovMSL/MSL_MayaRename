try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore
    
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.CacheScrollArea import CacheScrollArea


class CacheWidget(QtWidgets.QWidget):
    
    def __init__(self, parent = None):
        super(CacheWidget, self).__init__(parent)
        
        # Attribute---------------------------
        # Setting---------------------------
        self.setFixedHeight(30)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_Widgets(self):
        self.scroll_area = CacheScrollArea()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.scroll_area)
        
    def create_connections(self):
        pass

        
        