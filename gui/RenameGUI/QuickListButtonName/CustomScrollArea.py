try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore


class MyScrollArea(QtWidgets.QScrollArea):
	itClickedName = QtCore.Signal(str)

	def __init__(self, parent=None, key=None):  # OriLayout = QtWidgets.QHBoxLayout()
		super(MyScrollArea, self).__init__(parent)

		self.OriLayout = QtWidgets.QHBoxLayout()
		self.key = key
		self.index = int

		scroll_style = """QScrollBar:horizontal {
                            background: rgb(10, 10, 10);
                            height: 5px;
                            margin: 0px 0 0 0px;
                        }
                        QScrollBar::handle:horizontal {
                            border: 1px rgb(0,0,0);
                            background: rgb(80, 80, 80);
                        }
                        """
		self.setObjectName("fast_access")

		self.setFixedWidth(250)

		self.setWidgetResizable(True)
		self.setAcceptDrops(True)

		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.scrollbar = QtWidgets.QScrollBar()
		self.scrollbar.setStyleSheet(scroll_style)
		self.setHorizontalScrollBar(self.scrollbar)

		self.scroll_area_widget = QtWidgets.QWidget()
		self.setWidget(self.scroll_area_widget)

		self.scroll_area_widget_layout = self.OriLayout
		# self.scroll_area_widget_layout.setAlignment(QtCore.Qt.AlignTop)
		self.scroll_area_widget_layout.setContentsMargins(0, 0, 0, 0)
		self.scroll_area_widget_layout.setSpacing(2)

		self.scroll_area_widget.setLayout(self.scroll_area_widget_layout)

		self.Add_Buttons()

	def Add_Buttons(self):
		self.json_data = get_json_data()
		self.Separator = Separator_BTN(40, 25)
		self.scroll_area_widget_layout.addWidget(self.Separator)

		for i in self.json_data[self.key]:
			self.fast_access_BTN = Buttons_fast_name(i)
			self.scroll_area_widget_layout.addWidget(self.fast_access_BTN)
			self.fast_access_BTN.itClickedName.connect(self.receiveSignal)

	def receiveSignal(self, text):
		self.itClickedName.emit(text)

	def dragLeaveEvent(self, event):

		Count = self.scroll_area_widget_layout.count()
		for num, i in enumerate(range(Count), start=1):
			widget = self.scroll_area_widget_layout.itemAt(i).widget()
			widetName = widget.objectName()
			if widetName == "Separator":
				continue
			visibl = widget.isVisible()
			if visibl == False:
				widget.setVisible(1)
				self.scroll_area_widget_layout.insertWidget(self.index, widget)

		self.Separator.setVisible(0)

	def dragEnterEvent(self, event):
		event.acceptProposedAction()

		event.source().setVisible(0)
		self.Separator.setVisible(1)

		indexX = event.pos().x() // 40

		self.scroll_area_widget_layout.insertWidget(indexX, self.Separator)
		self.index = indexX

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

		Count = self.scroll_area_widget_layout.count()
		for num, i in enumerate(range(Count), start=1):
			item = self.scroll_area_widget_layout.itemAt(i)
			widet = item.widget().objectName()
			visibl = item.widget().isVisible()

		self.Separator.setVisible(1)
		indexX = event.pos().x() // 40

		self.scroll_area_widget_layout.insertWidget(indexX, self.Separator)
		self.index = indexX

	def dropEvent(self, event):

		mimeData = event.mimeData()
		if mimeData.text():
			Name = mimeData.text()
		else:
			Name = mimeData.Name_Btn

		Count = self.scroll_area_widget_layout.count()
		indexX = (event.pos().x() // 50)

		listW = []

		Index = int
		for i in range(Count):
			item = self.scroll_area_widget_layout.itemAt(i)
			widet = item.widget().objectName()
			if Name == widet:
				Index = i

			listW.append(widet)

		self.Separator.setVisible(0)

		if Name in listW:

			widet = self.scroll_area_widget_layout.itemAt(Index).widget()
			widet.setVisible(1)
			self.scroll_area_widget_layout.insertWidget(indexX, widet)

			# print("this name [{}] already exists in [{}]".format(Name, self.objectName()))


		else:

			self.fast_access_BTN = Buttons_fast_name(Name)
			self.scroll_area_widget_layout.insertWidget(indexX, self.fast_access_BTN)
			self.fast_access_BTN.itClickedName.connect(self.receiveSignal)

			Count = self.scroll_area_widget_layout.count()

			for num, i in enumerate(range(Count), start=1):
				item = self.scroll_area_widget_layout.itemAt(i)
				widet = item.widget().objectName()

			event.source().setVisible(1)

			# print("this name [{}] move in [{}]".format(Name, self.objectName()))