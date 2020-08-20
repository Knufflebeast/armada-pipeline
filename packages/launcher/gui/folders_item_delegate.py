import shutil

from Qt.QtGui import QPainter, QColor, QFont
from Qt.QtCore import Qt, Signal, QRect
from Qt.QtWidgets import QStyledItemDelegate, QStyle, QApplication, QLineEdit

from core import armada

import utilsa
logging = utilsa.Logger('armada')


class FoldersItemDelegate(QStyledItemDelegate):

	delegateComboSelectionChanged = Signal()
	delegateItemRenamed = Signal()

	def __init__(self, parent=None):
		"""
		:param item: str - Dir_Name.dirType
		"""
		super(FoldersItemDelegate, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

		self.icon_size = 25
		self.padding = 5

	def sizeHint(self, option, index):
		my_fixed_height = 40

		proxy = index.model()
		base_index = proxy.mapToSource(index)

		if index.column() == 0:
			size = super(FoldersItemDelegate, self).sizeHint(option, base_index)
			size.setHeight(my_fixed_height)
			return size

		if index.column() == 1:
			size = super(FoldersItemDelegate, self).sizeHint(option, base_index)
			size.setWidth(50)
			return size

		else:
			return super(FoldersItemDelegate, self).sizeHint(option, base_index)

	def paint(self, painter, option, index):

		painter.setRenderHint(QPainter.Antialiasing, True)
		painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
		painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
		painter.setPen(Qt.NoPen)

		rect_item = option.rect

		if index.column() == 1:
			sel_width = 5
			rect_item_sel = QRect(
				rect_item.right(),
				rect_item.top(),
				-sel_width,
				rect_item.height())

			painter.save()
			if option.state & QStyle.State_Selected:
				sel = 1
				painter.setBrush(QColor('#4b4b4b'))

			elif option.state & QStyle.State_MouseOver:
				sel = 0
				painter.setBrush(QColor('#323232'))

			else:
				sel = 0
				painter.setBrush(QColor('#00000000'))

			painter.drawRect(option.rect)

			if sel:
				painter.setBrush(QColor('#2c998e'))
				painter.drawRect(rect_item_sel)

			painter.restore()


			# Image or combobox
			# Type from column 0 data
			index_type = index.model().index(index.row(), 0, index.parent()).data(Qt.UserRole + 1)
			rect_image = QRect(
				rect_item.left() + 6,
				rect_item.top(),
				rect_item.width() - 12,
				rect_item.height()
			)
			if index_type == 'asset' or index_type == 'client':  # or index_type == 'asset_component':
				# Image from column 0 data
				index_image = index.model().index(index.row(), 0, index.parent()).data(Qt.UserRole + 2)  # Item image

				painter.save()
				pixmap_image = index_image.pixmap(1024, 1024)

				pixmap_image_scaled = pixmap_image.scaled(
					rect_image.width(),
					rect_image.height(),
					Qt.KeepAspectRatio,
					Qt.SmoothTransformation)

				QApplication.style().drawItemPixmap(
					painter,
					rect_image,
					Qt.AlignCenter,
					pixmap_image_scaled)

				painter.restore()

		if index.column() == 0:
			rect_icon_target = QRect(
				rect_item.left(),
				rect_item.top(), #(rect_item.height() - (rect_item.top() - icon_size)) / 2,
				self.icon_size,
				rect_item.height())
			rect_name_target = QRect(
				rect_icon_target.right() + self.padding,
				rect_item.top(),
				rect_item.width() - self.padding,
				rect_item.height())

			# BG
			painter.save()
			if option.state & QStyle.State_Selected:
				sel = 1
				painter.setBrush(QColor('#4b4b4b'))

			elif option.state & QStyle.State_MouseOver:
				sel = 0
				painter.setBrush(QColor('#323232'))

			else:
				sel = 0
				painter.setBrush(QColor('#00000000'))

			painter.drawRect(option.rect)
			painter.restore()

			# Icon
			painter.save()
			index_icon = index.data(role=Qt.DecorationRole)
			pixmap_icon = index_icon.pixmap(64, 64)
			pixmap_icon_scaled = pixmap_icon.scaled(
				rect_icon_target.width()-2,
				rect_icon_target.height()-2,
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation)
			QApplication.style().drawItemPixmap(
				painter,
				rect_icon_target,
				Qt.AlignCenter,
				pixmap_icon_scaled)

			painter.restore()

			# Name
			# Primary Title
			painter.save()
			index_name = index.data(role=Qt.DisplayRole)
			font_name = QFont("Segoe UI", 12, QFont.Normal)
			painter.setPen(QColor(255, 255, 255))
			painter.setFont(font_name)

			QApplication.style().drawItemText(
				painter,
				rect_name_target,
				Qt.AlignLeft | Qt.AlignVCenter,
				QApplication.palette(),
				True,
				index_name)

			painter.restore()

	def createEditor(self, parent, option, index):
		"""Editor that is created when edit is called"""
		# Only allow asset_components to have combobox edits

		if index.column() == 0:
			editor = QLineEdit(parent)
			editor.textChanged.connect(lambda: self.on_text_changed(editor, index))
			return editor

		else:  # Don't create editor
			pass
			# return super(FoldersItemDelegate, self).createEditor(parent, option, index)

	def setEditorData(self, editor, index):
		"""Set initial data when editing starts"""
		editor.setText(index.data(Qt.DisplayRole))
		# super(FoldersItemDelegate, self).setEditorData(editor, index)

	def setModelData(self, editor, model, index):
		"""Set underlying model data after editing is done"""
		# Rename dirs
		self.rename_directories(editor, index)
		# Update model
		base_model = model.sourceModel()
		base_index = model.mapToSource(index)
		base_model.setData(base_index, editor.text(), Qt.DisplayRole)
		self.delegateItemRenamed.emit()
		self.commitData.emit(editor)

		# return super(FoldersItemDelegate, self).setModelData(editor, model, index)

	def updateEditorGeometry(self, editor, option, index):
		"""Editor visual settings"""
		rect_icon_target = QRect(
			option.rect.left(),
			option.rect.top(),  # (rect_item.height() - (rect_item.top() - icon_size)) / 2,
			self.icon_size,
			option.rect.height())
		rect_name_target = QRect(
			rect_icon_target.right() + self.padding,
			option.rect.top(),
			option.rect.width() - self.padding - self.icon_size,
			option.rect.height())
		editor.setGeometry(rect_name_target)

		# else:
		# 	super(FoldersItemDelegate, self).updateEditorGeometry(editor, option, index)

	def rename_directories(self, editor, index):
		"""Renames directory based on index.

		Rnamed the data dir, updates the name in the data.json file, updates the folder name in the user dir.

		:param editor: QLineEdit
		:param index: Proxy index
		:return:
		"""
		# Get base index
		proxy = index.model()
		base_index = proxy.mapToSource(index)

		# Setup names
		name_init = base_index.data(Qt.DisplayRole)
		self.logger.debug('name_init = {}'.format(name_init))
		name_new = editor.text()
		self.logger.debug('name_new = {}'.format(name_new))

		# Data path abs
		data_path_abs = armada.resolver.generate_path(base_index, armada.resolver.DATA)

		# New data path
		new_data_path_abs = armada.resolver.generate_path(base_index, armada.resolver.DATA).rpartition(name_init)[0]
		new_data_path_abs = armada.resolver.build_path(new_data_path_abs, name_new, return_type='data')

		# Rename
		try:
			# Update json data file
			json_data = armada.resource.json_read(data_path_abs, filename='data')
			json_data['meta_data']['item_name'] = name_new

			# Save json data
			armada.resource.json_save(data_path_abs, filename='data', data=json_data)

			# Rename data path
			shutil.move(data_path_abs, new_data_path_abs)

		except FileNotFoundError:
			self.logger.warning("Can't find data path: {}".format(data_path_abs))

		# User path abs
		user_path_abs = armada.resolver.generate_path(base_index, armada.resolver.USER)

		# Rename
		try:
			# New user path
			new_user_path_abs = armada.resolver.generate_path(base_index, armada.resolver.USER).rpartition(name_init)[0]
			new_user_path_abs = armada.resolver.build_path(new_user_path_abs, name_new, return_type='user')

			# Rename user path
			shutil.move(user_path_abs, new_user_path_abs)

		except FileNotFoundError:
			self.logger.warning("Can't find user path: {}".format(user_path_abs))

	def on_text_changed(self, editor, text):
		"""Restrict characters during rename"""

		# Format text with convention
		typed_name = editor.text()
		conventions = armada.renaming_convention.Convention(typed_name)
		formatted_text = conventions.set_convention(case=conventions.CAPITAL_SNAKE)
		editor.setText(formatted_text)

# class ComboBox(QComboBox):
# 	def __init__(self, parent=None):
# 		super(ComboBox, self).__init__(parent)
#
# 	def paintEvent(self, e: QPaintEvent) -> None:
# 		try:
# 			rect_image = QRect(
# 				self.rect().left() + 6,
# 				self.rect().top(),
# 				self.rect().width() - 12,
# 				self.rect().height()
# 			)
# 			painter = QPainter()
# 			painter.begin(self)
# 			index_icon = self.currentData(Qt.DecorationRole)
# 			pixmap_icon = index_icon.pixmap(128, 128)
# 			pixmap_icon_scaled = pixmap_icon.scaled(
# 				rect_image.width(),
# 				rect_image.height(),
# 				Qt.KeepAspectRatio,
# 				Qt.SmoothTransformation
# 			)
# 			QApplication.style().drawItemPixmap(
# 				painter,
# 				rect_image,
# 				Qt.AlignLeft,
# 				pixmap_icon_scaled
# 			)
# 			painter.end()
#
# 		except AttributeError:
# 			super(ComboBox, self).paintEvent(e)
#
#
# class ComboItem(QStandardItem):
# 	def __init__(self, data=None):
# 		""":param item: str - Dir_Name.dirType
# 		"""
# 		super(ComboItem, self).__init__()
#
# 		# Item meta data
# 		self.item_name = data
# 		self.item_icon = resource.icon(self.item_name, 'png')
#
# 	def data(self, role):
# 		if role == Qt.DisplayRole:  # Name
# 			return self.item_name
# 		if role == Qt.DecorationRole:  # Icon
# 			return self.item_icon

