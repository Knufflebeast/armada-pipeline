from Qt import QtGui, QtCore, QtWidgets


class PreviewLabel(QtWidgets.QLabel):
	"""Details widget's preview image

	"""
	def __init__(self, img, parent=None):
		super(PreviewLabel, self).__init__(parent)
		self.setFixedHeight(120)
		self.setFixedWidth(160)
		# self.setMinimumWidth(200)
		self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
		self.pixmap = QtGui.QPixmap(img)
		self.setAlignment(QtCore.Qt.AlignTop)

	def paintEvent(self, event):
		size = self.size()
		painter = QtGui.QPainter(self)
		point = QtCore.QPoint(0, 0)
		scaled_pixmap = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
		# start painting the label from left upper corner
		point.setX((size.width() - scaled_pixmap.width()) / 2)
		point.setY((size.height() - scaled_pixmap.height()) / 2)
		point.x(), ' ', point.y()
		painter.drawPixmap(point, scaled_pixmap)

	def update_pixmap(self, pixmap):
		self.pixmap = pixmap
		self.repaint()
