from Qt import QtGui, QtCore, QtWidgets

from utilsa import Logger
logging = Logger('armada')


class LibraryTreeView(QtWidgets.QTreeView):

	librarySelectionChanged = QtCore.Signal(QtGui.QStandardItem)
	newCreate = QtCore.Signal(str)

	def __init__(self, parent=None, tree_model=None):
		"""Project tab's library tree view

		Args:
			parent:
			tree_model: tree_model.TreeModel
		"""
		super(LibraryTreeView, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building library list view...')

		self.parent = parent
		self.tree_model = tree_model
		self.setObjectName('armada_LibraryTreeView')

		# Settings
		self.setHeaderHidden(True)
		self.setMouseTracking(True)
		self.setExpandsOnDoubleClick(True)
		self.setItemsExpandable(True)
		self.setSortingEnabled(True)
		self.setIndentation(0)
		self.sortByColumn(0, QtCore.Qt.AscendingOrder)
		self.setColumnHidden(1, True)
		self.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.setMinimumWidth(200)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

		# Commands
		# self.setDpi(1)

		# Connections ---------------------
		self.selectionModel().selectionChanged.connect(self._selection_changed)
		# Renaming
		self.custom_delegate.delegateItemRenamed.connect(self._selection_changed)

	def paintEvent(self, event):
		print('empt')
		# if self.tree_model and self.tree_model.rowCount(self.rootIndex()) > 0:
		# 	print('hey')
		# else:
		self.viewport().setStyleSheet('background: transparent')
		painter = QtGui.QPainter(self.viewport())
		painter.begin()
		text = "Right click to create a folder"
		text_rect = painter.fontMetrics().boundingRect(text)
		text_rect.moveCenter(self.viewport().rect().center())
		painter.drawText(text_rect, QtCore.Qt.AlignCenter, text)
		self.paintEvent(event)

	def wheelEvent(self, event):

		delta = event.angleDelta().y()

		x = self.horizontalScrollBar().value()
		self.horizontalScrollBar().setValue(x - delta)

		y = self.verticalScrollBar().value()
		self.verticalScrollBar().setValue(y - delta)

	def setModel(self, model):
		"""Override setModel method"""
		super(LibraryTreeView, self).setModel(model)
		self.selection_model = self.selectionModel()

	def setDpi(self, dpi):
		"""Set the dots per inch multiplier.

		:type dpi: float
		:rtype: None
		"""
		size = 200 * dpi
		# self.setMinimumWidth(34 * dpi)
		self.setIconSize(QtCore.QSize(size, size))

	def _selection_changed(self):
		"""Triggered when the library item changes selection."""
		# Get current selection
		index = self.currentIndex()
		# Get index from armada model
		# index_source = self.model().mapToSource(index)

		self.logger.info(index.data(role=QtCore.Qt.UserRole))
		self.logger.info(index.data(role=QtCore.Qt.UserRole + 1))
		self.logger.info(index.data(role=QtCore.Qt.UserRole + 7))

		self.librarySelectionChanged.emit(index)

	# def index_from_path(self, path):
	# 	"""
	# 	:type path: str
	# 	:rtype: QtCore.QModelIndex
	# 	"""
	# 	# Get index
	# 	index = self.model().sourceModel().index(path)
	#
	# 	return self.model().mapFromSource(index)  # Map index from armada to sort filter

	# def set_root_path(self, path):
	# 	"""Set the model's root :path:
	# 	:type path: str
	# 	"""
	# 	# Set root path
	# 	self.setRootPath(path)
	# 	index = self.index_from_path(path)  # hide until i figure this out
	# 	# Set root index
	# 	self.setRootIndex(index)

	# def search_text_changed(self, text=None):
	# 	regExp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
	#
	# 	self.logger.info('User text = {0}'.format(text))
	#
	# 	self.proxy_model.text = text.lower()
	# 	self.proxy_model.setFilterRegExp(regExp)

	def folder_selection_changed(self, index_source=None):
		"""Called when user changes folder selection in folder view

		Args:
			index_source: index mapped back to the armada model (sent from folder tree view)
		"""

		# If selecting the pic in col 2, select column 1
		if index_source.column() == 1:
			index_source = index_source.model().index(index_source.row(), 0, index_source.parent())

		# Index ID
		index_uuid = str(index_source.data(QtCore.Qt.UserRole))
		self.proxy_model.index_selected_uuid = index_uuid
		reg_exp = QtCore.QRegExp(index_uuid, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)

		self.proxy_model.setFilterRegExp(reg_exp)

	# def toggle_sorting(self, sort):
	# 	self.proxy_model.sort(sort, self.proxy_model.sortOrder())
	#
	# def set_order(self, order):
	# 	sort_order = QtCore.Qt.SortOrder(order)
	# 	self.proxy_model.sort(0, sort_order)
	#
	# def set_role(self, role):
	# 	filter = QtCore.Qt.ItemDataRole(role)
	# 	self.proxy_model.setSortRole(filter)
	#
	# 	text = self.parent.le_search.text()
	# 	regExp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
	#
	# 	self.logger.info('User text = {0}'.format(text))
	#
	# 	self.proxy_model.text = text.lower()
	# 	self.proxy_model.setFilterRegExp(regExp)




