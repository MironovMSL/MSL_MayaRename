try:
	from PySide2 import QtWidgets, QtGui, QtCore
	from shiboken2 import wrapInstance
except:
	from PySide6 import QtWidgets, QtGui, QtCore
	from shiboken6 import wrapInstance
	
from MSL_MayaRename.core.resources import Resources
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.LibraryScrollAreaWidget.MainScrollAreaLibraryWidget import MainScrollAreaLibraryWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.AdditionButtonsWidget.AdditionButtonsWidget import AdditionButtonsWidget
from MSL_MayaRename.gui.RenameGUI.QuickListButtonNameWidget.LibraryGUI.MenuWidget.MenuWidget import MenuWidget
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import sys


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LibraryWindow(QtWidgets.QDialog):
	WINDOW_TITLE = "Library"
	library_show = QtCore.Signal(bool)
	
	def __init__(self, parent=maya_main_window()):
		super(LibraryWindow, self).__init__(parent)
		# Modul---------------------------
		self.resources   = Resources.get_instance()
		# Attribute---------------------------
		self.icon        = self.resources.get_icon_from_resources("earth-svgrepo-com.svg")
		self.count_categories  = len(list(self.resources.get_key_name_JSON(key="ListName")))
		self.step_width  = 60
		self.step_height = 20
		self.target_size = None
		self.resize_anim = None
		# Setting---------------------------
		self.setWindowTitle(self.WINDOW_TITLE)
		self.setObjectName("LibraryWindowRenameToolWindowID")
		self.setWindowIcon(self.icon)
		self.setMinimumSize(240, 200)
		self.setMaximumSize(420, 355)
		self.resize(300, 355)
		# On macOS make the window a Tool to keep it on top of Maya
		if sys.platform == "darwin":
			self.setWindowFlag(QtCore.Qt.Tool, True)
		
		# Remove Title
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
		# self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
	
		# Run functions ---------------------------
		self.create_widgets()
		self.create_layouts()
		self.create_connections()
		self.set_resize(self.count_categories)
		
	def __repr__(self):
		return f"Class: [LibraryWindow], name - [{self.objectName()}]"
	
	def create_widgets(self):
		self.resize_timer = QtCore.QTimer()
		self.resize_timer.setSingleShot(True)
		
		self.MenuWidget            = MenuWidget()
		self.MainScrollArea        = MainScrollAreaLibraryWidget()
		self.AdditionButtonsWidget = AdditionButtonsWidget()
		
	def create_layouts(self):
		# main layout---------------------------
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		# add widget---------------------------
		self.main_layout.addWidget(self.MenuWidget)
		self.main_layout.addWidget(self.MainScrollArea)
		self.main_layout.addWidget(self.AdditionButtonsWidget)

	def create_connections(self):
		self.resize_timer.timeout.connect(self.applyStepResize)
		self.AdditionButtonsWidget.isCategoryName.connect(self.add_category)
		self.AdditionButtonsWidget.isSubCategoryName.connect(self.add_subCategory)
		self.MainScrollArea.itDeleteCategory.connect(lambda name: self.update_category(name=name))
		self.MainScrollArea.itUpdateCategory.connect(lambda categories: self.update_category(categories=categories))
		self.MenuWidget.save_btn.itSave.connect(self.save_library)
		self.MenuWidget.reset_btn.itReset.connect(self.reset_library)
		self.MenuWidget.duplicate_btn.itDuplicate.connect(self.duplicate_library)
	
	def build_library(self):
		categories = self.MainScrollArea.scroll_area_widget.key_name
		count_categories = self.MainScrollArea.scroll_area_widget.main_layout.count()
		lybrary = {}
		
		if categories:
			for category in categories:
				for i in range(count_categories):
					item = self.MainScrollArea.scroll_area_widget.main_layout.itemAt(i).widget()
					if item and hasattr(item, 'name') and item.name == category:
						SubCategory = item.category_widget.scroll_area_widget.word_list  # list []
						lybrary[category] = SubCategory
		return lybrary
	
	def find_duplicates(self, lybrary):
		dublicate = {}
		lybrary_list = list(lybrary.keys())
		
		for index, category_x in enumerate(lybrary_list, start=1):
			for SubC_x in lybrary[category_x]:
				if SubC_x in dublicate:
					continue
				
				duplicate_in_categories = []
				
				for category_Y in lybrary_list[index:]:
					for SubC_y in lybrary[category_Y]:
						if SubC_x == SubC_y:
							duplicate_in_categories.append(category_Y)
				
				if duplicate_in_categories:
					duplicate_in_categories.insert(0, category_x)
					dublicate[SubC_x] = duplicate_in_categories
		
		return dublicate
	
	def save_library(self):
		new_library = self.build_library()

		self.resources.JSON_data["ListName"] = new_library
		self.resources.write_json()

		self.set_state_saveButton(False)
	
	def duplicate_library(self):
		lybrary = self.build_library()
		duplicates = self.find_duplicates(lybrary)
		
		if duplicates:
			# Вычисляем максимальную длину имени среди всех категорий
			max_name_length = max(len(name) for name in duplicates.keys())
	
			# Формируем HTML-сообщение с выравниванием через таблицу
			message = "<p style='font-size: 12px; line-height: 1.5;'>Duplicate names found:</p>"
			message += "<table style='width: 100%;'>"
			for name, categories in duplicates.items():
				spaces_needed = max_name_length - len(name)
				spaces = "&nbsp;" * (spaces_needed)  # Добавляем 2 пробела для разделения
				
				# Добавляем строку в таблицу с выравниванием
				message += (
					f"<tr>"
					f"<td style='padding-right: 10px; text-align: left; color: #D16D6D;'>{name} : </td>"
					f"<td style='color: #F5A623;'>{', '.join(categories)}</td>"
					f"</tr>"
				)
				print(f"{name:<{max_name_length+2}}:{', '.join(categories)}")
			
			message += "</table>"
			
			# Создаём информационное окно
			msg_box = QtWidgets.QMessageBox(self)
			msg_box.setWindowTitle("Duplicates")
			msg_box.setIcon(QtWidgets.QMessageBox.Information)
			msg_box.setTextFormat(QtCore.Qt.RichText)  # Включаем поддержку HTML
			msg_box.setText(message)
			msg_box.exec_()
		
		else:
			print("Duplicates of Names not found")
			
	def reset_library(self):
		
		button_pressed = QtWidgets.QMessageBox.question(self, "Question", f"Are you sure you want to reset <span style='color: #669e62; font-size: {12}px;'>{'the library'}</span> to its <span style='color: #669e62; font-size: {12}px;'>{'default state'}</span>?")
		
		if button_pressed == QtWidgets.QMessageBox.Yes:
			self.resources.JSON_data["ListName"] = self.resources.JSON_data["ListNameDefault"]
			count_categories = self.MainScrollArea.scroll_area_widget.main_layout.count()
			list_categories  = list(self.resources.get_key_name_JSON(key="ListNameDefault"))
	
			for i in reversed(range(count_categories)):
				item = self.MainScrollArea.scroll_area_widget.main_layout.takeAt(i)
				widget = item.widget()
				if widget and hasattr(widget, 'name'):
					widget.deleteLater()
	
			self.MainScrollArea.scroll_area_widget.key_name = list_categories
	
			self.MainScrollArea.scroll_area_widget.add_content("ListNameDefault")
			self.update_category(self.MainScrollArea.scroll_area_widget.key_name)
			self.set_resize(len(list_categories))
		else:
			print("Cancelled")
		
	def set_resize(self, count = None):
		assert count is not None, "count is None"
		self.count_categories = count
		
		if count > 4:
			width = count * self.step_width
			self.setMaximumSize(width, 355)
			self.resize(300, 355)
		else:
			self.setMaximumSize(240, 355)
			self.resize(300, 355)

	def set_add_size(self):
		self.count_categories += 1
		width  = self.count_categories * self.step_width
		height = self.size().height()
		if self.count_categories < 10:
			self.setMaximumWidth(width)
			self.resize(width, height)
			
		else:
			self.setMaximumWidth(width)
	
	def set_minus_size(self):
		self.count_categories -= 1
		width = self.count_categories * self.step_width
		height = self.size().height()
		
		if self.count_categories > 3:
			self.setMaximumWidth(width)
			self.resize(width, height)
		else:
			pass

	def set_state_saveButton(self, bool):
		self.MenuWidget.save_btn.set_Enabled(bool)
		
	def update_category(self, name = None, categories = None):
		if categories:
			self.AdditionButtonsWidget.addSubCategoryWidget.word_list = categories
		else:
			update_categories = self.MainScrollArea.scroll_area_widget.update_list()
			self.AdditionButtonsWidget.addSubCategoryWidget.word_list = update_categories
		if name:
			self.MenuWidget.save_btn.set_Enabled(True)
			self.AdditionButtonsWidget.addSubCategoryWidget.add_item_combobox(name)
			self.set_minus_size()
		else:
			self.AdditionButtonsWidget.addSubCategoryWidget.add_item_combobox()
	
	def add_category(self, name):
		if name:
			newCategory = self.MainScrollArea.scroll_area_widget.add_category(name, main_key= None)
			if newCategory:
				self.update_category()
				self.set_state_saveButton(True)
				self.set_add_size()
				
		else:
			print("Category not added: name cannot be empty.")
			
	
	def add_subCategory(self, name, category):
		if name:
			for i in range(self.MainScrollArea.scroll_area_widget.main_layout.count()):
				item = self.MainScrollArea.scroll_area_widget.main_layout.itemAt(i).widget()
				if item and hasattr(item, 'name'):
					if item.name == category:
						newSubCategory = item.category_widget.scroll_area_widget.add_button(name)
						if newSubCategory:
							item.category_widget.scroll_area_widget.update_list()
							self.set_state_saveButton(True)
							
		else:
			print("SubCategory not added: name cannot be empty.")
	
	def closeEvent(self, event):
		self.library_show.emit(False)
	
	def resizeEvent(self, event):
		if self.resize_anim:
			if self.resize_anim.state() == QtCore.QAbstractAnimation.Running:
				return
		width = event.size().width()
		height = event.size().height()
		
		# Round the width and height to the nearest step
		new_width = (width // self.step_width) * self.step_width
		new_height = ((height - 15) // self.step_height) * self.step_height + (15)
		
		# Check if the size needs to be increased or decreased
		width_diff = width - new_width
		height_diff = height - new_height
		
		if width_diff > self.step_width / 2:
			new_width += self.step_width
		elif width_diff < -self.step_width / 2:
			new_width -= self.step_width
		
		if height_diff > self.step_height / 2:
			new_height += self.step_height
		elif height_diff < -self.step_height / 2:
			new_height -= self.step_height
		
		# Set the target size
		self.target_size = QtCore.QSize(new_width, new_height)
		
		self.resize_timer.start(300)
		super().resizeEvent(event)
	
	def applyStepResize(self):
		start_size = self.size()
		
		self.resize_anim = QtCore.QPropertyAnimation(self, b"size")
		self.resize_anim.setStartValue(start_size)
		self.resize_anim.setEndValue(self.target_size)
		self.resize_anim.setDuration(100)
		self.resize_anim.start()
		
#TODO  saving geometry UI when I close UI
#TODO  asking for save libraey if I close UI