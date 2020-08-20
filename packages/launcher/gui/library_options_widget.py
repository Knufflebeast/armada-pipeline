from Qt import QtWidgets, QtCore

from core import armada

from utilsa import Logger
logging = Logger('armada')


class LibraryOptionsWidget(QtWidgets.QWidget):
	"""Creates search options next to the search line edit
	"""

	sort_state = QtCore.Signal(bool)
	order_state = QtCore.Signal(int)
	role_state = QtCore.Signal(int)

	def __init__(self, parent=None):
		super(LibraryOptionsWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

		# GUI
		# self.lbl_sort_options = QtWidgets.QLabel('Options')
		# self.chb_sort = QtWidgets.QCheckBox('Sort')
		# self.chb_sort.toggle()
		self.btn_filter = QtWidgets.QPushButton(armada.resource.color_svg('filter', 128, '#9E9E9E'), "Filter")
		self.btn_filter.setObjectName('Filter')
		self.btn_filter.setIconSize(QtCore.QSize(20, 20))
		self.btn_filter.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_filter.setMinimumSize(60, 30)
		self.btn_combo_sort = QtWidgets.QPushButton(armada.resource.color_svg('sort', 128, '#9E9E9E'), "Sort")
		self.btn_combo_sort.setObjectName('Sort')
		self.btn_combo_sort.setIconSize(QtCore.QSize(20, 20))
		self.btn_combo_sort.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_combo_sort.setMinimumSize(60, 30)
		self.btn_refresh = QtWidgets.QPushButton(armada.resource.color_svg('refresh', 128, '#9E9E9E'), "Refresh")
		self.btn_refresh.setObjectName('Refresh')
		self.btn_refresh.setIconSize(QtCore.QSize(20, 20))
		self.btn_refresh.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_filter.setMinimumSize(60, 30)
		# self.comb_sort_order = QtWidgets.QComboBox()
		# self.comb_sort_order.addItem('Ascending', QtCore.Qt.AscendingOrder)
		# self.comb_sort_order.addItem('Descending', QtCore.Qt.DescendingOrder)
		# self.comb_sort_order.setEnabled(True)
		# self.comb_sort_order.setMinimumWidth(120)
		# self.comb_sort_order.setMinimumHeight(20)
		# self.lbl_search_options = QtWidgets.QLabel('Context: ')
		# self.name_filter = QtWidgets.QCheckBox('Name')
		# self.name_filter.toggle()
		# self.creator_filter = QtWidgets.QCheckBox('Creator')
		# self.status_filter = QtWidgets.QCheckBox('Status')

		# Layout
		self.main_layout = QtWidgets.QHBoxLayout()
		# self.main_layout.addWidget(self.lbl_sort_options)
		# self.main_layout.addWidget(self.chb_sort)
		self.main_layout.addWidget(self.btn_filter)
		self.main_layout.addWidget(self.btn_combo_sort)
		self.main_layout.addWidget(self.btn_refresh)
		# self.main_layout.addWidget(self.lbl_search_options)
		# self.main_layout.addWidget(self.name_filter)
		# self.main_layout.addWidget(self.creator_filter)
		# self.main_layout.addWidget(self.status_filter)
		# self.main_layout.setSpacing(10)
		self.main_layout.setContentsMargins(0, 0, 0, 0)


		self.setLayout(self.main_layout)

		# self.name_filter.pressed.connect(self.on_name)
		# self.creator_filter.pressed.connect(self.on_creator)
		# self.status_filter.pressed.connect(self.on_status)
		# self.chb_sort.pressed.connect(self.on_sort)
		# self.comb_sort_order.activated.connect(self.on_order)

	def on_sort(self):
		"""Sorting on/off
		"""
		self.sort_state.emit(self.chb_sort.isChecked())
		if self.comb_sort_order.isEnabled():
			self.comb_sort_order.setEnabled(False)
		else:
			self.comb_sort_order.setEnabled(True)

	def on_order(self):
		"""Ascending or descening
		"""
		self.order_state.emit(self.comb_sort_order.itemData(self.comb_sort_order.currentIndex()))

	def on_name(self):
		"""Toggle other checkboxes off
		"""
		self.creator_filter.setChecked(False)
		self.status_filter.setChecked(False)
		self.role_state.emit(QtCore.Qt.DisplayRole)

	def on_creator(self):
		"""Toggle other checkboxes off
			"""
		self.status_filter.setChecked(False)
		self.name_filter.setChecked(False)
		self.role_state.emit(QtCore.Qt.UserRole + 2)

	def on_status(self):
		"""Toggle other checkboxes off
			"""
		self.creator_filter.setChecked(False)
		self.name_filter.setChecked(False)
		self.role_state.emit(QtCore.Qt.UserRole + 4)

