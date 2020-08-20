"""
Module for prep asset popup. 
"""
import os
import uuid
# from pathlib import Path

from Qt import QtCore, QtWidgets
from Qt.QtGui import QStandardItem

from core import armada
from packages import marina

import utilsa

logging = utilsa.Logger('armada')


class NewPopup(QtWidgets.QDialog):
	"""Builds the New Popup when the new button is pressed

	Dialog presents user with options for creating a new folder or file

	Context sensitive item types to create:
		- Projects folder        > Client folders
		- Client folder          > Project folders
		- Project folder         > Asset type folders
		- Asset Type folder      > Asset folders
		- Asset folder           > Task folders
		- Task folder            > Asset component folders
		- Asset Component folder > File component groups with versions inside each group
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	newCreated = QtCore.Signal()

	def __init__(self, parent=None, index_proxy_folders=None, tree_proxy=None, new_type=None):
		"""

		Args:
			parent: RightClickMenu widget
			index_proxy_folders: ProxyItem selected in folder view
			tree_proxy: QSortFilterProxyModel from selected widget
			new_type: str, Data bound to selected menu action (name of the action)
		"""
		super(NewPopup, self).__init__()

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('New popup...')

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(armada.resource.style_sheet('popup_window'))

		# self.ext_data = self.parent.ext_data
		self.parent = parent
		self.index_proxy_folders = index_proxy_folders
		self.index_source_folders = self.index_proxy_folders.model().mapToSource(index_proxy_folders)

		new_type_data = new_type.data()
		self.new_type = new_type_data['type']
		self.new_template_id = new_type_data['template_id']

		self.index_source_folders_type = self.index_source_folders.data(QtCore.Qt.UserRole + 1)

		self.tree_proxy = tree_proxy
		self.tree_model = tree_proxy.sourceModel()

		# # Multi-threading
		# self.threadpool = QtCore.QThreadPool()
		# print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

		# GUI ------------------------------
		# Get structure

		# Get new type from potential children

		# Format
		self.formatted_new_type = self._format_type(self.new_template_id)

		self.new_category = armada.structure.get_type_data(self.new_type, armada.structure.CATEGORY)
		self.new_icon = armada.structure.get_type_data(self.new_type, armada.structure.ICON)
		self.lbl_title = QtWidgets.QLabel("New {0}".format(str(self.new_category).capitalize()))

		self.lbl_asset_name = QtWidgets.QPushButton(
			armada.resource.color_svg(
				self.new_icon,
				1024,
				'#FFFFFF'
			),
			"{0} Name:".format(self.formatted_new_type)
		)
		self.lbl_asset_name.setStyleSheet(armada.resource.style_sheet('icon_label'))
		self.le_asset_name = QtWidgets.QLineEdit()
		self.le_asset_name.setAlignment(QtCore.Qt.AlignLeft)

		# Get available software list for new major popup
		if self.new_template_id == 'major_component':
			self.lbl_items_title = QtWidgets.QLabel('Software:')
		else:
			self.lbl_items_title = QtWidgets.QLabel('Folder Type')
		self.lw_items = QtWidgets.QListWidget()
		self.lw_items.setViewMode(QtWidgets.QListView.IconMode)
		# self.lw_items.setMaximumHeight(50)
		# self.lw_items.setResizeMode(QtWidgets.QListView.Fixed)
		self.lw_items.setUniformItemSizes(True)
		self.lw_items.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustIgnored)
		self.lw_items.setMovement(self.lw_items.Static)
		self.lw_items.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents);
		self.lw_items.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum);
		self.lw_items.setFlow(QtWidgets.QListView.LeftToRight)
		# self.lw_items.setSpacing(5)
		self.lw_items.setMinimumSize(500, 300)
		self.lw_items.setStyleSheet("""
		QListView{
			show-decoration-selected: 0;
			background: #262626;
			color:rgb(218,218,218) ;
			font:12px "Roboto-Thin";
			border: none;
			height: 200px;
			outline: 0;
			padding-left: 10;
			padding-right: 10;
		}
					
		""")

		# Get app configs
		if self.new_template_id == 'major_component':
			app_config_path = armada.resource.get('armada', 'app')
			children = [dI for dI in os.listdir(app_config_path) if os.path.isdir(os.path.join(app_config_path, dI))]

			for item in children:
				# Ignore non app folders in aramda.app directory
				if item == '__pycache__':
					pass

				else:
					icon = armada.resource.icon(item.lower(), 'png')
					lw_item = QtWidgets.QListWidgetItem(icon, item.capitalize())
					lw_item.setSizeHint(self.lw_items.sizeHint())
					self.lw_items.addItem(lw_item)
		# else:
		# 	for item in self.new_type:
		# 		# Pass over sub_folder category (they should be auto created)
		# 		item_categroy = structure.get_type_data(item, structure.CATEGORY)
		# 		if item_categroy == 'sub_folder':
		# 			pass
		# 		else:
		# 			self.icon = structure.get_type_data(item, structure.ICON)
		# 			self.formatted_item = self._format_type(item)
		# 			self.icon = structure.get_type_data(item, structure.ICON)
		# 			icon = resource.color_svg(self.icon, 128, '#FFFFFF')
		# 			lw_item = QtWidgets.QListWidgetItem(icon, self.formatted_item)
		# 			lw_item.setSizeHint(self.lw_items.sizeHint())
		# 			self.lw_items.addItem(lw_item)
		# 	icon = resource.color_svg('folder', 128, '#FFFFFF')
		# 	lw_item = QtWidgets.QListWidgetItem(icon, "Folder")
		# 	lw_item.setSizeHint(self.lw_items.sizeHint())
		# 	self.lw_items.addItem(lw_item)

		# Python 3
		# Use with pathlib
		# pathin = Path(os.path.join(os.getenv('ARMADA_ROOT_PATH'), 'resources', 'apps'))
		# software_list = self.get_all_apps(pathin)
		#
		# for item in software_list:
		# 	icon = armada.resource.icon(item.lower(), 'png')
		# 	item = QtWidgets.QListWidgetItem(icon, item)
		# 	self.lw_items.addItem(item)

		self.btn_cancel = QtWidgets.QPushButton("Cancel")
		self.btn_accept = QtWidgets.QPushButton("Accept")

		# Layout ---------------------------
		self.title_layout = QtWidgets.QHBoxLayout()
		self.title_layout.addWidget(self.lbl_title, 0, QtCore.Qt.AlignLeft)

		self.name_layout = QtWidgets.QHBoxLayout()
		# self.name_layout.addWidget(self.icon_asset_name)
		self.name_layout.addWidget(self.lbl_asset_name)
		self.name_layout.addWidget(self.le_asset_name)

		if self.new_template_id == 'major_component':
			self.items_layout = QtWidgets.QVBoxLayout()
			self.items_layout.addWidget(self.lbl_items_title, 0, QtCore.Qt.AlignLeft)
			self.items_layout.addWidget(self.lw_items)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_accept)
		self.button_layout.addWidget(self.btn_cancel)
		self.button_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addLayout(self.name_layout)
		if self.new_template_id == 'major_component':
			self.main_layout.addLayout(self.items_layout)
		self.main_layout.addLayout(self.button_layout)
		self.main_layout.addStretch()

		self.setLayout(self.main_layout)

		# Connections
		self.btn_cancel.clicked.connect(self.on_cancel_pressed)
		self.btn_accept.clicked.connect(self.on_accept_pressed)
		self.le_asset_name.textChanged.connect(self.on_text_changed)

		self.enter_pressed.connect(self.on_accept_pressed)
		self.esc_pressed.connect(self.on_cancel_pressed)

		# self.move_ui()

		self.le_asset_name.setFocus()

	#
	# def move_ui(self):
	# 	"""Moves the UI to window's edge"""
	#
	# 	# Get button position, get window position, get popup size,
	# 	# move the window.
	# 	c = self.parent.rect().center()
	# 	print(c.x(), c.y())
	#
	# 	# btn_global_point = self.button_pos.mapToGlobal(self.button_pos.rect().topLeft())
	# 	# win_global_point = self.parent.mapToGlobal(self.rect().topLeft())
	# 	# popup_size = self.mapToGlobal(self.rect().topRight())
	# 	# self.move(win_global_point.x()-popup_size.x()-8,btn_global_point.y())
	# 	self.move(self.parent.viewport().mapToGlobal(c).x(), self.parent.viewport().mapToGlobal(c).y())

	# def get_all_apps(self, dir_to_search):
	# 	""" Returns a list of file names from a directory
	#
	# 	:param dir_to_search:
	# 	:return:
	# 	"""
	# 	filename_list = []
	#
	# 	file_iterator = dir_to_search.iterdir()
	#
	# 	for item in file_iterator:
	# 		if item.is_file():  # change to is dir
	# 			clean_item = item.with_suffix('')
	# 			clean_item = clean_item.name.capitalize()
	# 			filename_list.append(clean_item)
	#
	# 	return filename_list

	def eventFilter(self, source, event):
		"""
		Close window on focus exit of popup
		"""
		if event.type() == QtCore.QEvent.WindowDeactivate:
			self.close()
		# elif event.type() == QtCore.QEvent.Close:
		# 	self.parent.repaint()
		# return true here to bypass default behaviour
		return super(NewPopup, self).eventFilter(source, event)

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

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		self.deleteLater()
		self.close()

	def on_text_changed(self, text):
		"""Remove banned characters from name string
		"""
		# # Set the text in label
		typed_name = self.le_asset_name.text()
		conventions = armada.renaming_convention.Convention(typed_name)
		formatted_text = conventions.set_convention(case=conventions.CAPITAL_SNAKE)
		self.le_asset_name.setText(formatted_text)

		# Determine new width of popup
		init_width = self.frameGeometry().width()
		lbl_name_width = self.lbl_asset_name.frameGeometry().width()
		le_asset_name_width = self.le_asset_name.frameGeometry().width()
		font_metrics = self.le_asset_name.fontMetrics()
		text_width = font_metrics.boundingRect(text).width()
		new_width = max(lbl_name_width + text_width + 50, init_width)

		if new_width > init_width:
			self.setFixedWidth(new_width)
			diff = int((new_width - init_width) / 2)
			self.move(QtCore.QPoint(self.pos().x() - diff, self.pos().y()))

	def _item_data(self, folder_type, name, software=None, major_ver='001', minor_ver='0001'):
		"""Item data used to create new folders based on context of current folder selection.

		Stucture is determined by the structure file

		todo:
			Make it so these items are somehow autopopulated and I don't have to hard code what each value equals

		:param folder_type: str, What type of folder is selected in the folder view
		:param name: str, Folder name
		:param software: str, Any software to add
		:return:
		"""
		self.logger.info('Item data filling...')

		# Get data structure dict
		data = armada.structure.get_type_data(folder_type, type_data=armada.structure.DATA)

		template_id = armada.structure.get_type_data(folder_type, type_data=armada.structure.TEMPLATE_ID)

		item_uuid = str(uuid.uuid4())

		# For any folder
		if 'meta_data' in data:
			data['meta_data']['item_name'] = name
			data['meta_data']['item_type'] = folder_type
			data['meta_data']['uuid'] = item_uuid
			data['meta_data']['locked'] = "True"
			data['meta_data']['hidden'] = "False"
			data['meta_data']['template_id'] = template_id
		if 'ext_data' in data:
			data['ext_data']['assignee'] = "mike"
			data['ext_data']['due_date'] = "Apr 20, 2020"
			data['ext_data']['priority'] = "Low"
			data['ext_data']['tags'] = ["Dev"]
			data['ext_data']['progress'] = "Complete"

		# Add type data for major
		if template_id == 'major_component':
			if 'type_data' in data:
				data['type_data']['software'] = software
				data['type_data']['major_ver'] = major_ver

		# Add type data for minor
		if template_id == 'minor_component':
			if 'meta_data' in data:
				data['meta_data']['item_name'] = minor_ver
			if 'type_data' in data:
				data['type_data']['software'] = software
				data['type_data']['minor_ver'] = minor_ver
				data['type_data']['comment'] = "Started"
				data['type_data']['user'] = "mike.bourbeau"
				data['type_data']['time'] = armada.file_data.get_date_time()

		return data

	def on_accept_pressed(self):
		"""
		Called when the user selects *Accept* from the New Folder popup.

		new_popup emits the data_accepted signal to call this function.

		.. note::
			Minors are always created along with majors at this point in the pipeline.

		.. note::
			Major dirs only have a data dir, but they're in charge of creating software dirs for now.
			Minor dirs only have a data dir.

		.. note::
			In future app file will be made at this point (instead of during launch event)
			and require a different setup for the launcher hooks. Will have to remove teh file creation from
			those hooks and make it just open the file


		:param name: str, User input name of new folder. It's validity is checked in the popup before it's sent
		:return:
		"""
		self.logger.info('Saving file...')
		name = self.le_asset_name.text()
		software = None

		# Make sure there's a type selection
		if self.new_template_id == 'major_component':
			try:
				software = self.lw_items.currentIndex().data(QtCore.Qt.DisplayRole).lower()
				self.logger.info('Software = {}'.format(software))
			except AttributeError:
				raise AttributeError('No software selected, please select one')

			try:
				new_type = self.lw_items.currentIndex().data(QtCore.Qt.DisplayRole).lower()
				self.logger.info('new_type = {}'.format(new_type))
			except AttributeError:
				raise AttributeError('No type selected, please select one')

		# Check if name exists in dir already
		existing_names = []
		for row in range(self.tree_model.rowCount(self.index_source_folders)):
			existing_names.append(self.tree_model.index(row, 0, self.index_source_folders).data(QtCore.Qt.DisplayRole))

		# Emit signal to library tree view
		if name in existing_names:
			raise ValueError('Name already exists! Choose a different folder name.')
		if name is '':
			raise ValueError('No name entered! Enter a name for the folder')
		else:

			folder_item = self.tree_model.itemFromIndex(self.index_source_folders)

			# Get item data
			data = self._item_data(self.new_type, name, software)
			# Create model items
			child_1 = armada.tree_item.TreeItem(data=data, item_parent=folder_item)
			# Append child item under parent
			folder_item.appendRow([child_1, QStandardItem()])

			# If new item is a major_component, create it then create and append minor items as child
			if self.new_template_id == 'major_component':
				major_child = armada.structure.get_type_data(self.new_type, armada.structure.CHILDREN)
				# Minor data
				child_data = self._item_data(major_child[0], name, software)  # Minor data
				child_child_1 = armada.tree_item.TreeItem(data=child_data, item_parent=child_1)
				# Append minor under the major component
				child_1.appendRow([child_child_1, QStandardItem()])

			# Update views
			index_new = self.tree_model.indexFromItem(child_1)
			index_new_proxy = self.tree_proxy.mapFromSource(index_new)

			folder_index_source = self.index_proxy_folders.model().mapToSource(self.index_proxy_folders)

			# 	Set header settings (without this the first item in a view is screwed up)
			self.parent.parent.folders_view.header()

			self.tree_model.dataChanged.emit(folder_index_source, index_new) # Update view

			# Select folder item in view unless it's a major
			if self.new_template_id != 'major_component':
				self.parent.parent.folders_view.setCurrentIndex(index_new_proxy)
				# self.parent.parent.folders_view.setCurrentIndex(index_new_proxy)
			# Select major in library if making a major
			else:
				index_lib_proxy = self.parent.parent.library_view.model().mapFromSource(index_new)
				self.parent.parent.library_view.setCurrentIndex(index_lib_proxy)

			# Make dirs
			new_item_index = self.tree_model.indexFromItem(child_1)

			self.logger.info('Making directories...')
			# Make all dir types except major and minor
			if self.new_template_id != 'major_component':

				# Make user path
				user_path_abs = armada.resolver.generate_path(new_item_index, armada.resolver.USER)
				armada.path_maker.make_dirs(user_path_abs)

				# Make data path
				data_path_abs = armada.resolver.generate_path(new_item_index, armada.resolver.DATA)
				armada.path_maker.make_dirs(data_path_abs)

				# Make data file (data path much exist first)
				armada.path_maker.make_data_file(data_path_abs, json_data=data)
				armada.path_maker.make_uuid_file(data_path_abs, uuid=child_1.data(QtCore.Qt.UserRole))

			# Make major and minor folder dirs
			else:

				# Make major data path
				data_path_abs = armada.resolver.generate_path(new_item_index, armada.resolver.DATA)
				armada.path_maker.make_dirs(data_path_abs)

				# Make major data file (data path must exist first)
				armada.path_maker.make_data_file(data_path_abs, json_data=data)

				# Make major uuid file
				armada.path_maker.make_uuid_file(data_path_abs, uuid=child_1.data(QtCore.Qt.UserRole))

				# Make software paths
				app_path_list = armada.resolver.generate_multi_paths(new_item_index, software)
				for app_path in app_path_list:
					armada.path_maker.make_dirs(app_path)

				# Minor making
				new_minor_index = self.tree_model.indexFromItem(child_child_1)
				# Make data path
				data_path_abs = armada.resolver.generate_path(new_minor_index, armada.resolver.DATA)
				armada.path_maker.make_dirs(data_path_abs)

				# Make data file (data path must exist first)
				armada.path_maker.make_data_file(data_path_abs, json_data=child_data)

				# Make uuid file
				armada.path_maker.make_uuid_file(data_path_abs, uuid=child_child_1.data(QtCore.Qt.UserRole))

				# Make app file
				user_path_abs = armada.resolver.generate_path(new_minor_index, armada.resolver.USER)
				"""
				.. todo::
					Create software file on major creation from launcher (will require standalone per software prob)
				
				# if not os.path.exists(user_path_abs):
				#
				# 	# Make software file (maya is the first one to try it out)
				# 	app_path = os.getenv('MAYA_LOCATION')
				# 	import sys
				# 	if os.path.exists(app_path) and app_path not in sys.path:
				# 		sys.path.append(app_path)
				# 	import maya.standalone
				# 	maya.standalone.initialize(name='python')
				# 	import maya.cmds as mc
				# 	mc.file(force=True, new=True)
				# 	mc.file(force=True, save=True)
				"""

				# Make path when inside software
				try:

					from packages import marina
					manip = marina.file_manip.FileManip(software=software, save_type=marina.file_manip.FileManip.NEW)
					manip.save_file(user_path_abs)
					current_index = self.parent.parent.parent.major_index
					self.parent.parent.parent.major_index = index_new
					self.parent.parent.parent.save_button_toggle()
				except:
					pass

		self.close()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(NewPopup, self).keyPressEvent(event)

# class WorkerSignals(QtCore.QObject):
# 	"""
# 	Defines the signals available from a running worker thread.
#
# 	Supported signals are:
# 		finished | No data
# 		error | `tuple` (exctype, value, traceback.format_exc() )
# 		result | `object` data returned from processing, anything
# 		progress | `int` indicating % progress
# 	"""
# 	finished = QtCore.Signal()
# 	error = QtCore.Signal(tuple)
# 	result = QtCore.Signal(object)
# 	progress = QtCore.Signal(int)
#
#
# class Worker(QtCore.QRunnable):
# 	"""
# 	Worker thread
#
# 	Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
#
# 	:param callback: The function callback to run on this worker thread. Supplied args and
# 						kwargs will be passed through to the runner.
# 	:type callback: function
# 	:param args: Arguments to pass to the callback function
# 	:param kwargs: Keywords to pass to the callback function
# 	"""
#
# 	def __init__(self, function, *args, **kwargs):
# 		super(Worker, self).__init__()
#
# 		# Store constructor arguments (re-used for processing)
# 		self.function = function
# 		self.args = args
# 		self.kwargs = kwargs
# 		self.signals = WorkerSignals()
#
# 		# Add the callback to our kwargs
# 		self.kwargs['progress_callbacks'] = self.signals.progress
#
# 	@QtCore.Slot()
# 	def run(self):
# 		"""
# 		Initialise the runner function with passed args, kwargs.
# 		"""
#
# 		# Retrieve args/kwargs here; and fire processing using them
# 		try:
# 			result = self.function(*self.args, **self.kwargs)
# 		except:
# 			traceback.print_exc()
# 			exctype, value = sys.exc_info()[:2]
# 			self.signals.error.emit((exctype, value, traceback.format_exc()))
# 		else:
# 			self.signals.result.emit(result)  # Return the result of the processing
# 		finally:
# 			self.signals.finished.emit()  # Done
