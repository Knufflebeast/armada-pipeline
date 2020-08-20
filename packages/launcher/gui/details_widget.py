"""
Module for options tab within publish tab
"""

from Qt import QtWidgets, QtCore

from core import armada
from packages import launcher

import utilsa

logging = utilsa.Logger('armada')


class DetailsWidget(QtWidgets.QWidget):
	"""Fills selection info tab with an options tab widget
	"""

	def __init__(self, parent=None, index_source=None):
		super(DetailsWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

		self.index_source = index_source
		self.parent = parent

		self.setMinimumWidth(500)

		# Header
		self.header_frame = QtWidgets.QFrame()
		self.header_frame.setFixedHeight(55)
		self.header_frame.setStyleSheet("QFrame{background: #4b4b4b; border: 0px;}")

		self.selected_color_frame = QtWidgets.QFrame()
		self.selected_color_frame.setStyleSheet("QFrame{background: #2c998e; border: 0px;}")
		self.selected_color_frame.setFixedWidth(5)

		self.btn_icon_type = QtWidgets.QPushButton()
		self.btn_icon_type.setFixedSize(30, 30)
		self.icon_type = armada.resource.icon('default', 'png')
		self.btn_icon_type.setIcon(self.icon_type)
		self.btn_icon_type.setIconSize(QtCore.QSize(30, 30))
		self.btn_icon_type.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))

		self.name_frame = QtWidgets.QFrame()
		self.name_frame.setStyleSheet("QFrame{background: #111111; border: 0px;}")
		self.name_frame.setFixedHeight(35)
		self.lbl_name = QtWidgets.QLabel('No selection')
		self.lbl_name.setContentsMargins(5, 0, 0, 0)

		self.lbl_name.setStyleSheet("QLabel{font: 18px Roboto-Thin; height: 20px; font-weight:bold;}")

		self.type_frame = QtWidgets.QFrame()
		self.type_frame.setStyleSheet("QFrame{background: #222222; border: 0px;}")
		self.type_frame.setFixedHeight(25)
		self.lbl_type = QtWidgets.QLabel('No type')
		self.lbl_type.setContentsMargins(5, 0, 5, 0)

		self.lbl_type.setStyleSheet("QLabel{font: Roboto-Thin; height: 10px;}")

		self.btn_back = QtWidgets.QPushButton()
		self.btn_back.setFixedSize(30, 30)
		self.btn_back_icon = armada.resource.color_svg('arrow_right', 128, '#FFFFFF')
		self.btn_back.setIcon(self.btn_back_icon)
		self.btn_back.setIconSize(QtCore.QSize(30, 30))
		self.btn_back.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))

		# Image and labels frame
		self.data_frame = QtWidgets.QFrame()
		self.data_frame.setStyleSheet("QFrame{background: #262626; border: 0px;}")

		# Image
		self.asset_pixmap = armada.resource.pixmap('default_asset')
		# self.asset_pixmap = resource.color_svg('default_asset', 128, '#FFFFFF', 'pixmap')
		# self.lbl_preview_image = QtWidgets.QLabel()
		# self.lbl_preview_image.setPixmap(self.asset_pixmap)
		self.lbl_preview_image = launcher.label_preview.PreviewLabel(self.asset_pixmap)

		# Labels
		self.labels_frame = QtWidgets.QFrame()
		self.labels_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")

		# User
		self.assignee_frame = QtWidgets.QFrame()
		self.assignee_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")
		self.user_avatar = launcher.label_image.LabelImage('mike.bourbeau', size=22)
		self.lbl_assignee = QtWidgets.QLabel('Mike Bourbeau')

		# Due
		self.due_frame = QtWidgets.QFrame()
		self.due_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")

		self.due_icon = QtWidgets.QLabel()
		self.due_svg = armada.resource.color_svg('calendar', 128, '#FFFFFF')
		self.due_icon.setPixmap(self.due_svg.pixmap(22, 22))
		self.lbl_due = QtWidgets.QLabel('Jan 24, 2020')

		# Priority
		self.priority_frame = QtWidgets.QFrame()
		self.priority_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")

		self.priority_icon = QtWidgets.QLabel()
		self.priority_svg = armada.resource.color_svg('priority', 128, '#FFFFFF')
		self.priority_icon.setPixmap(self.priority_svg.pixmap(22, 22))
		self.lbl_priority = QtWidgets.QLabel('High')

		# Tags
		self.tags_frame = QtWidgets.QFrame()
		self.tags_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")

		self.tags_icon = QtWidgets.QLabel()
		self.tags_svg = armada.resource.color_svg('tags', 128, '#FFFFFF')
		self.tags_icon.setPixmap(self.tags_svg.pixmap(22, 22))
		self.lbl_tags = QtWidgets.QLabel('Art')

		# Progress
		self.progress_frame = QtWidgets.QFrame()
		self.progress_frame.setStyleSheet("QFrame{background: transparent; border: 0px;}")

		self.progress_icon = QtWidgets.QLabel()
		self.progress_svg = armada.resource.color_svg('progress', 128, '#FFFFFF')
		self.progress_icon.setPixmap(self.progress_svg.pixmap(22, 22))
		self.lbl_progress = QtWidgets.QLabel('In Progress')

		# Layout
		name_layout = QtWidgets.QHBoxLayout()
		name_layout.addWidget(self.lbl_name, 0, QtCore.Qt.AlignLeft)
		name_layout.setContentsMargins(0, 0, 0, 0)

		type_layout = QtWidgets.QHBoxLayout()
		type_layout.addWidget(self.lbl_type, 0, QtCore.Qt.AlignLeft)
		type_layout.setContentsMargins(0, 0, 0, 0)

		name_type_layout = QtWidgets.QVBoxLayout()
		name_type_layout.addLayout(name_layout)
		name_type_layout.addLayout(type_layout)
		name_type_layout.setContentsMargins(0, 0, 0, 0)

		header_layout = QtWidgets.QHBoxLayout(self.header_frame)
		header_layout.addWidget(self.selected_color_frame, 0, QtCore.Qt.AlignLeft)
		header_layout.addWidget(self.btn_icon_type, 0, QtCore.Qt.AlignLeft)
		header_layout.addLayout(name_type_layout, 1)
		header_layout.addWidget(self.btn_back)
		header_layout.setContentsMargins(0, 0, 0, 0)

		self.assignee_layout = QtWidgets.QHBoxLayout(self.assignee_frame)
		# self.assignee_layout.addWidget(self.user_avatar)
		self.assignee_layout.addWidget(self.lbl_assignee)
		self.assignee_layout.setContentsMargins(5, 0, 5, 0)
		self.assignee_layout.setSpacing(5)

		self.due_layout = QtWidgets.QHBoxLayout(self.due_frame)
		self.due_layout.addWidget(self.due_icon)
		self.due_layout.addWidget(self.lbl_due, 1, QtCore.Qt.AlignLeft)
		self.due_layout.setContentsMargins(5, 0, 5, 0)
		self.due_layout.setSpacing(5)

		self.priority_layout = QtWidgets.QHBoxLayout(self.priority_frame)
		self.priority_layout.addWidget(self.priority_icon)
		self.priority_layout.addWidget(self.lbl_priority, 1, QtCore.Qt.AlignLeft)
		self.priority_layout.setContentsMargins(5, 0, 5, 0)
		self.priority_layout.setSpacing(5)

		self.tags_layout = QtWidgets.QHBoxLayout(self.tags_frame)
		self.tags_layout.addWidget(self.tags_icon)
		self.tags_layout.addWidget(self.lbl_tags, 1, QtCore.Qt.AlignLeft)
		self.tags_layout.setContentsMargins(5, 0, 5, 0)
		self.tags_layout.setSpacing(5)

		self.progress_layout = QtWidgets.QHBoxLayout(self.progress_frame)
		self.progress_layout.addWidget(self.progress_icon)
		self.progress_layout.addWidget(self.lbl_progress, 1, QtCore.Qt.AlignLeft)
		self.progress_layout.setContentsMargins(5, 0, 5, 0)
		self.progress_layout.setSpacing(5)

		self.labels_layout = QtWidgets.QVBoxLayout(self.labels_frame)
		self.labels_layout.addWidget(self.assignee_frame)
		self.labels_layout.addWidget(self.due_frame)
		self.labels_layout.addWidget(self.priority_frame)
		self.labels_layout.addWidget(self.tags_frame)
		self.labels_layout.addWidget(self.progress_frame)
		self.labels_layout.setContentsMargins(0, 0, 0, 0)
		self.labels_layout.setSpacing(3)
		self.labels_layout.setAlignment(QtCore.Qt.AlignTop)

		# self.data_layout = QtWidgets.QBoxLayout(QtWidgets.QVBoxLayout.Down)
		# self.data_layout.addWidget(self.lbl_path)
		# self.data_layout.addWidget(self.lbl_version)
		# self.data_layout.addWidget(self.lbl_creator)
		# self.data_layout.addWidget(self.lbl_last_edit)
		# self.data_layout.addWidget(self.lbl_status)
		# self.data_layout.addWidget(self.lbl_comments)

		self.data_layout = QtWidgets.QHBoxLayout(self.data_frame)
		self.data_layout.addWidget(self.lbl_preview_image)
		self.data_layout.addWidget(self.labels_frame)
		self.data_layout.setContentsMargins(0, 0, 0, 0)
		self.data_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.data_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addWidget(self.header_frame)
		self.main_layout.addWidget(self.data_frame)
		self.main_layout.setAlignment(QtCore.Qt.AlignTop)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

	def update_widget(self, index_source=None):

		if index_source.isValid():
			if index_source.column() == 1:
				index_source_col1 = index_source.model().index(index_source.row(), 0, index_source.parent())
				index_source = index_source_col1

			index_icon = index_source.data(role=QtCore.Qt.UserRole + 2)
			index_pixmap = index_icon.pixmap(1024, 1024)

			# Update header
			self.lbl_preview_image.update_pixmap(index_pixmap)
			self.btn_icon_type.setIcon(index_source.data(role=QtCore.Qt.DecorationRole))
			self.lbl_name.setText(index_source.data(role=QtCore.Qt.DisplayRole))
			self.lbl_type.setText(self._format_type(index_source.data(role=QtCore.Qt.UserRole + 19)))

			self.lbl_assignee.setText(index_source.data(QtCore.Qt.UserRole + 14))
			self.lbl_due.setText(index_source.data(QtCore.Qt.UserRole + 15))
			self.lbl_priority.setText(index_source.data(QtCore.Qt.UserRole + 16))
			# self.lbl_tags.setText(index_source.data(QtCore.Qt.UserRole + 17)) todo:: create tags widget
			self.lbl_progress.setText(index_source.data(QtCore.Qt.UserRole + 18))

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
