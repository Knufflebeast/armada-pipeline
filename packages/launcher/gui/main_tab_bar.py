""".. _main_tab_bar:

mb_armada.gui.main_tab_bar
*************************

.. image:: /images/main_tab_bar.png

- Tab bar for the :ref:`main_window <main_window>`
- Select between :ref:`projects <projects_context>`, :ref:`assets <assets_context>`, and :ref:`tasks <tasks_context>`
  contexts
"""

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from core import armada

import utilsa

logging = utilsa.Logger('armada')


class MainTabBar(QtWidgets.QTabBar):
	"""
	.. note::
		When a tab is selected a ``currentChanged`` `signal` is sent to the :ref:`main_stacked_widget's <main_stacked_widget>`
		``setCurrentIndex`` `slot.`

		This connection is set in the :ref:`main_window <main_window>` widget.
	"""

	def __init__(self, parent=None):
		super(MainTabBar, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building main tab tab...')

		self.parent = parent
		self.setObjectName('armada_MainTabBar')
		self.setMinimumHeight(37)
		self.setDrawBase(False)  # Removes line under and between base of tabs
		self.setIconSize(QtCore.QSize(24, 24))
		self.setStyleSheet(armada.resource.style_sheet('tabbar_main'))

		icon = armada.resource.color_svg('folder_project', 128, 'black')
		self.addTab(icon, 'Projects')
		icon = armada.resource.color_svg('folder_asset', 128, 'black')
		self.addTab(icon, 'Assets')
		icon = armada.resource.color_svg('asana_logo', 128, 'black')
		self.addTab(icon, 'Tasks')

		self.setCurrentIndex(0)

	def paintEvent(self, _e):
		"""Override paintEvent to draw the tabs like we want to.
		Args:
			_e: QPaintEvent
		Returns:
		"""

		painter = QtWidgets.QStylePainter(self)
		tab = QtWidgets.QStyleOptionTab()

		for idx in range(self.count()):
			# painter.begin(self)
			self.initStyleOption(tab, idx)

			# Draw tab
			if tab.text is not '':
				painter.setRenderHint(QtGui.QPainter.Antialiasing)

				# Icon
				index_icon = tab.icon
				icon_size = 20

				rect_icon = QtCore.QRect(
					tab.rect.left() + 10,
					tab.rect.top() - 2,
					icon_size,
					tab.rect.height()
				)

				pixmap_icon = index_icon.pixmap(128, 128)

				# Change color on state
				mask = pixmap_icon.createMaskFromColor(QtGui.QColor('black'), QtCore.Qt.MaskOutColor)
				if tab.state & QtWidgets.QStyle.State_MouseOver:
					pixmap_icon.fill((QtGui.QColor('#5a5a5a')))
				if tab.state & QtWidgets.QStyle.State_Selected:
					pixmap_icon.fill((QtGui.QColor('#FFFFFF')))
				else:
					pixmap_icon.fill((QtGui.QColor('#CDCDCD')))
				pixmap_icon.setMask(mask)

				pixmap_icon_scaled = pixmap_icon.scaled(
					icon_size,
					icon_size,
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation
				)
				painter.save()
				QtWidgets.QApplication.style().drawItemPixmap(
					painter,
					rect_icon,
					QtCore.Qt.AlignCenter,
					pixmap_icon_scaled
				)
				painter.restore()

				# Name
				rect_text = QtCore.QRect(
					rect_icon.right() + 5,
					tab.rect.top() - 5,
					tab.rect.width(),
					tab.rect.height() + 2
				)
				painter.save()
				font_name = QtGui.QFont("Segoe UI", 12, QtGui.QFont.Normal)
				painter.setFont(font_name)

				# Change color on state
				if tab.state & QtWidgets.QStyle.State_MouseOver:
					color = '#5a5a5a'
				# font_name = QFont("Segoe UI Bold", 11, QFont.Normal)
				if tab.state & QtWidgets.QStyle.State_Selected:
					color = '#FFFFFF'
				# font_name = QFont("Segoe UI Bold", 11, QFont.Normal)
				else:
					color = '#CDCDCD'

				painter.setPen(QtGui.QColor(color))
				# painter.setFont(font_name)
				QtWidgets.QApplication.style().drawItemText(
					painter,
					rect_text,
					QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
					tab.palette,
					True,
					tab.text
				)
				painter.restore()

				# Selection bottom rectangle
				path = QtGui.QPainterPath()
				path.addRect(
					tab.rect.left(),
					tab.rect.top() + tab.rect.height() - 5,
					tab.rect.width(),
					5
				)

				# Change color on state
				if tab.state & QtWidgets.QStyle.State_MouseOver:
					painter.fillPath(path, QtGui.QColor('#5a5a5a'))
				if tab.state & QtWidgets.QStyle.State_Selected:
					painter.fillPath(path, QtGui.QColor('#2c998e'))
				else:
					painter.fillPath(path, QtGui.QColor('transparent'))

			# Don't bother drawing a tab if the entire tab is outside of
			# the visible tab bar.
			if tab.rect.right() < 0 or tab.rect.left() > self.width():
				continue


