import os
import shutil
# from pathlib import Path

from Qt.QtGui import QStandardItem
from Qt.QtCore import Qt, QRegExp, QSize, Signal, QModelIndex
from Qt.QtWidgets import QListView, QFrame, QAbstractItemView, QMenu, QAction

from core import armada

import utilsa
logging = utilsa.Logger('armada')


class MinorsListView(QListView):

	minorSelectionChanged = Signal(QStandardItem)
	newCreate = Signal(str)
	softwareLaunched = Signal(QModelIndex)

	def __init__(self, parent=None, tree_model=None):
		super(MinorsListView, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building selected list view...')

		self.parent = parent
		self.tree_model = tree_model

		# Settings
		self.setWrapping(False)
		self.setMovement(self.Static)
		self.setUniformItemSizes(True)
		self.setFrameShape(QFrame.NoFrame)
		self.setFlow(QListView.TopToBottom)
		# self.setResizeMode(QListView.Adjust)
		# self.setSelectionMode(QtWidgets.QTreeWidget.ExtendedSelection)
		self.setVerticalScrollMode(QListView.ScrollPerPixel)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

		# Commands
		# self.setDpi(1)

		# Renaming
		# self.custom_delegate.delegateItemRenamed.connect(self._selection_changed)

	def mouseDoubleClickEvent(self, event):
		"""When an item is double clicked in the library_list_view it emits a signal to folder_tree_view's
		lib_drilled_down method. This will change the folder's selected item to be the item double clicked in the
		library. A selection change in folder_tree_view will trigger the cascading view update update on all other views.

		:param event:
		:return:
		"""
		index_proxy = self.currentIndex()
		index_source = self.model().mapToSource(index_proxy)

		self.softwareLaunched.emit(index_source)

	def update_widget(self, index_source=None):

		if index_source.isValid():
			if index_source.column() == 1:
				index_source_col1 = index_source.model().index(index_source.row(), 0, index_source.parent())
				index_source = index_source_col1

			# Update list
			if index_source.data(Qt.UserRole + 19) != 'major_component':
				self.hide()
			else:
				self.show()

				index_uuid = str(index_source.data(Qt.UserRole))
				self.model().index_selected_uuid = index_uuid

				reg_exp = QRegExp(index_uuid, Qt.CaseInsensitive, QRegExp.FixedString)
				self.model().setFilterRegExp(reg_exp)

				proxy_root_index = self.model().mapFromSource(index_source)
				self.setRootIndex(proxy_root_index)

	def setModel(self, model):
		"""Override setModel method"""
		super(MinorsListView, self).setModel(model)
		self.selection_model = self.selectionModel()
		self.selectionModel().selectionChanged.connect(self._selection_changed)

	def wheelEvent(self, event):

		delta = event.angleDelta().y()

		x = self.horizontalScrollBar().value()
		self.horizontalScrollBar().setValue(x - delta)

		y = self.verticalScrollBar().value()
		self.verticalScrollBar().setValue(y - delta)

	def setDpi(self, dpi):
		"""
		Set the dots per inch multiplier.

		:type dpi: float
		:rtype: None
		"""
		size = 200 * dpi
		# self.setMinimumWidth(34 * dpi)
		self.setIconSize(QSize(size, size))

	def _selection_changed(self):
		"""Triggered when the user selects a new folder item.

		Emits librarySelectionChanged signal and sends index_source to selected_widget
		"""
		self.logger.debug('Minor selection signal emit')

		index_proxy = self.currentIndex()
		index_source = self.model().mapToSource(index_proxy)  # change to proxy model?

		self.minorSelectionChanged.emit(index_source)

	def current_folder_selection(self):
		# Get current selection
		index = self.currentIndex()
		return self.item_from_index(index)

	def item_from_index(self, index):
		"""
		:type index: QtCore.QModelIndex
		:rtype: str
		"""
		# Get index from armada model
		index = self.model().mapToSource(index)
		return index

	def index_from_path(self, path):
		"""
		:type path: str
		:rtype: QtCore.QModelIndex
		"""
		# Get index
		index = self.model().sourceModel().index(path)
		# Map index from armada to sort filter
		return self.model().mapFromSource(index)

	def set_root_path(self, path):
		"""Set the model's root :path:
		:type path: str
		"""
		# Set root path
		self.setRootPath(path)
		index = self.index_from_path(path)  # hide until i figure this out
		# Set root index
		self.setRootIndex(index)

	def search_text_changed(self, text=None):
		regExp = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)

		self.logger.info('User text = {0}'.format(text))

		self.model().text = text.lower()
		self.model().setFilterRegExp(regExp)

	def folder_selection_changed(self, index_source=None):
		"""Called when user changes folder selection in folder view

		Args:
			index_source: index mapped back to the armada model (sent from folder tree view)
		"""
		if index_source.column() == 1:
			index_source_col1 = index_source.model().index(index_source.row(), 0, index_source.parent())
			index_source = index_source_col1

		# Filter
		index_uuid = str(index_source.data(Qt.UserRole))
		self.model().index_selected_uuid = index_uuid

		reg_exp = QRegExp(index_uuid, Qt.CaseInsensitive, QRegExp.FixedString)
		self.model().setFilterRegExp(reg_exp)

		proxy_root_index = self.model().mapFromSource(index_source)
		self.setRootIndex(proxy_root_index)

	def _right_click_menu(self, position):
		"""
		Right click menu

		:param position:
		:return:
		"""
		self.click_position = position
		menu_index = self.indexAt(position)

		rc_menu = QMenu()
		act_new = self._create_action("New", rc_menu, self._on_new)
		act_thumbnail = self._create_action("Add Thumbnail", rc_menu, self._on_thumbnail(menu_index))
		act_sideline = self._create_action("Sideline", rc_menu, lambda: self._on_sideline(menu_index))
		act_delete = self._create_action("Delete {}".format((menu_index.data(Qt.DisplayRole))), rc_menu, lambda: self._on_delete(menu_index))

		rc_menu.exec_(self.viewport().mapToGlobal(self.click_position))
		# menu.exec_(self.mapToGlobal(position))

	def _create_action(self, text, menu, slot):
		"""
		Helper function to save typing when populating menus with action.
		"""
		action = QAction(text, self)
		menu.addAction(action)
		action.triggered.connect(slot)
		return action

	def _on_thumbnail(self, proxy_index):
		"""Add thumbnail to selection

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""

	def _on_delete(self, proxy_index):
		"""Removes a file completely

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""

		folder_index_source = self.model().mapToSource(proxy_index)
		# folder_type = folder_index_source.data(Qt.UserRole + 1)
		template_id = folder_index_source.data(Qt.UserRole + 19)
		print('current sel = {}'.format(folder_index_source.data(Qt.DisplayRole)))
		print('parent = {}'.format(folder_index_source.parent().data(Qt.DisplayRole)))

		# Delete data dir for all non major/minor selections
		if not template_id == 'minor_component':
			# Data path abs
			data_path_abs = armada.resolver.generate_path(folder_index_source, armada.resolver.DATA)

			# Delete data dir
			if os.path.exists(data_path_abs):
				shutil.rmtree(data_path_abs)

			# User path abs
			user_path_abs = armada.resolver.generate_path(folder_index_source, armada.resolver.USER)

			# Delete user dir
			if os.path.exists(user_path_abs):
				shutil.rmtree(user_path_abs)

			# Remove index from model
			self.tree_model.removeRows(folder_index_source.row(), 1, folder_index_source.parent())
			self.tree_model.dataChanged.emit(folder_index_source, folder_index_source)

		# # If selected item is a minor file
		# else:
		# 	# Delete data dir
		# 	data_path_abs = resolver.generate_path(folder_index_source, resolver.DATA)
		#
		# 	# Delete the file if it has already been made
		# 	if os.path.exists(data_path_abs):
		# 		shutil.rmtree(data_path_abs)
		#
		# 	user_path_abs = resolver.generate_path(folder_index_source, resolver.USER)
		#
		# 	# Delete the file if it has already been made
		# 	if os.path.exists(user_path_abs):
		# 		shutil.rmtree(user_path_abs)
		#
		# 	# If all minors have been deleted, delete the major
		# 	major_data_path_abs = resolver.generate_path(folder_index_source.parent(), resolver.DATA)
		#
		# 	pathin = Path(major_data_path_abs)
		# 	major_children = [f for f in pathin.iterdir() if f.is_dir()]
		#
		# 	if not major_children:
		#
		# 		# Remove index from model
		# 		self.tree_model.removeRows(folder_index_source.parent().row(), 1, folder_index_source.parent().parent())
		# 		self.tree_model.dataChanged.emit(folder_index_source.parent(), folder_index_source.parent())
		#
		# 		# Delete the file if it has already been made
		# 		# Delete user dir
		# 		if os.path.exists(major_data_path_abs):
		# 			shutil.rmtree(major_data_path_abs)
		#
		# 	else:
		# 		# Remove index from model
		# 		self.tree_model.removeRows(folder_index_source.row(), 1, folder_index_source.parent())
		# 		self.tree_model.dataChanged.emit(folder_index_source, folder_index_source)

		print("POOF! It's gone!")

	# def toggle_sorting(self, sort):
	# 	self.model().sort(sort, self.model().sortOrder())
	#
	# def set_order(self, order):
	# 	sort_order = Qt.SortOrder(order)
	# 	self.model().sort(0, sort_order)
	#
	# def set_role(self, role):
	# 	filter = Qt.ItemDataRole(role)
	# 	self.model().setSortRole(filter)
	#
	# 	text = self.parent.le_search.text()
	# 	regExp = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
	#
	# 	self.logger.info('User text = {0}'.format(text))
	#
	# 	self.model().text = text.lower()
	# 	self.model().setFilterRegExp(regExp)

