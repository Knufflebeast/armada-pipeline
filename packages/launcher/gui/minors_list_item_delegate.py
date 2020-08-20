
# import importlib
from Qt.QtGui import QColor, QFont, QPainterPath, QPainter, QPen, QFontMetrics
from Qt.QtWidgets import QStyledItemDelegate, QStyle, QApplication, QStyleOptionButton, QPushButton
from Qt.QtCore import Qt, Signal, QEvent, QModelIndex, QRect, QSize

from core import armada


# from utilsa.logger import Logger
# logging = Logger('armada')


class MinorsListItemDelegate(QStyledItemDelegate):

	softwareLaunched = Signal(QModelIndex)

	def __init__(self, parent=None):
		"""
		:param item: str - Dir_Name.dirType
		"""
		super(MinorsListItemDelegate, self).__init__(parent)
		# self.logger = logging.getLogger('gui.' + self.__class__.__name__)

		self._spacing = 10
		self._icon_size = 80

		self.launch = FloatingButton()


	def sizeHint(self, option, index):

		my_fixed_height = 100
		proxy = index.model()
		base_index = proxy.mapToSource(index)

		if index.column() == 0:
			size = super(MinorsListItemDelegate, self).sizeHint(option, base_index)
			size.setHeight(my_fixed_height)
			return size

		else:
			return super(MinorsListItemDelegate, self).sizeHint(option, base_index)

	def editorEvent(self, event, model, option, index):

		# Launch app when launch button clicked
		if event.type() == QEvent.MouseButtonRelease:
			click_pos = event.pos()
			rect_launch = self.rect_launch

			if rect_launch.contains(click_pos):
				self.softwareLaunched.emit(index)
				return True
			else:
				return False
		else:
			return False

	def paint(self, painter, option, index):

		painter.setRenderHint(QPainter.Antialiasing, True)
		painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
		painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

		# Rect
		rect_item = option.rect

		# Background
		painter.setPen(Qt.NoPen)

		# Rects

		# Image
		rect_image = QRect(
			rect_item.left() + 9,
			rect_item.top() + 7,  # (rect_item.height() - (rect_item.top() - icon_size)) / 2,
			115 ,
			rect_item.height() - 16
		)

		# Software icon
		rect_software = QRect(
			rect_image.right() + self._spacing,
			rect_image.top(),
			25,
			rect_image.height() / 2
		)

		# BG rect
		sel_width = 5
		rect_item_sel = QRect(
			rect_item.right(),
			rect_item.top(),
			-sel_width,
			rect_item.height()-1)

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

		# Image
		painter.save()
		# Image backdrop
		painter.setBrush(QColor('#3A3A3A'))
		painter.drawRect(rect_image)

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

		# Software icon
		icon_type = index.data(role=Qt.DecorationRole)
		pixmap_icon = icon_type.pixmap(128, 128)
		pixmap_icon_scaled = pixmap_icon.scaled(
			rect_software.width(),
			rect_software.height(),
			Qt.KeepAspectRatio,
			Qt.FastTransformation
		)
		QApplication.style().drawItemPixmap(
			painter,
			rect_software,
			Qt.AlignVCenter | Qt.AlignLeft,
			pixmap_icon_scaled
		)

		# Name
		name_index = index.data(role=Qt.DisplayRole)
		name_font = QFont("Segoe UI", 12, QFont.DemiBold | QFont.NoAntialias)
		font_metrics = QFontMetrics(name_font)
		name_width = font_metrics.boundingRect(name_index).width()
		rect_name = QRect(
			rect_software.right() + self._spacing,
			rect_image.top(),
			name_width,
			rect_image.height() / 2
		)
		painter.setPen(QColor(255, 255, 255))
		painter.setFont(name_font)
		QApplication.style().drawItemText(
			painter,
			rect_name,
			Qt.AlignVCenter | Qt.AlignLeft,
			QApplication.palette(),
			True,
			name_index
		)

		# User avatar
		user_avatar = index.data(role=Qt.UserRole + 5)
		avatar_ratio = 4
		avatar_size = 25  # int(rect_icon_target.width()/avatar_ratio)
		rect_avatar = QRect(
			rect_image.right() + self._spacing,
			rect_name.bottom(),
			avatar_size,
			rect_image.height() / 2
		)
		if user_avatar:
			pixmap_avatar = armada.resource.pixmap(user_avatar)
			pixmap_avatar_scaled = pixmap_avatar.scaled(
				rect_avatar.width(),
				rect_avatar.height(),
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation
			)
			painter.save()
			path = QPainterPath()
			path.addRoundedRect(
				rect_avatar.left(),
				rect_avatar.top() + 9,
				rect_avatar.width(),
				avatar_size,
				avatar_size,
				avatar_size
			)
			painter.setClipPath(path)
			QApplication.style().drawItemPixmap(
				painter,
				rect_avatar,
				Qt.AlignVCenter | Qt.AlignLeft,
				pixmap_avatar_scaled
			)
			painter.restore()

		# Date Rect
		index_date = index.data(role=Qt.UserRole + 4)
		# Date
		date_font = QFont("Segoe UI", 8, QFont.Light | QFont.NoAntialias)
		font_metrics = QFontMetrics(date_font)
		date_width = font_metrics.boundingRect(index_date).width()
		rect_date = QRect(
			rect_avatar.right() + self._spacing,
			rect_name.bottom(),
			date_width,
			rect_image.height() / 2
		)

		painter.setPen(QColor(255, 255, 255))
		painter.setFont(date_font)
		QApplication.style().drawItemText(
			painter,
			rect_date,
			Qt.AlignVCenter | Qt.AlignLeft,
			QApplication.palette(),
			True,
			index_date
		)

		# Line bottom
		painter.setPen(QPen(QColor(255, 255, 255, 75), 1))
		painter.drawLine(
			rect_item.left() + self._spacing,
			rect_item.bottom(),
			rect_item.width() - self._spacing,
			rect_item.bottom()
		)

		# Comments
		index_comment = index.data(role=Qt.UserRole + 6)
		if index_comment:
			comment_font = QFont("Segoe UI", 10, QFont.NoAntialias)
			painter.setFont(comment_font)
			painter.setPen(QColor(255, 255, 255))

			# Comment
			rect_comment = QRect(
				rect_date.right() + self._spacing,
				rect_item.top() + 7,
				(rect_item.width() / 2) - 50,
				rect_image.height()
			)

			QApplication.style().drawItemText(
				painter,
				rect_comment,
				Qt.AlignLeft | Qt.TextWrapAnywhere,
				QApplication.palette(),
				True,
				index_comment
			)

		# Launch
		if index.data(role=Qt.UserRole + 19) == 'minor_component':
			painter.save()
			option = QStyleOptionButton()
			option.initFrom(self.launch)

			# Launch
			launch_icon_size = 30
			rect_launch = QRect(
				rect_item.right() - launch_icon_size - self._spacing,
				rect_item.bottom() - int(rect_item.height() / 2) - int(launch_icon_size / 2),
				launch_icon_size,
				launch_icon_size
			)
			self.rect_launch = rect_launch  # This is set for the eventfilter
			option.rect = rect_launch

			if self.launch.isDown():
				option.state = QStyle.State_Sunken
			else:
				pass

			if self.launch.isDefault():
				option.features = option.features or QStyleOptionButton.DefaultButton

			option.icon = self.launch.icon()
			option.iconSize = QSize(30, 30)

			self.launch.style().drawControl(QStyle.CE_PushButton, option, painter, self.launch)
			painter.restore()
			##############################
			# option = QStyleOptionButton()
			# option.initFrom(self.launch)
			# option.rect = rect_launch
			#
			# if self.launch.isDown():
			# 	option.state = QStyle.State_Sunken
			# else:
			# 	pass
			#
			# if self.launch.isDefault():
			# 	option.features = option.features or QStyleOptionButton.DefaultButton
			#
			# option.icon = self.launch.icon()
			#
			# option.iconSize = QSize(40, 40)
			#
			# self.launch.style().drawControl(QStyle.CE_PushButton, option, painter, self.launch)

			##########################
			# btn = QStyleOptionButton()
			# btn.rect = rect_launch
			# launch_icon = resource.color_svg('launch', 128, '#FFFFFF')
			# btn.icon = launch_icon
			# btn.iconSize = QSize(launch_icon_size, launch_icon_size)
			#
			# # btn.state = QStyle.State_Enabled | (
			# # 	QStyle.State_MouseOver if option.state & QStyle.State_MouseOver else QStyle.State_None)
			#
			# if btn.state & QStyle.State_Selected:
			# 	sel = 1
			# 	painter.setBrush(QColor('#4b4b4b'))
			#
			# elif btn.state & QStyle.State_MouseOver:
			# 	sel = 0
			# 	painter.setBrush(QColor('#323232'))
			#
			# else:
			# 	sel = 0
			# 	painter.setBrush(QColor('#00000000'))
			#
			# btn.palette = QColor('#000000')
			#
			# QApplication.style().drawControl(QStyle.CE_PushButtonLabel, btn, painter)


class FloatingButton(QPushButton):
	def __init__(self, parent=None):
		super(FloatingButton, self).__init__(parent)

		# self.setLayout(QHBoxLayout())
		# size = 80
		# self.setFixedSize(size, size)

		self.setIcon(armada.resource.color_svg('launch', 128, '#FFFFFF'))
		self.setStyleSheet("""
			QPushButton{
				background:#00000000;
				height: 30px;
				font: 12px "Roboto-Thin";
				border-radius: 40
			}
			QPushButton:hover{
				background: #2fa89b;
			}
			# QPushButton:hover:pressed{
			# 	background: #2c998e;
			# }
			QPushButton:pressed{
				background:  #32ada9;
			}
			""")

	# def paintEvent(self, qpaintevent):
	# 	option = QStyleOptionButton()
	# 	option.initFrom(self)
	#
	# 	if self.isDown():
	# 		option.state = QStyle.State_Sunken
	# 	else:
	# 		pass
	#
	# 	if self.isDefault():
	# 		option.features = option.features or QStyleOptionButton.DefaultButton
	# 	option.text = self.text()
	# 	option.icon = self.icon()
	# 	option.iconSize = QSize(40, 40)
	#
	# 	painter = QPainter(self)
	# 	self.style().drawControl(QStyle.CE_PushButton, option, painter, self)

