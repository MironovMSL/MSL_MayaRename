from MSL_MayaRename.gui.mainGui import MainToolWindow
import maya.cmds as cmds
import os

root_ = os.path.dirname(__file__)

win = None  # Глобальная переменная для хранения текущего экземпляра окна

def show_main_window():
	if cmds.window("MainRenameToolWindowID", exists=True):
		cmds.deleteUI("MainRenameToolWindowID")
	
	if cmds.windowPref("MainRenameToolWindowID", exists=1):
		cmds.windowPref("MainRenameToolWindowID", remove=1)
	
	if cmds.window("LibraryWindowRenameToolWindowID", exists=True):
		cmds.deleteUI("LibraryWindowRenameToolWindowID")
	
	if cmds.windowPref("LibraryWindowRenameToolWindowID", exists=1):
		cmds.windowPref("LibraryWindowRenameToolWindowID", remove=1)
		
	win = MainToolWindow()
	win.show()