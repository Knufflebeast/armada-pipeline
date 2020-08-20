"""
browser_popup

Equivalent to projects_widget

Main Module
"""

import os

from Qt.QtWidgets import QBoxLayout, QHBoxLayout, QSizePolicy, QSplitter, QDialog
from Qt import QtCore

from core import armada
from packages import launcher
from packages import marina

import utilsa
logging = utilsa.Logger('marina')

software = os.getenv('_SOFTWARE')


class BrowserPopup(QDialog):

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self, parent=None, major_index=None, tree_model=None):
		super(BrowserPopup, self).__init__()

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.warning('Building library popup window...')

		self.parent = parent
		self.tree_model = tree_model
		self.major_index = major_index

		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(armada.resource.style_sheet('main_window'))

		# Variables
		self.software = os.getenv('_SOFTWARE')

		self.logger.info('Software : {0}'.format(self.software))

		# self.sizeHint()
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		self.setStyleSheet(armada.resource.style_sheet('main_window'))
		self.setObjectName('mmm_libary_popup')

		# -----------------------------------------------------------
		# GUI -------------------------------------------------------

		######################################################
		# Folder view
		folders_proxy_model = launcher.folders_proxy_model.FoldersProxyModel(self)
		folders_proxy_model.setSourceModel(self.tree_model)

		self.folders_view = launcher.folders_tree_view.FoldersTreeView(self)
		self.folders_view.setModel(folders_proxy_model)
		folders_delegate = launcher.folders_item_delegate.FoldersItemDelegate(self)
		self.folders_view.setItemDelegate(folders_delegate)
		self.folders_view.header()
		self.folders_view.setMinimumWidth(300)

		# Startup selection
		proxy_root_index = self.folders_view.model().mapFromSource(self.tree_model.index(0, 0))
		proxy_current_index = self.folders_view.model().mapFromSource(self.tree_model.index(self.major_index.parent().row(), 0, self.major_index.parent().parent()))

		self.folders_view.expand(proxy_root_index)
		self.folders_view.setRootIndex(proxy_root_index)
		self.folders_view.setCurrentIndex(proxy_current_index)
		self.folders_view._selection_changed()

		#####################################################
		# Library view
		library_proxy_model = launcher.library_proxy_model.LibraryProxyModel()
		library_proxy_model.setSourceModel(self.tree_model)
		self.library_view = launcher.library_list_view.LibraryListView(self)
		self.library_view.setModel(library_proxy_model)
		library_delegate = launcher.library_item_delegate.LibraryItemDelegate(self)
		self.library_view.setItemDelegate(library_delegate)

		# Startup selection
		proxy_lib_root_index = self.library_view.model().mapFromSource(self.tree_model.index(self.major_index.parent().row(), 0, self.major_index.parent().parent()))
		self.library_view.setRootIndex(proxy_lib_root_index)
		index_proxy = self.library_view.model().mapFromSource(self.major_index)
		self.library_view.setCurrentIndex(index_proxy)

		#####################################################
		# Breadcrumb bar
		index_major = self.tree_model.index(self.major_index.parent().row(), 0, self.major_index.parent().parent())
		self.breadcrumb_bar_widget = launcher.breadcrumb_widget.BreadcrumbWidget(self, index_source=index_major)
		self.breadcrumb_bar_widget.setContentsMargins(0, 0, 0, 0)

		# ---------------------------------------
		# Layout --------------------------------

		self.lib_split = QSplitter(QtCore.Qt.Horizontal)
		self.lib_split.addWidget(self.folders_view)
		self.lib_split.addWidget(self.library_view)
		self.lib_split.setChildrenCollapsible(True)
		self.lib_split.setHandleWidth(1)
		self.lib_split.setStretchFactor(1, 1)

		self.lib_layout = QBoxLayout(QBoxLayout.TopToBottom)
		self.lib_layout.addWidget(self.breadcrumb_bar_widget)
		self.lib_layout.addWidget(self.lib_split)
		self.lib_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QHBoxLayout(self)
		self.main_layout.addLayout(self.lib_layout)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.main_layout)

		# Connections ------------------------------------
		# Update library
		self.folders_view.folderSelectionChanged.connect(self.library_view.folder_selection_changed)

		# Update breadcrumbs
		self.folders_view.folderSelectionChanged.connect(self.breadcrumb_bar_widget.tabbar_crumbs.folder_selection_changed)

		# Update folders view
		self.breadcrumb_bar_widget.tabbar_crumbs.breadcrumbSelectionChanged.connect(self.folders_view.breadcrumb_changed)
		self.library_view.drillDown.connect(self.folders_view.lib_drilled_down)

		# Right click menu
		self.library_view.customContextMenuRequested.connect(self._library_right_click_menu)
		self.folders_view.customContextMenuRequested.connect(self._folder_right_click_menu)

		return
		# # Connections
		# self.esc_pressed.connect(self.on_cancel_pressed)
	#
	# def on_cancel_pressed(self):
	# 	self.hide()

	# def eventFilter(self, source, event):
	# 	"""
	# 	Close window on focus exit of popup
	# 	# """
	# 	# if event.type() == QEvent.WindowDeactivate:
	# 	# 	self.close()
	# 	# if event.type() == QtCore.QEvent.Close:
	# 	# 	self.close()
	# 	# return true here to bypass default behaviour
	# 	return super(BrowserPopup, self).eventFilter(source, event)

	def _library_right_click_menu(self, position):
		"""
		Right click menu

		:param position:
		:return:
		"""
		# View selection
		click_position = position
		index_proxy_sel = self.library_view.indexAt(position)

		# Folder selection
		index_proxy_folders = self.folders_view.currentIndex()

		rc_menu = launcher.right_click_menu.RightClickMenu(self, index_proxy_sel, index_proxy_folders, self.folders_view.model())

		rc_menu.exec_(self.library_view.viewport().mapToGlobal(click_position))

	def _folder_right_click_menu(self, position):
		"""
		Right click menu

		:param position:
		:return:
		"""

		# View selection
		click_position = position
		index_proxy_sel = self.folders_view.indexAt(position)

		# Folder selection
		index_proxy_folders = self.folders_view.currentIndex()

		rc_menu = launcher.right_click_menu.RightClickMenu(self, index_proxy_sel, index_proxy_folders, self.folders_view.model())

		rc_menu.exec_(self.folders_view.viewport().mapToGlobal(click_position))

	# def keyPressEvent(self, event):
	# 	if event.key() == QtCore.Qt.Key_Return:
	# 		self.enter_pressed.emit(self.enter_signal_str)
	# 		return True
	# 	if event.key() == QtCore.Qt.Key_Escape:
	# 		self.esc_pressed.emit(self.esc_signal_str)
	# 		return True
	# 	else:
	# 		super(BrowserPopup, self).keyPressEvent(event)