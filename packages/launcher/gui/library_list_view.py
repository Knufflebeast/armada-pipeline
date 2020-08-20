import sys
import platform
# Use NSURL as a workaround to pyside/Qt4 behaviour for dragging and dropping on OSx
op_sys = platform.system()
if op_sys == 'Darwin':
	from Foundation import NSURL

from Qt import QtGui, QtCore, QtWidgets

from utilsa import Logger
logging = Logger('armada')


class LibraryListView(QtWidgets.QListView):

	librarySelectionChanged = QtCore.Signal(QtGui.QStandardItem)
	drillDown = QtCore.Signal(QtCore.QModelIndex)

	def __init__(self, parent=None, tree_model=None):
		super(LibraryListView, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building library list view...')

		self.parent = parent
		self.tree_model = tree_model

		# Settings
		self.setWrapping(True)
		self.setMouseTracking(True)
		self.setMovement(self.Static)
		self.setUniformItemSizes(True)
		self.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.setFlow(QtWidgets.QListView.LeftToRight)
		self.setViewMode(QtWidgets.QListView.IconMode)
		self.setResizeMode(QtWidgets.QListView.Adjust)
		self.setHorizontalScrollMode(QtWidgets.QListView.ScrollPerPixel)
		self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.setAcceptDrops(True)
		# Context Menu
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		# Size
		self.setMinimumHeight(500)
		self.setMinimumWidth(400)
		self.setSpacing(10)

		# Commands
		# self.setDpi(1)

	def setModel(self, model):
		"""Override setModel method"""
		super(LibraryListView, self).setModel(model)
		self.selection_model = self.selectionModel()
		self.selectionModel().selectionChanged.connect(self._selection_changed)

	def wheelEvent(self, event):

		delta = event.angleDelta().y()

		x = self.horizontalScrollBar().value()
		self.horizontalScrollBar().setValue(x - delta)

		y = self.verticalScrollBar().value()
		self.verticalScrollBar().setValue(y - delta)

	def mousePressEvent(self, event):
		if not self.indexAt(event.pos()).isValid():
			self.selectionModel().clear()
		super(LibraryListView, self).mousePressEvent(event)

	# def load_image(self):
	# 	"""
	# 	Set the image to the pixmap
	# 	:return:
	# 	"""
	# 	pixmap = QtGui.QPixmap(self.fname)
	# 	pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
	# 	self.lbl.setPixmap(pixmap)
	#
	# # The following three methods set up dragging and dropping for the app
	# def dragEnterEvent(self, e):
	# 	if e.mimeData().hasUrls:
	# 		e.accept()
	# 	else:
	# 		e.ignore()
	#
	# def dragMoveEvent(self, e):
	# 	if e.mimeData().hasUrls:
	# 		e.accept()
	# 	else:
	# 		e.ignore()
	#
	# def dropEvent(self, e):
	# 	"""
	# 	Drop files directly onto the widget
	# 	File locations are stored in fname
	# 	:param e:
	# 	:return:
	# 	"""
	# 	if e.mimeData().hasUrls:
	# 		e.setDropAction(QtCore.Qt.CopyAction)
	# 		e.accept()
	# 		# Workaround for OSx dragging and dropping
	# 		for url in e.mimeData().urls():
	# 			if op_sys == 'Darwin':
	# 				fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
	# 			else:
	# 				fname = str(url.toLocalFile())
	# 		print(fname.rpartition('.')[0] + '.' + fname.rpartition('.')[2].lower())
	#
	# 		self.fname = fname
	# 		self.load_image()
	# 	else:
	# 		e.ignore()

	def mouseDoubleClickEvent(self, event):
		"""When an item is double clicked in the library_list_view it emits a signal to folder_tree_view's
		lib_drilled_down method. This will change the folder's selected item to be the item double clicked in the
		library. A selection change in folder_tree_view will trigger the cascading view update on all other views.

		:param event:
		:return:
		"""
		# Filter
		index_proxy = self.currentIndex()
		if index_proxy.isValid():
			# Don't drill down through major_components
			if not index_proxy.data(QtCore.Qt.UserRole + 19) == 'major_component':
				index_source = self.model().mapToSource(index_proxy)
				self.drillDown.emit(index_source)

		event.accept()

	def setDpi(self, dpi):
		"""
		Set the dots per inch multiplier.

		:type dpi: float
		:rtype: None
		"""
		size = 24 * dpi
		self.setMinimumWidth(35 * dpi)
		self.setIconSize(QtCore.QSize(size, size))
		self.setStyleSheet("height: {size}".format(size=size))

	def _selection_changed(self):
		"""Triggered when the user selects a new library item.

		Emits librarySelectionChanged signal and sends index_source to selected_widget
		"""
		self.logger.debug('Library selection signal emit')

		index_proxy = self.currentIndex()
		index_source = self.model().mapToSource(index_proxy)

		self.librarySelectionChanged.emit(index_source)

	# def current_folder_selection(self):
	# 	# Get current selection
	# 	index = self.currentIndex()
	# 	return self.item_from_index(index)

	# def index_from_path(self, path):
	# 	"""
	# 	:type path: str
	# 	:rtype: QtCore.QModelIndex
	# 	"""
	# 	# Get index
	# 	index = self.model().sourceModel().index(path)
	# 	# Map index from armada to sort filter
	# 	return self.model().mapFromSource(index)
	#
	# def set_root_path(self, path):
	# 	"""Set the model's root :path:
	# 	:type path: str
	# 	"""
	# 	# Set root path
	# 	self.setRootPath(path)
	# 	index = self.index_from_path(path)  # hide until i figure this out
	# 	# Set root index
	# 	self.setRootIndex(index)
	#
	# def search_text_changed(self, text=None):
	# 	regExp = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
	#
	# 	self.logger.info('User text = {0}'.format(text))
	#
	# 	self.model().text = text.lower()
	# 	self.model().setFilterRegExp(regExp)

	def folder_selection_changed(self, index_source=None):
		"""Called when user changes folder selection in folder view

		Args:
			index_source: index mapped back to the armada model (sent from folder tree view)
		"""
		self.clearSelection()

		if index_source.column() == 1:
			index_source_col1 = index_source.model().index(index_source.row(), 0, index_source.parent())
			index_source = index_source_col1

		# Filter
		index_uuid = str(index_source.data(QtCore.Qt.UserRole))
		self.model().index_selected_uuid = index_uuid

		reg_exp = QtCore.QRegExp(index_uuid, QtCore.Qt.CaseSensitive, QtCore.QRegExp.FixedString)
		self.model().setFilterRegExp(reg_exp)

		proxy_root_index = self.model().mapFromSource(index_source)
		self.setRootIndex(proxy_root_index)

	def toggle_sorting(self, sort):
		self.model().sort(sort, self.model().sortOrder())

	def set_order(self, order):
		sort_order = QtCore.Qt.SortOrder(order)
		self.model().sort(0, sort_order)

	def set_role(self, role):
		filter = QtCore.Qt.ItemDataRole(role)
		self.model().setSortRole(filter)

		text = self.parent.le_search.text()
		regExp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)

		self.logger.info('User text = {0}'.format(text))

		self.model().text = text.lower()
		self.model().setFilterRegExp(regExp)

