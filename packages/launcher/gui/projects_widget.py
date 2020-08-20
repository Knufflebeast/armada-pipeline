""".. _projects_widget:

mb_armada.gui.projects_context.projects_widget
**********************************************

Module for main ProjectsWidget

The ProjectTab is a project level context where users browse for files on a project level
"""
import os
import collections

try:
	collectionsAbc = collections.abc
except AttributeError:
	collectionsAbc = collections

import jsonschema

from Qt.QtCore import Qt, QSize, QRegExp
from Qt.QtWidgets import QWidget, QFrame, QSizePolicy, QPushButton, QBoxLayout, QSpacerItem, QSplitter, QVBoxLayout

from core import armada
from packages import launcher


from utilsa import Logger
logging = Logger('armada')


class ProjectsWidget(QWidget):
	"""
	Fills projects UI with contents

	Connection gets data from folders_tree_view and sends it to assets_tree_view
	"""

	def __init__(self, parent=None):
		super(ProjectsWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building projects tab...')

		self.parent = parent
		self.setObjectName('ProjectsWidget')

		#####################################
		# Model
		# If config isn't setup run setup
		if os.getenv('ARMADA_MOUNT_PREFIX') == '':
			# Mount point setup
			launcher.armada_setup.ArmadaSetupPopup()

		else:
			pass

		data_root_path = armada.resource.data_path()
		self.tree_model = armada.tree_model.TreeModel(self, data_root_path)
		library_data = self.tree_model.create_data_dict(data_root_path, depth=3, depth_toggle=armada.tree_model.TreeModel.DEPTH_ON)
		self.tree_model.fill_model(library_data)

		self.file_system_watcher = armada.directory_watcher.Watcher(armada.resource.data_path('Projects'))
		self.file_system_watcher.run()

		# Projects root
		root_index = self.tree_model.index(0, 0)

		#######################################
		# Folders view
		folders_proxy_model = launcher.folders_proxy_model.FoldersProxyModel(self)
		folders_proxy_model.setSourceModel(self.tree_model)
		self.folders_view = launcher.folders_tree_view.FoldersTreeView(self)
		self.folders_view.setModel(folders_proxy_model)
		self.folders_delegate = launcher.folders_item_delegate.FoldersItemDelegate(self)
		self.folders_view.setItemDelegate(self.folders_delegate)
		self.folders_view.header()

		# Startup location
		proxy_root_index = self.folders_view.model().mapFromSource(root_index)
		self.folders_view.expand(proxy_root_index)
		self.folders_view.setRootIndex(proxy_root_index)
		self.folders_view.setCurrentIndex(proxy_root_index)

		########################################
		# Library view
		library_proxy_model = launcher.library_proxy_model.LibraryProxyModel(self)
		library_proxy_model.setSourceModel(self.tree_model)
		self.library_view = launcher.library_list_view.LibraryListView(self)
		self.library_view.setModel(library_proxy_model)
		self.library_delegate = launcher.library_item_delegate.LibraryItemDelegate(self)
		self.library_view.setItemDelegate(self.library_delegate)

		# Startup location
		proxy_root_index = self.library_view.model().mapFromSource(root_index)
		project_root_uuid = "000"
		self.library_view.model().index_selected_uuid = project_root_uuid
		reg_exp = QRegExp(project_root_uuid, Qt.CaseSensitive, QRegExp.FixedString)
		self.library_view.model().setFilterRegExp(reg_exp)
		self.library_view.setRootIndex(proxy_root_index)

		##########################################
		# Selected widget
		self.selected_widget = launcher.selected_widget.SelectedWidget(self, self.tree_model)

		self.lineB = QFrame()
		self.lineB.setFixedHeight(1)
		self.lineB.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.lineB.setStyleSheet("background-color: #636363;")

		# Back Button
		self.btn_back = QPushButton()
		self.btn_back.setFixedSize(30, 30)
		self.icon = armada.resource.color_svg('arrow_up', 128, '#FFFFFF')
		self.btn_back.setIcon(self.icon)
		self.btn_back.setIconSize(QSize(40, 40))
		self.btn_back.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))

		###############################################
		# Breadcrumb Bar
		self.breadcrumb_bar_widget = launcher.breadcrumb_widget.BreadcrumbWidget(self, root_index)
		self.breadcrumb_bar_widget.setContentsMargins(0, 0, 0, 0)

		# Filter options
		self.library_options_widget = launcher.library_options_widget.LibraryOptionsWidget(self)

		# Layout
		self.header_layout = QBoxLayout(QBoxLayout.LeftToRight)
		self.header_layout.addWidget(self.btn_back)
		self.header_layout.addWidget(self.breadcrumb_bar_widget)
		spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.header_layout.addSpacerItem(spacer)
		self.header_layout.addWidget(self.library_options_widget)
		self.header_layout.setContentsMargins(0, 0, 0, 0)
		self.header_layout.setStretch(0, 1)

		self.asset_split = QSplitter(Qt.Horizontal)
		self.asset_split.addWidget(self.folders_view)
		self.asset_split.addWidget(self.library_view)
		self.asset_split.addWidget(self.selected_widget)
		self.asset_split.setChildrenCollapsible(False)
		self.asset_split.setHandleWidth(1)
		self.asset_split.setStretchFactor(1, 1)
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)

		self.vert_layout = QBoxLayout(QBoxLayout.TopToBottom)
		self.vert_layout.addLayout(self.header_layout)
		self.vert_layout.addWidget(self.lineB)
		self.vert_layout.addWidget(self.asset_split)
		self.vert_layout.setStretch(2,1)

		self.main_layout = QVBoxLayout()
		self.main_layout.addLayout(self.vert_layout)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.main_layout)

		# Connections -------------------------------------
		# Update library
		self.folders_view.folderSelectionChanged.connect(self.library_view.folder_selection_changed)

		# Update breadcrumbs
		self.folders_view.folderSelectionChanged.connect(self.breadcrumb_bar_widget.tabbar_crumbs.folder_selection_changed)

		# Update folders view
		self.breadcrumb_bar_widget.tabbar_crumbs.breadcrumbSelectionChanged.connect(self.folders_view.breadcrumb_changed)
		self.library_view.drillDown.connect(self.folders_view.lib_drilled_down)

		# Update model
		self.folders_view.expanded.connect(self.tree_model.lazy_load_update_model)
		self.folders_view.folderSelectionChanged.connect(self.tree_model.lazy_load_update_model)

		# On rename from delegate (use this if i ever make it so you can rename by double clicking an item)
		# self.library_delegate.delegateItemRenamed.connect(self.library_view._selection_changed)
		# self.folders_delegate.delegateItemRenamed.connect(self.folders_view._selection_changed)

		# Update details and minors
		self.folders_view.folderSelectionChanged.connect(self.selected_widget.details_widget.update_widget)
		self.folders_view.folderSelectionChanged.connect(self.selected_widget.lv_minors.update_widget)
		self.library_view.librarySelectionChanged.connect(self.selected_widget.details_widget.update_widget)
		self.library_view.librarySelectionChanged.connect(self.selected_widget.lv_minors.update_widget)

		# Right click menu
		self.library_view.customContextMenuRequested.connect(self._library_right_click_menu)
		self.folders_view.customContextMenuRequested.connect(self._folder_right_click_menu)

		# Watcher updates
		self.file_system_watcher.event_handler.sender.fileCreated.connect(self.tree_model.create_row)
		self.file_system_watcher.event_handler.sender.fileModified.connect(self.tree_model.modify_row)
		self.file_system_watcher.event_handler.sender.fileDeleted.connect(self.tree_model.delete_row)
		self.file_system_watcher.event_handler.sender.fileMoved.connect(self.tree_model.move_row)

	def _library_right_click_menu(self, position):
		"""Show right click menu for library view

		:param position:
		:return:
		"""
		# View selection
		click_position = position
		index_proxy_sel = self.library_view.indexAt(position)

		# Folder selection
		index_proxy_folders = self.folders_view.currentIndex()

		self.rc_menu = launcher.right_click_menu.RightClickMenu(self, index_proxy_sel, index_proxy_folders, self.folders_view.model())

		self.rc_menu.exec_(self.library_view.viewport().mapToGlobal(click_position))

	def _folder_right_click_menu(self, position):
		"""Right click menu for folders view

		:param position:
		:return:
		"""

		# View selection
		click_position = position
		index_proxy_sel = self.folders_view.indexAt(position)

		# Folder selection
		index_proxy_folders = self.folders_view.currentIndex()

		self.rc_menu = launcher.right_click_menu.RightClickMenu(self, index_proxy_sel, index_proxy_folders, self.folders_view.model())

		self.rc_menu.exec_(self.folders_view.viewport().mapToGlobal(click_position))


		# self.folders_widget.tv_folders.selectionModel().selectionChanged.connect(self.expand_file_components())

		# self.le_search_bar.textChanged.connect(self.library_widget.lv_library.search_text_changed)

		# self.library_options_widget.sort_state.connect(self.library_widget.lv_library.toggle_sorting)
		# self.library_options_widget.order_state.connect(self.library_widget.lv_library.set_order)
		# self.library_options_widget.role_state.connect(self.library_widget.lv_library.set_role)


	# def update_model(self, index):
	#
	# 	parent = self.tree_model.itemFromIndex(index)
	# 	for item in index.children:




