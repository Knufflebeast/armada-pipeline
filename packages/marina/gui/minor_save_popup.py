"""
Module for minor save popup.

A minor save is the .xxxx part of the _vxxx.xxxx version template
"""

import os
import uuid

from Qt import QtCore
from Qt import QtWidgets
from Qt.QtGui import QStandardItem, QIcon
from Qt.QtCore import Qt

from core import armada
from packages import marina

import utilsa

logging = utilsa.Logger('armada')


#######################################################
class MinorSavePopup(QtWidgets.QDialog):
	"""Create the major save popup window"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self, parent=None, index_source=None, tree_model=None):
		"""

		Args:
			parent: parent widget
			index_source:
			tree_model:
		"""
		super(MinorSavePopup, self).__init__()

		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.info('Minor save window open...')

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(armada.resource.style_sheet('main_window'))

		# Variables
		self.parent = parent
		self.index_source_folders = index_source
		self.index_source_folders_type = self.index_source_folders.data(QtCore.Qt.UserRole + 1)
		self._tree_model = tree_model
		self.version_current = self.get_current_version()
		self.version_increment = self.get_increment_version()

		self.resize(230, 100)

		self.software = os.getenv('_SOFTWARE')
		self.working_dir = os.getenv('WORKING_DIR')

		# Commands
		# self.move_ui()

		# GUI------------------------------------
		self.lbl_title = QtWidgets.QLabel("Version Increment")

		self.lbl_version_name = QtWidgets.QPushButton(
			armada.resource.icon(self.software, 'png'),
			"{0} -> {1}".format(self.version_current, self.version_increment)
		)
		self.lbl_version_name.setStyleSheet(armada.resource.style_sheet('icon_label'))

		self.lbl_comment_name = QtWidgets.QLabel("Comments:")
		self.lbl_comment_name.setStyleSheet(armada.resource.style_sheet('icon_label'))
		self.le_comments = QtWidgets.QLineEdit()

		# self.le_comments = QtWidgets.QLineEdit()
		self.btn_save = QtWidgets.QPushButton("Save")
		self.btn_cancel = QtWidgets.QPushButton("Cancel")

		# Layout ---------------------------
		self.name_layout = QtWidgets.QVBoxLayout()
		# self.name_layout.addWidget(self.icon_asset_name)
		self.name_layout.addWidget(self.lbl_title, 0, QtCore.Qt.AlignLeft)
		self.name_layout.addWidget(self.lbl_version_name, 0, QtCore.Qt.AlignLeft)
		self.name_layout.addWidget(self.lbl_comment_name, 0, QtCore.Qt.AlignLeft)
		self.name_layout.addWidget(self.le_comments)

		# self.label = QtWidgets.QLabel("Major comments?")

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_save)
		self.button_layout.addWidget(self.btn_cancel)

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_layout.addLayout(self.name_layout)
		# self.main_layout.addWidget(self.label)
		# self.main_layout.addWidget(self.le_comments)
		self.main_layout.addLayout(self.button_layout)

		self.setLayout(self.main_layout)

		# --------- Connections -----------
		self.le_comments.textChanged.connect(self.on_text_changed)

		self.btn_cancel.clicked.connect(self.on_cancel_pressed)
		self.btn_save.clicked.connect(self.on_save_pressed)

		self.esc_pressed.connect(self.on_cancel_pressed)

		self.le_comments.setFocus()

	def get_current_version(self):
		"""
		Gets current version number

		Returns:

		"""
		# Get last list view minor_ver
		proxy_major = self.parent.lv_minors.model().mapFromSource(self.index_source_folders)
		minor_index = self.parent.lv_minors.model().index(0, 0, proxy_major)
		minor_ver = minor_index.data(Qt.UserRole + 10)
		return minor_ver

	def get_increment_version(self):
		"""
		Gets new version number by incrementing number of last version

		Returns:

		"""
		# Get last list view minor_ver
		minor_ver = self.get_current_version()
		# Increment version number
		increment_ver = str(int(minor_ver) + 1).zfill(len(minor_ver))

		return increment_ver

	def on_save_pressed(self):
		"""Make a minor save

		todo:
			In future app file will be made at this point (instead of during launch event)
			and require a different setup for the launcher hooks. Will have to remove teh file creation from
			those hooks and make it just open the file

		:param name: str, User input name of new folder. It's validity is checked in the popup before it's sent
		:return:
		"""
		self.logger.info('Minor saving...')

		# Add item to model
		item_parent = self.parent.tree_model.itemFromIndex(self.index_source_folders)

		major_child_type = armada.structure.get_type_data(self.index_source_folders_type, type_data=armada.structure.CHILDREN)
		template_id = armada.structure.get_type_data(major_child_type[0], type_data=armada.structure.TEMPLATE_ID)

		# Structure
		child_data = armada.structure.get_type_data(major_child_type[0], type_data=armada.structure.DATA)

		# Data
		if 'meta_data' in child_data:
			child_data['meta_data']['item_name'] = self.version_increment
			child_data['meta_data']['item_type'] = major_child_type[0]
			child_data['meta_data']['uuid'] = str(uuid.uuid4())
			child_data['meta_data']['hidden'] = 'False'
			child_data['meta_data']['locked'] = 'True'
			child_data['meta_data']['template_id'] = template_id
		if 'type_data' in child_data:
			child_data['type_data']['software'] = self.software
			child_data['type_data']['minor_ver'] = self.version_increment
			child_data['type_data']['comment'] = self.le_comments.text()
			child_data['type_data']['user'] = "mike.bourbeau"
			child_data['type_data']['time'] = armada.file_data.get_date_time()

		# Create and add tree item to minor list view
		item_child = armada.tree_item.TreeItem(data=child_data, item_parent=item_parent)
		item_parent.appendRow([item_child, QStandardItem()])

		# Get index
		new_minor_index = self.parent.tree_model.indexFromItem(item_child)

		# Make data path
		data_path_abs = armada.resolver.generate_path(new_minor_index, 'data')

		# Save data to json
		armada.resource.json_save(data_path_abs, data=child_data)

		# Take screenshot and save it to data dir
		screenshot_image = armada.file_data.take_screenshot(data_path_abs)
		# Assign screenshot to new item
		item_child.setData(QIcon(screenshot_image), Qt.UserRole + 2)

		# Make app file
		new_minor_path = armada.resolver.generate_path(new_minor_index, 'user')

		"""
		.. todo::
			Make software path stuff on major creation
		"""

		# Rename current file to new file path
		manip = marina.file_manip.FileManip(software=self.software, save_type=marina.file_manip.FileManip.EXISTING)
		manip.save_file(new_minor_path)
		# Make major uuid file
		armada.path_maker.make_uuid_file(data_path_abs, uuid=item_child.data(QtCore.Qt.UserRole))
		self.close()

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

	def on_text_changed(self, text):
		"""
		Remove banned characters from name string
		"""
		# # Set the text in label
		typed_name = self.le_comments.text()
		typed_name_ = typed_name.capitalize()
		self.le_comments.setText(typed_name_)

		# Determine new width of popup
		init_width = self.frameGeometry().width()
		font_metrics = self.le_comments.fontMetrics()
		text_width = font_metrics.boundingRect(text).width()
		new_width = max(text_width + 50, init_width)

		if new_width > init_width:
			self.setFixedWidth(new_width)
			diff = int((new_width-init_width)/2)
			self.move(QtCore.QPoint(self.pos().x()-diff, self.pos().y()))

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""

		self.close()

	# def keyPressEvent(self, event):
	# 	if event.key() == QtCore.Qt.Key_Return:
	# 		self.enter_pressed.emit(self.enter_signal_str)
	# 		return True
	# 	if event.key() == QtCore.Qt.Key_Escape:
	# 		self.esc_pressed.emit(self.esc_signal_str)
	# 		return True
	# 	else:
	# 		super(MinorSavePopup, self).keyPressEvent(event)

	# def eventFilter(self, source, event):
	# 	"""
	# 	Close window on focus exit of popup
	# 	"""
	# 	if event.type() == QtCore.QEvent.WindowDeactivate:
	# 		self.close()
	# 	# elif event.type() == QtCore.QEvent.Close:
	# 	# 	self.parent.repaint()
	# 	# return true here to bypass default behaviour
	# 	return super(MinorSavePopup, self).eventFilter(source, event)


