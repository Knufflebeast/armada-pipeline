# """
# Module for major save popup.
#
# A major save is the _vxxx part of the _vxxx.xxxx version template
# """
#
# import os
# import uuid
#
# from Qt import QtCore
# from Qt import QtWidgets
# from Qt.QtGui import QStandardItem
#
# from mb_armada.gui.projects_context.tree_item import TreeItem
#
# from utilsa import resource
# from utilsa import renaming_convention
# from utilsa.path_resolver.index_path_resolver import generate_path
# from utilsa.path_resolver.multi_path_resolver import generate_multi_paths
# from path_maker import make_dirs
# from utilsa.logger import Logger
#
# logging = Logger('marina')
# logger = logging.getLogger(__name__)
#
#
# class MajorSavePopup(QtWidgets.QDialog):
# 	"""Create the major save popup window"""
#
# 	# Signal vars
# 	enter_pressed = QtCore.Signal(str)
# 	enter_signal_str = "returnPressed"
# 	esc_pressed = QtCore.Signal(str)
# 	esc_signal_str = "escPressed"
#
# 	def __init__(self, parent=None, index_source=None, tree_model=None):
# 		"""
#
# 		Args:
# 			parent: parent widget
# 			index_source:
# 			tree_model:
# 		"""
# 		super(MajorSavePopup, self).__init__()
#
# 		logger.warning('Major saving...')
#
# 		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
# 		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
# 		self.installEventFilter(self)
# 		self.setStyleSheet(resource.style_sheet('main_window'))
#
# 		# Variables
# 		self.parent = parent
# 		self.index_source_folders = index_source
# 		self.index_source_folders_type = self.index_source_folders.data(QtCore.Qt.UserRole + 1)
# 		self._tree_model = tree_model
#
# 		self.resize(230, 100)
#
# 		self.software = os.getenv('_SOFTWARE')
# 		self.working_dir = os.getenv('WORKING_DIR')
#
# 		# Commands
# 		# self.move_ui()
#
# 		# GUI------------------------------------
# 		self.new_type = self._map_type(self.index_source_folders_type)
#
# 		self.lbl_asset_name = QtWidgets.QPushButton(
# 			resource.color_svg(
# 				'folder_{}'.format(self.new_type),
# 				1024,
# 				'#FFFFFF'
# 			),
# 			"{0} Name:".format(self.new_type)
# 		)
# 		self.lbl_asset_name.setStyleSheet(resource.style_sheet('icon_label'))
# 		self.le_asset_name = QtWidgets.QLineEdit()
#
# 		# self.le_comments = QtWidgets.QLineEdit()
# 		self.btn_create = QtWidgets.QPushButton("Create")
# 		self.btn_cancel = QtWidgets.QPushButton("Cancel")
#
# 		# Layout ---------------------------
# 		self.name_layout = QtWidgets.QVBoxLayout()
# 		# self.name_layout.addWidget(self.icon_asset_name)
# 		self.name_layout.addWidget(self.lbl_asset_name, 0, QtCore.Qt.AlignLeft)
# 		self.name_layout.addWidget(self.le_asset_name)
#
# 		# self.label = QtWidgets.QLabel("Major comments?")
#
# 		self.button_layout = QtWidgets.QHBoxLayout()
# 		self.button_layout.addWidget(self.btn_create)
# 		self.button_layout.addWidget(self.btn_cancel)
#
# 		self.main_layout = QtWidgets.QVBoxLayout(self)
# 		self.main_layout.addLayout(self.name_layout)
# 		# self.main_layout.addWidget(self.label)
# 		# self.main_layout.addWidget(self.le_comments)
# 		self.main_layout.addLayout(self.button_layout)
#
# 		self.setLayout(self.main_layout)
#
# 		# --------- Connections -----------
# 		self.le_asset_name.textChanged.connect(self.on_text_changed)
#
# 		self.btn_cancel.clicked.connect(self.on_cancel_pressed)
# 		self.btn_create.clicked.connect(self.on_accept_pressed)
#
# 		self.esc_pressed.connect(self.on_cancel_pressed)
#
# 		self.le_asset_name.setFocus()
#
# 	def on_accept_pressed(self):
# 		"""
# 				Called when the user selects *Accept* from the New Folder popup.
#
# 				new_popup emits the data_accepted signal to call this function.
#
# 				.. note::
# 					Minors are always created along with majors at this point in the pipeline.
#
# 				.. note::
# 					Major dirs only have a data dir, but they're in charge of creating software dirs for now.
# 					Minor dirs only have a data dir.
#
# 				.. note::
# 					In future app file will be made at this point (instead of during launch event)
# 					and require a different setup for the launcher hooks. Will have to remove teh file creation from
# 					those hooks and make it just open the file
#
#
# 				:param name: str, User input name of new folder. It's validity is checked in the popup before it's sent
# 				:return:
# 				"""
# 		name = self.le_asset_name.text()
# 		new_type = self.new_type.lower().replace(" ", "_")
#
# 		# Check if name exists in dir already
# 		existing_names = []
# 		for row in range(self._tree_model.rowCount(self.index_source_folders)):
# 			existing_names.append(self._tree_model.index(row, 0, self.index_source_folders).data(QtCore.Qt.DisplayRole))
#
# 		# Emit signal to library tree view
# 		if name in existing_names:
# 			raise ValueError('Name already exists! Choose a different folder name.')
# 		if name is '':
# 			raise ValueError('No name entered! Enter a name for the folder')
# 		else:
#
# 			# Check if software selected when creating major
# 			if self.index_source_folders_type == 'asset_component':
# 				try:
# 					software = os.getenv('_SOFTWARE') # In the future I can put back the software list (once lib view groups by software
# 				except AttributeError:
# 					raise AttributeError('No software selected, please select one')
#
# 			# Send data with no software
# 			else:
# 				software = None
#
# 			folder_item = self._tree_model.itemFromIndex(self.index_source_folders)
#
# 			# Get item data
# 			data = self._item_data(new_type, name, software)
# 			# Create model items
# 			child_1 = TreeItem(self._tree_model, data=data, item_parent=folder_item)
# 			# Append child item under parent
# 			folder_item.appendRow([child_1, QStandardItem()])
#
# 			# If new item is a major_component, create it then create and append minor items as child
# 			if new_type == 'major_component':
# 				# Minor data
# 				child_data = self._item_data('minor_component', name, software)  # Minor data
# 				child_child_1 = TreeItem(self._tree_model, data=child_data, item_parent=child_1)
# 				# Append minor under the major component
# 				child_1.appendRow([child_child_1, QStandardItem()])
#
# 			# Update views
# 			self._tree_model.dataChanged.emit(self.index_source_folders, self.index_source_folders)
#
# 			new_index = self._tree_model.indexFromItem(child_1)
# 			self.parent.details_widget.update_widget(new_index)
# 			self.parent.lv_minors.update_widget(new_index)
#
# 			# Make dirs
# 			dir_maker = MakeDirs()
# 			new_item_index = self._tree_model.indexFromItem(child_1)
#
# 			# Make all dir types except major and minor
# 			if new_type != 'major_component':
#
# 				# Make user path
# 				user_path_abs = generate_path(new_item_index, resolver.USER)
# 				dir_maker.make_dirs(user_path_abs)
#
# 				# Make data path
# 				data_path_abs = generate_path(new_item_index, resolver.DATA)
# 				dir_maker.make_dirs(data_path_abs)
#
# 				# Make data file (data path much exist first)
# 				dir_maker.make_data_file(new_item_index, data, data_path_abs)
#
# 			# Make major and minor folder dirs
# 			else:
#
# 				# Make data path
# 				data_path_abs = generate_path(new_item_index, resolver.DATA)
# 				dir_maker.make_dirs(data_path_abs)
#
# 				# Make data file (data path much exist first)
# 				data_parent_path_abs = generate_path(new_item_index.parent(), resolver.DATA)
# 				dir_maker.make_data_file(new_item_index, data, data_path_abs, data_parent_path_abs)
#
# 				# Make software paths
# 				app_path_list = generate_multi_paths(new_item_index, software)
# 				for app_path in app_path_list:
# 					dir_maker.make_dirs(app_path)
#
# 				# Minor
# 				new_minor_index = self._tree_model.indexFromItem(child_child_1)
# 				# Make data path
# 				data_path_abs = generate_path(new_minor_index, resolver.DATA)
# 				dir_maker.make_dirs(data_path_abs)
#
# 				# Make data file (data path much exist first)
# 				dir_maker.make_data_file(new_minor_index, child_data, data_path_abs)
#
# 				# Make app file
# 				"""
# 				.. todo::
# 					Make software path stuff on major creation
# 				"""
#
# 		self.close()
#
# 	def _map_type(self, index_source_folders_type):
# 		"""
# 		Returns child type of selected folder. It maps
#
# 		If project type is selected this function will return "Asset Type"
#
# 		:param folder_index_source:
# 		:return:
# 		"""
# 		types = {
# 			'pipeline_root': 'client',
# 			'client': 'project',
# 			'project': 'asset_type',
# 			'asset_type': 'asset',
# 			'asset': 'asset_task',
# 			'asset_task': 'asset_component',
# 			'asset_component': 'major_component',
# 			'major_component': 'minor_component'
# 		}
#
# 		return ' '.join(x.capitalize() or '_' for x in types[index_source_folders_type].split('_'))
#
# 	def on_text_changed(self, text):
# 		"""
# 		Remove banned characters from name string
# 		"""
# 		# # Set the text in label
# 		typed_name = self.le_asset_name.text()
# 		conventions = renaming_convention.Convention(typed_name)
# 		formatted_text = conventions.set_convention(case=conventions.CAPITAL_SNAKE)
# 		self.le_asset_name.setText(formatted_text)
#
# 		# Determine new width of popup
# 		init_width = self.frameGeometry().width()
# 		font_metrics = self.le_asset_name.fontMetrics()
# 		text_width = font_metrics.boundingRect(text).width()
# 		new_width = max(text_width + 50, init_width)
#
# 		if new_width > init_width:
# 			self.setFixedWidth(new_width)
# 			diff = int((new_width-init_width)/2)
# 			self.move(QtCore.QPoint(self.pos().x()-diff, self.pos().y()))
#
#
# 	def _item_data(self, folder_type, name, software=None):
# 		"""Item data used to create new folders based on context of current folder selection.
#
# 		todo:
# 			Set up a single dictionary data structure using lucidity or something so this isn't so hard coded
#
# 		:param folder_type: str, What type of folder is selected in the folder view
# 		:param name: str, Folder name
# 		:param software: str, Any software to add
# 		:return:
# 		"""
#
# 		# Get data structure dict
# 		data_structure = resource.data_structure('data_structure')
#
# 		item_uuid = str(uuid.uuid4())
#
# 		if folder_type == 'client' or folder_type == 'project' or folder_type == 'asset_type' or \
# 				folder_type == 'asset' or folder_type == 'asset_task' or folder_type == 'client':
#
# 			data = data_structure['basic']
#
# 			data['meta_data']['item_name'] = name
# 			data['meta_data']['item_type'] = folder_type
# 			data['meta_data']['uuid'] = item_uuid
#
# 			return data
#
# 		# Asset Component
# 		elif folder_type == 'asset_component':
#
# 			data = data_structure['asset_component']
#
# 			data['meta_data']['item_name'] = name
# 			data['meta_data']['item_type'] = folder_type
# 			data['meta_data']['uuid'] = item_uuid
#
# 			data['type_data']['softwares'] = []
#
# 			return data
#
# 		# File component
# 		elif folder_type == 'major_component':
#
# 			data = data_structure['major_component']
#
# 			data['meta_data']['item_name'] = name
# 			data['meta_data']['item_type'] = folder_type
# 			data['meta_data']['uuid'] = item_uuid
#
# 			data['type_data']['software'] = software
# 			data['type_data']['major_ver'] = "001"
#
# 			data['ext_data']['assignee'] = "mike"
# 			data['ext_data']['due_date'] = "Apr 20, 2020"
# 			data['ext_data']['priority'] = "Low"
# 			data['ext_data']['tags'] = ["Dev"]
# 			data['ext_data']['progress'] = "Complete"
#
# 			return data
#
# 		elif folder_type == 'minor_component':
#
# 			data = data_structure['minor_component']
#
# 			data['meta_data']['item_name'] = "0001"
# 			data['meta_data']['item_type'] = folder_type
# 			data['meta_data']['uuid'] = item_uuid
#
# 			data['type_data']['software'] = software
# 			data['type_data']['minor_ver'] = "0001"
# 			data['type_data']['comment'] = "Started"
# 			data['type_data']['user'] = "mike.bourbeau"
# 			data['type_data']['time'] = "Jan 24, 2020 | 5:00pm"
#
# 			return data
#
# 	# # ------------------------------------------------------
# 	# def move_ui(self):
# 	# 	""" Moves the UI to window's edge """
# 	# 	self.setWindowFlags(QtCore.Qt.Popup)
# 	# 	# Get button position
# 	# 	btn_global_point = self.button_pos.mapToGlobal(self.button_pos.rect().topLeft())
# 	# 	# Get window position
# 	# 	win_global_point = self.parent.mapToGlobal(self.rect().topLeft())
# 	# 	# Get popup Size
# 	# 	popup_size = self.mapToGlobal(self.rect().topRight())
# 	# 	# Move the window
# 	# 	self.move(win_global_point.x() - popup_size.x() - 8, btn_global_point.y())
#
# 	def on_cancel_pressed(self):
# 		"""Cancel button pressed
# 		"""
#
# 		self.close()
#
# 	def keyPressEvent(self, event):
# 		if event.key() == QtCore.Qt.Key_Return:
# 			self.enter_pressed.emit(self.enter_signal_str)
# 			return True
# 		if event.key() == QtCore.Qt.Key_Escape:
# 			self.esc_pressed.emit(self.esc_signal_str)
# 			return True
# 		else:
# 			super(MajorSavePopup, self).keyPressEvent(event)
#
# 	def eventFilter(self, armada, event):
# 		"""
# 		Close window on focus exit of popup
# 		"""
# 		if event.type() == QtCore.QEvent.WindowDeactivate:
# 			self.close()
# 		# elif event.type() == QtCore.QEvent.Close:
# 		# 	self.parent.repaint()
# 		# return true here to bypass default behaviour
# 		return super(MajorSavePopup, self).eventFilter(armada, event)
