""".. _main_stacked_widget:

launcher.gui.main_stacked_widget
*********************************

- Selecting tabs in the :ref:`main_tab_bar <main_tab_bar>` will switch to different widgets.
- Select between :ref:`projects_context <projects_context>`, :ref:`assets_context <assets_context>`, and :ref:`tasks_context <tasks_context>`

"""

from Qt.QtWidgets import QStackedWidget

from packages import launcher

import utilsa
logging = utilsa.Logger('armada')


class MainStackedWidget(QStackedWidget):
	"""Switches visible UI based on launcher tab selection

	.. note::
		When a tab in :ref:`main_tab_bar <main_tab_bar>` is selected a ``currentChanged`` `signal` is sent to the
		main_stacked_widget's ``setCurrentIndex`` `slot.`

		This connection is set in the :ref:`main_window <main_window>` widget.
	"""

	def __init__(self, parent=None):
		super(MainStackedWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building main stacked widget...')

		self.parent = parent
		self.setObjectName('armada_MainStackedWidget')

		self.addWidget(launcher.projects_widget.ProjectsWidget(self))
		self.addWidget(launcher.assets_widget.AssetsWidget(self))
		self.addWidget(launcher.tasks_widget.TasksWidget(self))
