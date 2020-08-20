"""
Module for prep asset popup. 
"""

import errno
import shutil

from Qt import QtCore, QtWidgets

from core import armada

import utilsa

logging = utilsa.Logger('armada')


class RenamePopup(QtWidgets.QDialog):
	"""Builds the New Popup when the new button is pressed
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self, parent=None, index_proxy_sel=None, index_proxy_folders=None, tree_proxy=None):
		"""
		Args:
			parent: RightClickMenu widget
			index_proxy_sel: QModelIndex being renamed
			index_proxy_folders: QModelIndex selected in folder view
			tree_proxy: QSortFilterProxyModel
		"""
		super(RenamePopup, self).__init__()

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Building folders tree view...')

		self.parent = parent
		self.index_proxy_sel = index_proxy_sel
		self.index_proxy_folders = index_proxy_folders
		self.index_source_sel = self.index_proxy_sel.model().mapToSource(self.index_proxy_sel)
		self.index_source_sel_type = self.index_source_sel.data(QtCore.Qt.UserRole + 1)
		self.index_source_sel_name = self.index_source_sel.data(QtCore.Qt.DisplayRole)
		self.tree_proxy = tree_proxy
		self.tree_model = self.tree_proxy.sourceModel()

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.installEventFilter(self)

		self.setStyleSheet(armada.resource.style_sheet('popup_window'))

		# GUI ------------------------------
		self.sel_type = self.index_source_sel_type
		self.new_icon = armada.structure.get_type_data(self.sel_type, armada.structure.ICON)
		self.lbl_title = QtWidgets.QLabel('Rename Folder')

		self.lbl_asset_name = QtWidgets.QPushButton(
			armada.resource.color_svg(
				self.new_icon,
				1024,
				'#FFFFFF'
			), ''
		)
		self.lbl_asset_name.setText("{0} to:".format(self.index_source_sel_name))
		self.lbl_asset_name.setStyleSheet(armada.resource.style_sheet('icon_label'))

		self.le_asset_name = QtWidgets.QLineEdit()
		self.le_asset_name.setAlignment(QtCore.Qt.AlignLeft)
		self.le_asset_name.setText(self.index_source_sel_name)

		self.btn_accept = QtWidgets.QPushButton("Accept")
		self.btn_cancel = QtWidgets.QPushButton("Cancel")

		# Layout ---------------------------
		self.title_layout = QtWidgets.QVBoxLayout()
		# self.name_layout.addWidget(self.icon_asset_name)
		self.title_layout.addWidget(self.lbl_title)

		self.rename_layout = QtWidgets.QHBoxLayout()
		self.rename_layout.addWidget(self.lbl_asset_name)
		self.rename_layout.addWidget(self.le_asset_name)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_accept)
		self.button_layout.addWidget(self.btn_cancel)
		self.button_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addLayout(self.rename_layout)
		self.main_layout.addLayout(self.button_layout)
		self.main_layout.addStretch()

		self.setLayout(self.main_layout)

		self.le_asset_name.setFocus()
		# Connections
		self.btn_accept.clicked.connect(self.on_accept_pressed)
		self.btn_cancel.clicked.connect(self.on_cancel_pressed)
		self.le_asset_name.textChanged.connect(self.on_text_changed)

		self.enter_pressed.connect(self.on_accept_pressed)
		self.esc_pressed.connect(self.on_cancel_pressed)

	def eventFilter(self, source, event):
		"""
		Close window on focus exit of popup
		"""
		if event.type() == QtCore.QEvent.WindowDeactivate:
			self.close()
		# elif event.type() == QtCore.QEvent.Close:
		# 	self.parent.repaint()
		# return true here to bypass default behaviour
		return super(RenamePopup, self).eventFilter(source, event)

	def on_accept_pressed(self):
		"""
		Accept button pressed.

		Emits the *data_accepted* signal to the library tree view.

		Signal contains new file name, cleaned up asset type, and software
		"""
		name = self.le_asset_name.text()

		# Check if name exists in dir already
		existing_names = []
		for row in range(self.tree_model.rowCount(self.index_proxy_folders)):
			existing_names.append(self.tree_model.index(row, 0, self.index_proxy_folders).data(QtCore.Qt.DisplayRole))

		# Emit signal to library tree view
		if name in existing_names:
			raise ValueError('Name already exists! Choose a different folder name.')
		if name is '':
			raise ValueError('No name entered! Enter a name for the folder')
		else:
			self.rename_directories()

			self.close()

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		self.deleteLater()
		self.close()

	def on_text_changed(self, text):
		"""
		Remove banned characters from name string
		"""
		# Format text with convention
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
			diff = int((new_width-init_width)/2)
			self.move(QtCore.QPoint(self.pos().x()-diff, self.pos().y()))

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(RenamePopup, self).keyPressEvent(event)

	def rename_directories(self):
		"""Renames directory based on index.

		Rnamed the data dir, updates the name in the data.json file, updates the folder name in the user dir.

		:param editor: QLineEdit
		:param index: Proxy index
		:return:
		"""

		# Setup names
		name_init = self.index_source_sel_name
		self.logger.debug('name_init = {}'.format(name_init))
		name_new = self.le_asset_name.text()
		self.logger.debug('name_new = {}'.format(name_new))

		# Data path abs
		data_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.DATA)

		# New data path
		new_data_path_abs_ = armada.resolver.generate_path(self.index_source_sel, armada.resolver.DATA).rpartition(name_init)[0]
		new_data_path_abs = armada.resolver.build_path(new_data_path_abs_, name_new, return_type='data')

		# Rename data path (works for all template_id's)
		try:

			# Update json data file
			json_data = armada.resource.json_read(data_path_abs)
			json_data['meta_data']['item_name'] = name_new

			# Save json data
			armada.resource.json_save(data_path_abs, data=json_data)

			# Rename data path
			shutil.move(data_path_abs, new_data_path_abs)

		# except FileNotFoundError:
		except OSError as e:  # Using this because of python 2.7 in maya
			if e.errno == errno.EEXIST:
				pass
			else:
				raise self.logger.exception("Can't find user path: {}".format(data_path_abs))

		template_id = armada.structure.get_type_data(self.index_source_sel_type, armada.structure.TEMPLATE_ID)

		# Rename user path for all template_id's other than major_components
		if template_id != 'major_component':

			user_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.USER)

			# Rename
			try:
				# New user path
				new_user_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.USER).rpartition(name_init)[0]
				new_user_path_abs = armada.resolver.build_path(new_user_path_abs, name_new, return_type='user')

				# Rename data path
				shutil.move(user_path_abs, new_user_path_abs)

			# except FileNotFoundError:
			except OSError as e:  # Using this because of python 2.7 in maya
				if e.errno == errno.EEXIST:
					pass
				else:
					raise self.logger.exception("Can't find user path: {}".format(user_path_abs))

		# Rename user path for minor_components (major_components are only represented to users in the file name)
		# todo:
		# 	might be best to not rename the files due to vendor in 3d programs (i forget what i mean by this now...)
		else:
			# Rename
			try:
				# Get
				for row in range(self.tree_model.rowCount(self.index_source_sel)):
					# Index to edit
					minor_index = self.tree_model.index(row, 0, self.index_source_sel)
					# Rel path to parse
					minor_user_path_rel = armada.resolver.generate_path(minor_index, armada.resolver.USER, return_abs=False)
					# Minor structure ID
					minor_structure_var = armada.structure.get_type_data(self.index_source_sel_type, armada.structure.CHILDREN)[0]

					# Parse path to get template data dict
					template_data = armada.resolver.parse_path(minor_user_path_rel, minor_structure_var)
					# Rename major_component's value in the dict
					template_data_new = template_data.copy()
					template_data_new.update({template_id: name_new})

					# Get abs user path
					minor_path_abs = armada.resolver.resolve_data(template_data, minor_structure_var, armada.resolver.USER)
					self.logger.debug("minor_path_abs: '{}'".format(minor_path_abs))
					# Get new abs user path
					minor_path_new_abs = armada.resolver.resolve_data(template_data_new, minor_structure_var, armada.resolver.USER)
					self.logger.debug("minor_path_new_abs: '{}'".format(minor_path_new_abs))

					# Rename user path minors
					shutil.move(minor_path_abs, minor_path_new_abs)

			# except FileNotFoundError:
			except OSError as e:  # Using this because of python 2.7 in maya
				if e.errno == errno.EEXIST:
					pass
				else:
					self.logger.exception("Can't find user path: {}".format(minor_path_abs))

		# Update model
		self.tree_model.setData(self.index_source_sel, self.le_asset_name.text(), QtCore.Qt.DisplayRole)

		# Update views
		self.tree_model.dataChanged.emit(self.index_source_sel.parent(), self.index_source_sel)

		# Select item in view
		self.parent.parent.folders_view._selection_changed()
		self.parent.parent.folders_view.setCurrentIndex(self.index_source_sel)
		self.parent.parent.library_view._selection_changed()

