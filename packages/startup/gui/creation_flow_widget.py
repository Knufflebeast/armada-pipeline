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
from startup.gui import breadcrumb_startup_steps
from startup.gui import create_workspace
from startup.gui import create_username
from startup.gui import create_project

import utilsa

logging = utilsa.Logger('armada')

USER, WORKSPACE = ('user', 'workspace')


class CreationFlowWidget(QtWidgets.QWidget):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	newCreated = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(CreationFlowWidget, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Setup starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.armada_root_path = definitions.ROOT_PATH

		self.setWindowIcon(resource.icon('armada_logo', 'png'))
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		# self.resize(1300, 750)
		self.sizeHint()


		# GUI -----------------------------------------------
		self.frame_left = QtWidgets.QFrame()
		self.frame_left.setStyleSheet("QFrame{background: #202020;}")
		self.frame_left.setMaximumWidth(600)

		# Logo
		self.logo_image = QtWidgets.QLabel(self)
		self.logo_image.setObjectName('MainLogo')
		self.logo_image.resize(self.logo_image.sizeHint())
		self.logo_image_pixmap = resource.pixmap('banner').scaled(
			200, 25, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self.logo_image.setPixmap(self.logo_image_pixmap)
		self.logo_image.setAlignment(QtCore.Qt.AlignVCenter)

		# Breadcrumb stuff
		self.breadcrumb_steps = breadcrumb_startup_steps.BreadcrumbStartupSteps(self)
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.ABOUT_YOU)
		# self.breadcrumb_steps.setTabEnabled(breadcrumb_startup_steps.WORKSPACE, False)
		# self.breadcrumb_steps.setTabEnabled(breadcrumb_startup_steps.PROJECT, False)

		self.create_username_widget = create_username.CreateUsername(self)
		self.create_workspace_widget = create_workspace.CreateWorkspace(self)
		self.create_project_widget = create_project.CreateProject(self)

		# Creation stacked widget. Guides first setup flow
		self.sw_creation_flows = QtWidgets.QStackedWidget(self)

		self.sw_creation_flows.addWidget(self.create_username_widget)
		self.sw_creation_flows.addWidget(self.create_workspace_widget)
		self.sw_creation_flows.addWidget(self.create_project_widget)

		self.example_widget = QtWidgets.QWidget()
		self.example_widget.setMaximumWidth(400)

		# Layout --------------------------------------------
		frame_layout = QtWidgets.QHBoxLayout()
		frame_layout.addWidget(self.frame_left)
		frame_layout.setAlignment(QtCore.Qt.AlignLeft)
		frame_layout.setContentsMargins(0, 0, 0, 0)
		frame_layout.setSpacing(0)

		logo_layout = QtWidgets.QHBoxLayout()
		logo_layout.addWidget(self.logo_image, 0, QtCore.Qt.AlignTop)
		logo_layout.addWidget(self.breadcrumb_steps, 1, QtCore.Qt.AlignLeft)
		logo_layout.setContentsMargins(10, 10, 10, 10)
		logo_layout.setSpacing(5)

		input_layout = QtWidgets.QVBoxLayout(self.frame_left)
		input_layout.addLayout(logo_layout)
		input_layout.addWidget(self.sw_creation_flows)
		# input_layout.addStretch()
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(0, 0, 0, 0)
		input_layout.setSpacing(0)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(frame_layout)
		self.main_layout.addWidget(self.example_widget)
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.breadcrumb_steps.breadcrumbIndexChanged.connect(self._on_breadcrumb_changed)

		# self.login_widget.loginPressed.connect(self.create_username_widget.update)
		self.create_username_widget.nextPressed.connect(self._on_user_next_pressed)
		self.create_workspace_widget.nextPressed.connect(self._on_workspace_next_pressed)
		# self.create_project_widget.complete.connect(self.create_project_widget.launch_armada)

	def _on_breadcrumb_changed(self, index):
		index_map = {
			0: 0,
			2: 1,
			4: 2
		}
		# self.breadcrumb_steps.setCurrentIndex(index)
		self.sw_creation_flows.setCurrentIndex(index_map[index])
		print(self.breadcrumb_steps.currentIndex())
		print(index_map[index])

	def _on_user_next_pressed(self):
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.WORKSPACE)
		self.create_workspace_widget.update()

	def _on_workspace_next_pressed(self):
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.PROJECT)
		self.create_project_widget.update()
		# self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.WORKSPACE)
