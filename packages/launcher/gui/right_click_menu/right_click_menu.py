import os

from Qt import QtCore
from Qt import QtWidgets

from core import armada
from packages import launcher

import utilsa
logging = utilsa.Logger('armada')

class RightClickMenu(QtWidgets.QMenu):

	def __init__(self, parent=None, index_proxy_sel=None, index_proxy_folders=None, tree_proxy=None):
		"""Right click menu with context sensitive options

		Args:
			parent:
			index_proxy_sel:
			index_proxy_folders:
			tree_proxy:
		"""
		super(RightClickMenu, self).__init__(parent)

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Right clicked...')

		self.parent = parent

		self.index_proxy_sel = index_proxy_sel
		self.index_proxy_folders = index_proxy_folders
		self.index_source_folders = self.index_proxy_folders.model().mapToSource(index_proxy_folders)

		self.tree_proxy = tree_proxy


		# Show when clicking on an item
		if self.index_proxy_sel.isValid():
			# If selecting item in col 2, select column 1
			if self.index_proxy_sel.column() != 0:
				self.index_proxy_sel = self.index_proxy_sel.model().index(
					self.index_proxy_sel.row(), 0, self.index_proxy_sel.parent()
				)
			# Cache data for dir to be deleted so model's delete_row can handle same names
			self._on_right_click()
			self._create_action("Rename", lambda: self._on_rename())
			self._create_action("Edit Thumbnail", lambda: self._on_thumbnail(self.index_proxy_sel))
			# self._create_action("Sideline", lambda: self._on_hide(self.index_proxy_sel))
			self._create_action("Delete {}".format((self.index_proxy_sel.data(QtCore.Qt.DisplayRole))), lambda: self._on_delete())

		# Only show in blank space
		else:
			# self._create_action("New Folder", self._on_new)
			self._create_menu("New", self._on_new)

	def _on_right_click(self):
		self.index_source_sel = self.index_proxy_sel.model().mapToSource(self.index_proxy_sel)
		data_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.DATA)
		json_data = armada.resource.json_read(data_path_abs)

		self.logger.info('json_data = {}'.format(json_data))

	def _create_action(self, text, slot):
		"""
		Helper function to save typing when populating menus with action.
		"""
		action = QtWidgets.QAction(text, self)
		self.addAction(action)
		action.triggered.connect(slot)
		return action

	def _create_menu(self, text, slot):
		"""
		Helper function to save typing when populating menus with action.
		"""

		# menu = QMenu(text, self)
		# self.addMenu(menu)
		self.addSection('Create')

		index_source_folders_type = self.index_source_folders.data(QtCore.Qt.UserRole + 1)
		new_types = armada.structure.get_type_data(index_source_folders_type, armada.structure.CHILDREN)

		# Standard folder option
		# action = QtWidgets.QAction("Folder", self)
		# action.setIcon(resource.color_svg('folder', 1024, '#F9D085'))
		# action.triggered.connect(slot)
		# self.addAction(action)

		# Pipeline objects
		for item in new_types:
			template_id = armada.structure.get_type_data(item, armada.structure.TEMPLATE_ID)
			# if category == 'sub_folder':
			# 	pass
			# else:
			formatted_new_type = self._format_type(template_id)
			action = QtWidgets.QAction("{}".format(formatted_new_type), self)
			icon = armada.structure.get_type_data(item, armada.structure.ICON)
			action.setIcon(armada.resource.color_svg(icon, 1024, '#F9D085'))
			data = {
				'type': item,
				'template_id': template_id
			}
			action.setData(data)
			self.addAction(action)
			action.triggered.connect(slot)

		return action

	def _format_type(self, mapped_type):
		"""
		Formats the component type name nicely for user display

		Args:
			mapped_type:

		Returns:

		"""
		formatted_type = ' '.join(x.capitalize() or '_' for x in mapped_type.split('_'))
		self.logger.debug('Formatted type = {}'.format(formatted_type))
		return formatted_type

	def _on_thumbnail(self, proxy_index):
		"""Add thumbnail to selection

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""
		self.thumbnail_popup = launcher.popup_thumbnail.ThumbnailPopup(
			parent=self,
			index_proxy_sel=self.index_proxy_sel,
			index_proxy_folders=self.index_proxy_folders,
			tree_proxy=self.tree_proxy
		)
		self.thumbnail_popup.show()

	def _on_rename(self,):
		"""
		Called when *Rename* is selected from the right click menu

		:return:
		"""
		self.rename_popup = launcher.popup_rename.RenamePopup(
			parent=self,
			index_proxy_sel=self.index_proxy_sel,
			index_proxy_folders=self.index_proxy_folders,
			tree_proxy=self.tree_proxy
		)
		self.rename_popup.show()

	def _on_delete(self):
		"""Removes a file completely

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""
		self.delete_popup = launcher.popup_delete.DeletePopup(
			parent=self,
			index_proxy_sel=self.index_proxy_sel,
			index_proxy_folders=self.index_proxy_folders,
			tree_proxy=self.tree_proxy
		)
		self.delete_popup.show()

	def _on_hide(self, proxy_index):
		"""Removes a file so you can clean up a directory, but return to it later if need be

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""
		folder_index_source = self.proxy_model.mapToSource(proxy_index)
		print('current sel = {}'.format(folder_index_source.data(QtCore.Qt.DisplayRole)))
		print('parent = {}'.format(folder_index_source.parent().data(QtCore.Qt.DisplayRole)))

		# Get folder path to index
		path_prefix = os.getenv('ARMADA_MOUNT_PREFIX')

		# Data path
		file_path_data_abs = armada.resolver.generate_path(folder_index_source, armada.resolver.DATA)

		# user path
		file_path_user_abs = armada.resolver.generate_path(folder_index_source, armada.resolver.USER)
		#
		# # Trash dir paths
		# trash_user_dir = resource.data_path(resource.data_path(
		# 	'sideline',
		# 	file_path_user_rel.rpartition(folder_index_source.data(Qt.DisplayRole))[0])
		# )
		# trash_data_dir = resource.data_path(resource.data_path(
		# 	'file_data',
		# 	file_path_data_rel.rpartition(folder_index_source.data(Qt.DisplayRole))[0])
		# )

		# # Don't make dirs if deleting a minor
		# if folder_index_source.data(Qt.UserRole + 1) != 'minor':
		# 	if not os.path.exists(trash_data_dir):
		# 		os.makedirs(trash_data_dir)
		# 	shutil.move(file_path_data_abs, trash_data_dir)
		#
		# if not os.path.exists(trash_user_dir):
		# 	os.makedirs(trash_user_dir)
		# shutil.move(file_path_user_abs, trash_user_dir)
		#
		# self.tree_proxy.removeRows(folder_index_source.row(), 1, folder_index_source.parent())
		# self.tree_proxy.dataChanged.emit(folder_index_source, folder_index_source)

	def _on_new(self):
		"""
		Called when *New* is selected from the right click menu

		:return:
		"""
		action = self.sender()

		self.new_popup = launcher.popup_new.NewPopup(
			parent=self,
			index_proxy_folders=self.index_proxy_folders,
			tree_proxy=self.tree_proxy,
			new_type=action
		)
		self.new_popup.show()

