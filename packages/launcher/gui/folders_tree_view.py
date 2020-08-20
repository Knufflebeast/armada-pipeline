import os
from Qt.QtGui import QStandardItem
from Qt.QtWidgets import QTreeView, QHeaderView, QFrame, QAbstractItemView
from Qt.QtCore import Qt, QSize, Signal

from core import armada

import utilsa
logging = utilsa.Logger('armada')


class FoldersTreeView(QTreeView):

	folderSelectionChanged = Signal(QStandardItem)
	comboSelectionChanged = Signal(QStandardItem)

	def __init__(self, parent=None):
		super(FoldersTreeView, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building folders tree view...')

		# Settings
		self.setMinimumWidth(200)
		self.setMaximumWidth(600)

		# self.setAnimated(True)
		self.setHeaderHidden(True)
		self.setMouseTracking(True)
		self.setSortingEnabled(True)
		self.setItemsExpandable(True)
		self.setRootIsDecorated(True)
		self.setExpandsOnDoubleClick(True)
		self.sortByColumn(0, Qt.AscendingOrder)
		# Size columns
		self.setFrameShape(QFrame.NoFrame)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Right click menu
		self.setContextMenuPolicy(Qt.CustomContextMenu)

		self.setStyleSheet("""
		QTreeView::branch:has-children:!has-siblings:closed,
		QTreeView::branch:closed:has-children:has-siblings {{
			image: url({0}/resources/icon/arrow_right_white.svg);
		}}
		QTreeView::branch:open:has-children:!has-siblings,
		QTreeView::branch:open:has-children:has-siblings  {{
			image: url({0}/resources/icon/arrow_down_white.svg);
		}}
		QTreeView::branch:open:has-children:!has-siblings,
		QTreeView::branch:open:has-children:has-siblings  {{
			image: url({0}/resources/icon/arrow_down_white.svg);
		}}
		""".format(armada.definitions.ROOT_PATH))

		# Commands
		# self.setDpi(1)

		# Connections ---------------------

	def header(self):
		header = super(FoldersTreeView, self).header()
		# header = self.header()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Fixed)
		header.setStretchLastSection(False)
		self.setColumnWidth(1, 50)

	def lib_drilled_down(self, index_source_drilled):
		self.logger.debug('Index drilled down: {}'.format(index_source_drilled))
		proxy_root_index = self.model().mapFromSource(index_source_drilled)
		self.setCurrentIndex(proxy_root_index)
		self.setExpanded(proxy_root_index, True)

	def setModel(self, model):
		"""Override setModel method"""
		super(FoldersTreeView, self).setModel(model)
		self.selection_model = self.selectionModel()
		self.selectionModel().selectionChanged.connect(self._selection_changed)

	def setDpi(self, dpi):
		"""
		Set the dots per inch multiplier.

		:type dpi: float
		:rtype: None
		"""
		size = 24 * dpi
		self.setIndentation(15 * dpi)
		self.setMinimumWidth(35 * dpi)
		self.setIconSize(QSize(size, size))
		self.setStyleSheet("height: {size}".format(size=size))

	def _selection_changed(self):
		"""
		Triggered when the user selects a new folder item.

		Emits itemSelectionChanged signal and sends index_source to library view
		"""
		self.logger.debug('Folder selection signal emit')

		index_proxy = self.currentIndex()
		index_source = self.model().mapToSource(index_proxy)

		self.folderSelectionChanged.emit(index_source)

	def _combo_changed(self):
		"""
		Triggered when the user changes the folder's combobox item.

		Emits the comboSelectionChanged signal and sends the index_source to library view to filter the view.

		:return:
		"""
		self.logger.debug('Combo selection signal emit')

		index_proxy = self.currentIndex()
		index_source = self.model().mapToSource(index_proxy)

		self.comboSelectionChanged.emit(index_source)

	def breadcrumb_changed(self, index_source):
		"""
		Called when the breadcrumb selection is changed.

		:param index_source:
		:return:
		"""
		index_proxy = self.model().mapFromSource(index_source)
		# self.logger.debug('Received index from breadcrumb = {}'.format(index_proxy))
		# self.logger.debug('Breadcrumb data display = {}'.format(index_proxy.data(QtCore.Qt.DisplayRole)))
		self.setCurrentIndex(index_proxy)

		# menu.exec_(self.mapToGlobal(position))

	# def path_from_index(self, index, path=''):
	# 	"""
	# 	Sets self.emit_dict so that data can be sent to library view
	#
	# 	:type index: QtCore.QModelIndex
	# 	:param str: File path (only used during recursion)
	# 	"""
	#
	# 	parent_index = index.parent()
	# 	parent_data = parent_index.data()
	# 	index_data = index.data()
	#
	# 	# If item has a parent, keep going up hierarchy
	# 	if parent_data is not None:
	# 		file_path = os.path.join(index_data, path)
	# 		self.logger.debug('Has parent path = {0}'.format(file_path))
	#
	# 		return self.path_from_index(parent_index, path=file_path)
	#
	# 	# When the root item is reached return file path
	# 	elif parent_data is None:
	# 		file_path = os.path.join(index_data, path).strip(os.path.sep)
	#
	# 		self.logger.debug('Asset file path = {0}'.format(path))
	# 		self.logger.debug('Asset file path = {0}'.format(file_path))
	#
	# 		return file_path.replace('\\', '/')


