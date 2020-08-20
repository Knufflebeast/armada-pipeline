from Qt import QtGui
from Qt.QtWidgets import QStyledItemDelegate, QLineEdit, QStyle, QApplication
from Qt.QtCore import Qt, Signal, QRect

from utilsa.logger import Logger
logging = Logger('marina')


class LibraryItemDelegate(QStyledItemDelegate):

	delegateItemRenamed = Signal()

	def __init__(self, parent):
		"""
		:param parent: str - Dir_Name.dirType
		"""
		super(LibraryItemDelegate, self).__init__(parent)

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)

		self._spacing = 0
		self._icon_size = 25

	def sizeHint(self, option, index):

		if index.column() == 0:
			width = 150
			height = 225

			# if index.column() == 0:
			size = super(LibraryItemDelegate, self).sizeHint(option, index)

			# if option.state & QStyle.State_Selected:
			# 	width = 100
			# elif option.state & QStyle.State_MouseOver:
			# 	width = 100
			# else:
			# 	width = 200

			size.setWidth(width + 2 * self._spacing)
			size.setHeight(height)
			return size

		else:
			return super(LibraryItemDelegate, self).sizeHint(option, index)

	# def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: 'QStyleOptionViewItem', index: QModelIndex) -> bool:
	#
	# 	# Launch app when launch button clicked
	# 	if event.type() == QEvent.MouseButtonRelease:
	# 		click_pos = event.pos()
	# 		rect_launch = self.rect_launch
	#
	# 		if rect_launch.contains(click_pos):
	# 			launcher_path = os.path.join(
	# 				os.getenv('_SOURCE_DIR'),
	# 				'mb_armada', 'hooks', 'launchers',
	# 				'{}_hook.py'.format(index.data(Qt.UserRole + 3))
	# 			)
	#
	# 			spec = importlib.util.spec_from_file_location("painter_hook.name", launcher_path)
	# 			software_hook = importlib.util.module_from_spec(spec)
	# 			spec.loader.exec_module(software_hook)
	# 			software_hook.Launch(index)
	#
	# 			return True
	#
	# 		else:
	#
	# 			return False
	#
	# 	else:
	# 		return False

	def createEditor(self, parent, option, index):
		# index_type = index.model().index(index.row(), 0, index.parent()).data(Qt.UserRole + 1)
		software_id = index.model().index(index.row(), 0, index.parent()).data(Qt.UserRole + 19)

		if software_id == 'minor_component':
			pass

		elif index.column() == 0:
			editor = QLineEdit(parent)
			editor.textChanged.connect(lambda: self.on_text_changed(editor, index))
			return editor

		else:  # Don't create editor
			pass

	def setModelData(self, editor, model, index):
		"""Set underlying model data after editing is done"""
		# Rename dirs
		self.rename_directories(editor, index)
		# Update model
		base_model = model.sourceModel()
		base_index = model.mapToSource(index)
		base_model.setData(base_index, editor.text(), Qt.DisplayRole)
		self.commitData.emit(editor)
		self.delegateItemRenamed.emit()

		# return super(FoldersItemDelegate, self).setModelData(editor, model, index)

	def updateEditorGeometry(self, editor, option, index):
		"""Editor visual settings"""
		# Rects
		rect_image = QRect(
			option.rect.left() + self._spacing,
			option.rect.top(),
			option.rect.width() - (2 * self._spacing),
			option.rect.height() - int(option.rect.height()/2)
		)
		rect_data = QRect(
			option.rect.left() + self._spacing,
			rect_image.bottom(),
			option.rect.width() - (2 * self._spacing),
			option.rect.height() - int(option.rect.height()/2)
		)
		pad_data = 15
		rect_icon_type = QRect(
			option.rect.left() + self._spacing,
			rect_data.top() + self._spacing,
			self._icon_size,
			int((rect_image.height()/3)/2)
		)
		rect_name = QRect(
			rect_icon_type.right() + pad_data,
			rect_data.top() + 10,
			option.rect.width(),
			int((rect_image.height()/3)/2)
		)
		editor.setGeometry(rect_name)

	def paint(self, painter, option, index):

		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
		# painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

		# Rect
		rect_item = option.rect

		# Background
		painter.setPen(Qt.NoPen)

		# Rects
		rect_image = QRect(
			rect_item.left() + self._spacing,
			rect_item.top(),
			rect_item.width() - (2 * self._spacing),
			rect_item.height() - int(rect_item.height()/2)
		)
		rect_data = QRect(
			rect_item.left() + self._spacing,
			rect_image.bottom(),
			rect_item.width() - (2 * self._spacing),
			rect_item.height() - int(rect_item.height()/2)
		)

		pad_data = 5
		app_icon_width = 30
		rect_app_icon = QRect(
			rect_item.right() - pad_data - app_icon_width - self._spacing,
			rect_data.top() - pad_data - app_icon_width,
			app_icon_width,
			app_icon_width
		)

		rect_icon_type = QRect(
			rect_item.left() + self._spacing,
			rect_data.top() + self._spacing,
			self._icon_size,
			int((rect_image.height()/3)/2)
		)
		rect_name = QRect(
			rect_icon_type.right() + pad_data,
			rect_data.top() + 10,
			rect_item.width(),
			int((rect_image.height()/3)/2)
		)
		rect_date = QRect(
			rect_icon_type.right() + pad_data,
			rect_name.bottom(),
			rect_item.width() - pad_data,
			int((rect_image.height()/3) / 2)
		)
		rect_comment = QRect(
			rect_item.left() + pad_data + self._spacing,
			int(rect_date.bottom() + (pad_data / 2)),
			rect_item.width() - (pad_data * 2),
			int((rect_image.height()*.666) - (pad_data * 2) + self._spacing)
		)

		# Top half
		painter.save()
		painter.setBrush(QtGui.QColor('#3A3A3A'))
		painter.drawRect(rect_image)
		painter.restore()

		# Bot half
		painter.save()
		if option.state & QStyle.State_Selected:
			painter.setBrush(QtGui.QColor(0, 149, 119))
		elif option.state & QStyle.State_MouseOver:
			painter.setBrush(QtGui.QColor(100, 100, 100))
		else:
			painter.setBrush(QtGui.QColor('#4F4F4F'))

		painter.drawRect(rect_data)
		painter.restore()

		# Image
		painter.save()
		index_image = index.data(role=Qt.UserRole + 2)
		index_pixmap = index_image.pixmap(1024, 1024)
		pixmap_scaled = index_pixmap.scaled(
			rect_image.width(),
			rect_image.height(),
			Qt.KeepAspectRatio,
			Qt.SmoothTransformation
		)
		QApplication.style().drawItemPixmap(
			painter,
			rect_image,
			Qt.AlignCenter,
			pixmap_scaled)
		painter.restore()

		# Icon
		icon_type = index.data(role=Qt.DecorationRole)
		pixmap_icon = icon_type.pixmap(128, 128)
		pixmap_icon_scaled = pixmap_icon.scaled(
			rect_icon_type.width(),
			rect_icon_type.height(),
			Qt.KeepAspectRatio,
			Qt.FastTransformation
		)
		QApplication.style().drawItemPixmap(
			painter,
			rect_icon_type,
			Qt.AlignVCenter | Qt.AlignLeft,
			pixmap_icon_scaled
		)

		# Primary Title
		painter.setPen(QtGui.QColor(255, 255, 255))
		# Name
		name_index = index.data(role=Qt.DisplayRole)
		name_font = QtGui.QFont("Segoe UI", 12, QtGui.QFont.DemiBold | QtGui.QFont.NoAntialias)
		painter.setFont(name_font)
		QApplication.style().drawItemText(
			painter,
			rect_name,
			Qt.AlignVCenter | Qt.AlignLeft,
			QApplication.palette(),
			True,
			name_index
		)

		# Secondary Rect
		if index.data(role=Qt.UserRole + 19) == 'major_component':
			# Show item type
			index_date = index.data(role=Qt.UserRole + 7)
		elif index.data(role=Qt.UserRole + 19) == 'minor_component':
			# Show date
			index_date = index.data(role=Qt.UserRole + 4)
		else:
			index_date = index.data(role=Qt.UserRole + 9)

		date_font = QtGui.QFont("Segoe UI", 8, QtGui.QFont.Light | QtGui.QFont.NoAntialias)
		painter.setFont(date_font)
		painter.setPen(QtGui.QColor(255, 255, 255))
		QApplication.style().drawItemText(
			painter,
			rect_date,
			Qt.AlignLeft | Qt.AlignTop,
			QApplication.palette(),
			True,
			index_date
		)

		# Line
		painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 75), .5))
		painter.drawLine(
			rect_item.left() + self._spacing,
			rect_date.bottom(),
			rect_item.right() - self._spacing,
			rect_date.bottom()
		)

		# Comments
		index_comment = index.data(role=Qt.UserRole + 6)
		if index_comment:
			comment_font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.NoAntialias)
			painter.setFont(comment_font)
			painter.setPen(QtGui.QColor(255, 255, 255))
			QApplication.style().drawItemText(
				painter,
				rect_comment,
				Qt.AlignLeft | Qt.TextWrapAnywhere,
				QApplication.palette(),
				True,
				index_comment
			)

		# Actions
		if index.data(role=Qt.UserRole + 1) == 'major_component':
			# Icon
			icon_type = index.data(role=Qt.UserRole + 13)
			pixmap_icon = icon_type.pixmap(128, 128)
			pixmap_icon_scaled = pixmap_icon.scaled(
				rect_app_icon.width(),
				rect_app_icon.height(),
				Qt.KeepAspectRatio,
				Qt.FastTransformation
			)
			QApplication.style().drawItemPixmap(
				painter,
				rect_app_icon,
				Qt.AlignCenter,
				pixmap_icon_scaled
			)


			# btn = QStyleOptionButton()
			# btn.rect = rect_launch
			# launch_icon = resource.color_svg('launch', 128, '#FFFFFF')
			# btn.icon = launch_icon
			# btn.iconSize = QSize(launch_icon_width, launch_icon_width)
			# btn.state = QStyle.State_Enabled | (
			# 	QStyle.State_MouseOver if option.state & QStyle.State_MouseOver else QStyle.State_None
			# )
			#
			# btn.palette = QtGui.QColor('#000000')
			#
			# # if option.state & QtWidgets.QStyle.State_Selected:
			# # 	painter.setBrush(QtGui.QColor(0, 149, 119))
			# # elif option.state & QtWidgets.QStyle.State_MouseOver:
			# # 	painter.setBrush(QtGui.QColor(100, 100, 100))
			# # else:
			# # 	painter.setBrush(QtGui.QColor(67, 67, 67))
			#
			# QApplication.style().drawControl(QStyle.CE_PushButtonLabel, btn, painter)


