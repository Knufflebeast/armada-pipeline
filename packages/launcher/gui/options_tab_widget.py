"""
options_tab_widget
^^^^^^^^^^^^^^^^^^
"""


from Qt import QtWidgets

from packages import launcher

import utilsa

logging = utilsa.Logger('launcher')
logger = logging.getLogger(__name__)

class OptionsTabWidget(QtWidgets.QTabWidget):
	"""Container for options parameters and comment/publish
	"""
	
	def __init__(self, parent=None):
		super(OptionsTabWidget, self).__init__(parent)

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Building options tab widget...')

		self.setMinimumHeight(120)
		self.setMaximumHeight(300)

		# GUI
		self.addTab(launcher.options_tab.OptionsTab(), "Options")

		# Layout
		self.main_layout = QtWidgets.QVBoxLayout()
		#self.main_layout.addWidget( self.option_tab_contents )

		self.setLayout(self.main_layout)
		

