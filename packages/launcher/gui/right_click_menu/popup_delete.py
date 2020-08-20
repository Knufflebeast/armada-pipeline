"""
Module for prep asset popup. 
"""
import os
import errno
# from pathlib import Path
import shutil

from Qt import QtCore
from Qt import QtWidgets

from core import armada

import utilsa
logging = utilsa.Logger('armada')


class DeletePopup(QtWidgets.QDialog):
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

	def __init__(self, parent=None, index_proxy_sel=None, index_proxy_folders=None, tree_proxy=None):
		"""

		Args:
			parent: RightClickMenu widget
			index_source_sel: QModelIndex being deleted
			index_source_folders: QModelIndex selected in folder view
			tree_proxy: QSortFilterProxyModel
		"""

		super(DeletePopup, self).__init__()

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Delete popup open...')

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setStyleSheet(armada.resource.style_sheet('popup_window'))
		self.installEventFilter(self)

		self.parent = parent
		self.index_proxy_sel = index_proxy_sel
		self.index_source_sel = self.index_proxy_sel.model().mapToSource(self.index_proxy_sel)
		self.index_proxy_folders = index_proxy_folders
		self.index_source_folders = self.index_proxy_folders.model().mapToSource(self.index_proxy_sel)
		self.index_source_sel_type = self.index_source_sel.data(QtCore.Qt.UserRole + 1)
		self.index_source_sel_name = self.index_source_sel.data(QtCore.Qt.DisplayRole)
		self.tree_proxy = tree_proxy
		self.tree_model = self.tree_proxy.sourceModel()
		self.sel_type = self.index_source_sel_type

		# GUI ------------------------------
		self.lbl_title = QtWidgets.QLabel('Delete Folder')
		self.lbl_verify = QtWidgets.QLabel('Really delete:')
		self.new_icon = armada.structure.get_type_data(self.sel_type, armada.structure.ICON)

		self.lbl_asset_name = QtWidgets.QPushButton(
			armada.resource.color_svg(
				self.new_icon,
				1024,
				'#FFFFFF'
			), ''
		)
		self.lbl_asset_name.setText("{0}".format(self.index_source_sel_name))
		self.lbl_asset_name.setStyleSheet(armada.resource.style_sheet('icon_label'))
		self.lbl_question_mark = QtWidgets.QLabel("?")

		self.btn_accept = QtWidgets.QPushButton("Accept")
		self.btn_cancel = QtWidgets.QPushButton("Cancel")

		# Layout ---------------------------
		self.title_layout = QtWidgets.QVBoxLayout()
		self.title_layout.addWidget(self.lbl_title)

		self.name_layout = QtWidgets.QHBoxLayout()
		self.name_layout.addWidget(self.lbl_verify)
		self.name_layout.addWidget(self.lbl_asset_name)
		self.name_layout.addWidget(self.lbl_question_mark)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_accept)
		self.button_layout.addWidget(self.btn_cancel)
		self.button_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addLayout(self.name_layout)
		self.main_layout.addLayout(self.button_layout)
		self.main_layout.addStretch()

		self.setLayout(self.main_layout)

		# Connections
		self.btn_accept.clicked.connect(self.on_accept_pressed)
		self.btn_cancel.clicked.connect(self.on_cancel_pressed)

		self.enter_pressed.connect(self.on_accept_pressed)
		self.esc_pressed.connect(self.on_cancel_pressed)

	def eventFilter(self, source, event):
		"""
		Close window on focus exit of popup
		"""
		if event.type() == QtCore.QEvent.WindowDeactivate:
			self.close()
		return super(DeletePopup, self).eventFilter(source, event)

	def on_accept_pressed(self):
		"""Removes a file completely

		:param proxy_index: QSortFilterProxy Item from the library view
		:return:
		"""

		index_uuid = self.index_source_sel.data(QtCore.Qt.UserRole)
		if index_uuid == os.getenv('_MAJOR_UUID'):
			print("You're in that file! Enter into a different file before deleting")
		else:

			folder_type = self.index_source_sel.data(QtCore.Qt.UserRole + 1)
			template_id = self.index_source_sel.data(QtCore.Qt.UserRole + 19)
			self.logger.debug('current sel = {}'.format(self.index_source_sel.data(QtCore.Qt.DisplayRole)))
			self.logger.debug('parent = {}'.format(self.index_source_sel.parent().data(QtCore.Qt.DisplayRole)))

			# Data path abs
			data_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.DATA)

			# Delete data dir
			if os.path.exists(data_path_abs):
				shutil.rmtree(data_path_abs)

			# User path abs
			user_path_abs = armada.resolver.generate_path(self.index_source_sel, armada.resolver.USER)

			# Delete user dir
			if template_id != 'major_component':  # Prevent software dir from being deleted
				if os.path.exists(user_path_abs):
					shutil.rmtree(user_path_abs)
			# Remove files
			else:
				pass

			# Remove index from model
			self.tree_model.removeRows(self.index_source_sel.row(), 1, self.index_source_sel.parent())
			self.tree_model.dataChanged.emit(self.index_source_sel, self.index_source_sel)

			self.close()

			print("POOF! It's gone!")

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		self.deleteLater()
		self.close()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(DeletePopup, self).keyPressEvent(event)


