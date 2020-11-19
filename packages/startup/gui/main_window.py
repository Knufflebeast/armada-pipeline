"""
Startup main window
"""
import os
import platform
from distutils.dir_util import copy_tree

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource
from core import path_maker
from startup.gui import login_flow
from startup.gui import creation_flow_widget


import utilsa

logging = utilsa.Logger('armada')

USER, WORKSPACE = ('user', 'workspace')


class StartupMainWindow(QtWidgets.QDialog):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(StartupMainWindow, self).__init__()

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Setup starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.armada_root_path = definitions.ROOT_PATH

		self.setWindowIcon(resource.icon('armada_logo', 'png'))
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.resize(1300, 750)
		self.sizeHint()
		self.setWindowTitle('Armada Startup')

		# GUI -----------------------------------------------
		self.login_flow_widget = login_flow.LoginFlow(self)
		self.creation_flow_widget = creation_flow_widget.CreationFlowWidget(self)

		# Main stacked widget that switches between first login and creation flows
		self.sw_main = QtWidgets.QStackedWidget()

		self.sw_main.addWidget(self.login_flow_widget)
		self.sw_main.addWidget(self.creation_flow_widget)

		# Layout -----------------------------------------------
		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addWidget(self.sw_main)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.login_flow_widget.loginPressed.connect(self.creation_flow_widget.username_widget.update)

	def _on_login(self):
		self.sw_main.setCurrentIndex(1)

