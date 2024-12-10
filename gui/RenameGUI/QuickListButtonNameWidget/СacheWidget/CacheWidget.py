try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore
    
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.CacheScrollArea import CacheScrollArea
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.СacheWidget.DeleteCacheButtonWidget import DeleteCacheButtonWidget
from MSL_MayaRename.core.resources import Resources

class CacheWidget(QtWidgets.QWidget):
    itClickedCache = QtCore.Signal(str)
    
    def __init__(self, parent = None):
        super(CacheWidget, self).__init__(parent)
        # Module----------------------
        self.resources = Resources.get_instance()
        # Attribute----------------------
        self.show_cache = self.resources.config.get_variable("library", "show_cache", False, bool)
        # Attribute---------------------------
        # Setting---------------------------
        self.setFixedHeight(30)
        self.setVisible(self.show_cache)
        # Run functions ---------------------------
        self.create_Widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_Widgets(self):
        self.scroll_area = CacheScrollArea()
        self.delete_btn  = DeleteCacheButtonWidget()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.delete_btn)
        
        self.main_layout.setAlignment(self.delete_btn, QtCore.Qt.AlignTop)
        
    def create_connections(self):
        self.delete_btn.clicked.connect(self.on_clear)
        self.scroll_area.itClickedCache.connect(lambda name: self.itClickedCache.emit(name))
        
    def on_clear(self):
        self.scroll_area.scroll_area_widget.clear_layout()
        