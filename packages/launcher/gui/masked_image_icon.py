from Qt import QtGui
from Qt import QtCore

from core import armada


def masked_icon(path=None, name='mike.bourbeau', extension='png', antialiasing=True, size=30, **kwargs):
    target = QtGui.QPixmap(QtCore.QSize(size, size))
    target.fill(QtCore.Qt.transparent)

    if path:
        pixmap = armada.resource.pixmap(path=path, name=name, extension=extension)
    else:
        pixmap = armada.resource.pixmap(name)

    pixmap_scaled = pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

    painter = QtGui.QPainter(target)
    if antialiasing:
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

    path = QtGui.QPainterPath()
    path.addRoundedRect(
        0, 0, size, size, size/2, size/2)

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap_scaled)

    return QtGui.QIcon(target)
