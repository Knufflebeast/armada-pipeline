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

from core import resource

import utilsa

logging = utilsa.Logger('armada')

ABOUT_YOU, WORKSPACE, PROJECT = 0, 2, 4


class BreadcrumbStartupSteps(QtWidgets.QTabBar):
	"""
	.. note::
		When a tab is selected a ``currentChanged`` `signal` is sent to the :ref:`main_stacked_widget's <main_stacked_widget>`
		``setCurrentIndex`` `slot.`

		This connection is set in the :ref:`main_window <main_window>` widget.
	"""

	breadcrumbIndexChanged = QtCore.Signal(int)

	def __init__(self, parent=None):
		super(BreadcrumbStartupSteps, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building main tab tab...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent

		self.setMinimumHeight(37)
		self.setDrawBase(False)  # Removes line under and between base of tabs
		self.setIconSize(QtCore.QSize(24, 24))
		self.setStyleSheet("""
			QTabBar{
				font: 10px "Segoe UI";
				background-color: rgba(90, 90, 90, 0);
			}

			QTabBar::tab {
				font: 10px "Segoe UI";
				background-color: rgba(90, 90, 90, 0);
				spacing:5;
			}

			QTabBar::tab::selected{
				color: #FFFFFF;
				font: 10px "Segoe UI bold";
				background-color: #2c998e;
			}
			QTabBar::tab:hover:selected{
				color: #FFFFFF;
				background-color: #2c998e;
			}
			QTabBar::tab::!selected{
				color: #FFFFFF;
				background-color: #5a5a5a;
			}
			QTabBar::tab:hover{
				color: #FFFFFF;
				background-color: #999998;
			}
			QTabBar::tab:disabled{
				color: #FFFFFF;
				background-color: rgba(0, 0, 0, 0);
				padding-right: -9px;
				padding-left: -9px;
			}

			QTabBar::tear {
				width: 0px;
			}
			QTabBar::scroller{
				width: 0;
			}
		""")

		tab = self.addTab('ABOUT YOU')

		icon = resource.color_svg('arrow_right', 128, '#a6a6a6')
		tab = self.addTab(icon, '')
		self.setTabEnabled(tab, False)

		self.addTab('CREATE WORKSPACE')

		icon = resource.color_svg('arrow_right', 128, '#a6a6a6')
		tab = self.addTab(icon, '')
		self.setTabEnabled(tab, False)

		self.addTab('ADD YOUR FIRST PROJECT')

		# Connections ------------------------------------------
		self.currentChanged.connect(self._on_index_changed)

	def _on_index_changed(self):
		index_map = {
			0: 0,
			2: 1,
			4: 2
		}
		# Send current breadcrumb widget to creation_flow_widget
		self.breadcrumbIndexChanged.emit(index_map[self.currentIndex()])


	def paintEvent(self, _e):
		"""Override paintEvent to draw the tabs like we want to.
		Args:
			_e: QPaintEvent
		Returns:
		"""
		# super(BreadcrumbStartupSteps, self).paintEvent(_e)

		painter = QtWidgets.QStylePainter(self)
		tab = QtWidgets.QStyleOptionTab()

		for idx in range(self.count()):
			# painter.begin(self)
			self.initStyleOption(tab, idx)

			# Draw arrow
			if tab.text is '':
				painter.setRenderHint(QtGui.QPainter.Antialiasing)

				# Icon
				index_icon = tab.icon
				icon_size = 20

				pixmap_icon = index_icon.pixmap(128, 128)

				pixmap_icon_scaled = pixmap_icon.scaled(
					icon_size,
					icon_size,
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation
				)
				painter.save()

				QtWidgets.QApplication.style().drawItemPixmap(
					painter,
					tab.rect,
					QtCore.Qt.AlignCenter,
					pixmap_icon_scaled
				)
				painter.restore()

			else:
				painter.setRenderHint(QtGui.QPainter.Antialiasing)

				painter.save()
				# Change color on state
				if tab.state & QtWidgets.QStyle.State_MouseOver:
					color = '#FFFFFF'
				elif tab.state & QtWidgets.QStyle.State_Selected:
					color = '#FFFFFF'
				else:
					color = '#a6a6a6'

				painter.setPen(QtGui.QColor(color))
				# painter.setFont(font_name)

				QtWidgets.QApplication.style().drawItemText(
					painter,
					tab.rect,
					QtCore.Qt.AlignCenter,
					tab.palette,
					True,
					tab.text
				)
				painter.restore()

				# # Selection bottom rectangle
				# path = QtGui.QPainterPath()
				# path.addRect(
				# 	tab.rect.left(),
				# 	tab.rect.top() + tab.rect.height() - 5,
				# 	tab.rect.width(),
				# 	5
				# )
				#
				# # Change color on state
				# if tab.state & QtWidgets.QStyle.State_MouseOver:
				# 	painter.fillPath(path, QtGui.QColor('#5a5a5a'))
				# if tab.state & QtWidgets.QStyle.State_Selected:
				# 	painter.fillPath(path, QtGui.QColor('#2c998e'))
				# else:
				# 	painter.fillPath(path, QtGui.QColor('transparent'))

			# Don't bother drawing a tab if the entire tab is outside of
			# the visible tab bar.
			if tab.rect.right() < 0 or tab.rect.left() > self.width():
				continue


