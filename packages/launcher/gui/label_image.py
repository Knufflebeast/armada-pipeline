from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore

from core import armada

class LabelImage(QtWidgets.QLabel):
	"""Scales image to fit within q label

	Image can be rounded or not

	"""
	def __init__(self, name, antialiasing=True, size=30, rounded=True, **kwargs):
		super(LabelImage, self).__init__(**kwargs)

		self.Antialiasing = antialiasing
		self.setMaximumSize(size, size)
		self.setMinimumSize(size, size)


		self.target = QtGui.QPixmap(self.size())
		self.target.fill(QtCore.Qt.transparent)

		pixmap = armada.resource.pixmap(name)
		pixmap_scaled = pixmap.scaled(
			size, size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

		painter = QtGui.QPainter(self.target)
		if self.Antialiasing:
			painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
			painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
			painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

		path = QtGui.QPainterPath()
		# If sides will be rounded
		if rounded:
			self.radius = size / 2
			path.addRoundedRect(
				0, 0, self.width(), self.height(), self.radius, self.radius)

		painter.setClipPath(path)
		painter.drawPixmap(0, 0, pixmap_scaled)
		self.setPixmap(self.target)
