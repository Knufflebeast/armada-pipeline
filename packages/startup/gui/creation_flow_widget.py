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
from startup.gui import create_structure_workflow
from startup.gui import create_structure_selection
from startup.gui import create_software

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
	setup_completed = QtCore.Signal()

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

		self.username_widget = create_username.CreateUsername(self)
		self.workspace_widget = create_workspace.CreateWorkspace(self)
		self.project_widget = create_project.CreateProject(self)
		self.structure_workflow_widget = create_structure_workflow.CreateStructureWorkflow(self)
		self.structure_selection_widget = create_structure_selection.CreateStructureSelection(self)
		self.software_widget = create_software.CreateSoftware(self)

		# Creation stacked widget. Guides first setup flow
		self.sw_creation_flows = QtWidgets.QStackedWidget(self)

		self.sw_creation_flows.addWidget(self.username_widget)
		self.sw_creation_flows.addWidget(self.workspace_widget)
		self.sw_creation_flows.addWidget(self.project_widget)
		self.sw_creation_flows.addWidget(self.structure_workflow_widget)
		self.sw_creation_flows.addWidget(self.structure_selection_widget)
		self.sw_creation_flows.addWidget(self.software_widget)

		self.example_widget = QtWidgets.QWidget()
		self.example_widget.setMaximumWidth(400)
		self.example_widget.setObjectName("armada_ExampleWidget")

		# State machine ------------------
		self.state_machine = QtCore.QStateMachine()
		self.s0_username = QtCore.QState()
		self.s1_workspace = QtCore.QState()
		self.s2_project = QtCore.QState()
		self.s3_structure_workflow = QtCore.QState()
		self.s4_structure_sel = QtCore.QState()
		self.s5_software = QtCore.QState()
		self.s6_complete = QtCore.QState()

		# Transitions
		# User next
		self.trans_s0_s1 = self.s0_username.addTransition(self.username_widget.btn_next.clicked, self.s1_workspace)
		# Workspace next
		self.trans_s1_s2 = self.s1_workspace.addTransition(self.workspace_widget.btn_next.clicked, self.s2_project)
		# Project next
		self.trans_s2_s3 = self.s2_project.addTransition(self.project_widget.btn_next.clicked, self.s3_structure_workflow)
		# Structure workflow next
		self.trans_s3_s4 = self.s3_structure_workflow.addTransition(self.structure_workflow_widget.btn_next.clicked, self.s4_structure_sel)
		# Structure sel next
		self.trans_s4_s5 = self.s4_structure_sel.addTransition(self.structure_selection_widget.btn_next.clicked, self.s5_software)
		# Complete
		self.trans_s5_s6 = self.s5_software.addTransition(self.software_widget.btn_next.clicked, self.s6_complete)
		# Software back
		self.trans_s5_s4 = self.s5_software.addTransition(self.software_widget.btn_back.clicked, self.s4_structure_sel)
		# Structure sel back
		self.trans_s4_s3 = self.s4_structure_sel.addTransition(self.structure_selection_widget.btn_back.clicked, self.s3_structure_workflow)
		# Structure workflow back
		self.trans_s3_s2 = self.s3_structure_workflow.addTransition(self.structure_workflow_widget.btn_back.clicked, self.s2_project)
		# Project back
		self.trans_s3_s2 = self.s2_project.addTransition(self.project_widget.btn_back.clicked, self.s1_workspace)
		# Workspace back
		self.trans_s2_s1 = self.s1_workspace.addTransition(self.workspace_widget.btn_back.clicked, self.s0_username)

		# Add states
		self.state_machine.addState(self.s0_username)
		self.state_machine.addState(self.s1_workspace)
		self.state_machine.addState(self.s2_project)
		self.state_machine.addState(self.s3_structure_workflow)
		self.state_machine.addState(self.s4_structure_sel)
		self.state_machine.addState(self.s5_software)
		self.state_machine.addState(self.s6_complete)
		self.state_machine.setInitialState(self.s0_username)

		# Connections
		self.s0_username.entered.connect(self.on_s0_username_entered)
		self.s1_workspace.entered.connect(self.on_s1_workspace_entered)
		self.s2_project.entered.connect(self.on_s2_project_entered)
		self.s3_structure_workflow.entered.connect(self.on_s3_structure_workflow_entered)
		self.s4_structure_sel.entered.connect(self.on_s4_structure_sel_entered)
		self.s5_software.entered.connect(self.on_s5_software_entered)
		self.s6_complete.entered.connect(self.on_s6_complete)

		self.state_machine.start()

		# Properties
		# self.s0_welcome.assignProperty(self.btn_left, "text", "Cancel")
		# self.s0_welcome.assignProperty(self.btn_right, "text", "Begin Setup!")
		# self.s1_mount_setup.assignProperty(self.btn_left, "text", "Back")
		# self.s1_mount_setup.assignProperty(self.btn_right, "text", "Next")
		# self.s2_structure_workflow.assignProperty(self.btn_left, "text", "Back")
		# self.s2_structure_workflow.assignProperty(self.btn_right, "text", "Next")
		# self.s3_structure_sel.assignProperty(self.btn_left, "text", "Back")
		# self.s3_structure_sel.assignProperty(self.btn_right, "text", "Next")
		# self.s4_software.assignProperty(self.btn_right, "text", "Back")
		# self.s4_software.assignProperty(self.btn_right, "text", "Finish!")

		# Layout --------------------------------------------
		frame_layout = QtWidgets.QHBoxLayout()
		frame_layout.addWidget(self.frame_left)
		frame_layout.setAlignment(QtCore.Qt.AlignLeft)
		frame_layout.setContentsMargins(0, 0, 0, 0)
		frame_layout.setSpacing(0)

		header_layout = QtWidgets.QHBoxLayout()
		header_layout.addWidget(self.logo_image, 0, QtCore.Qt.AlignTop)
		header_layout.addWidget(self.breadcrumb_steps, 1, QtCore.Qt.AlignLeft)
		header_layout.setContentsMargins(10, 10, 10, 10)
		header_layout.setSpacing(5)

		input_layout = QtWidgets.QVBoxLayout(self.frame_left)
		input_layout.addLayout(header_layout)
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
		# self.breadcrumb_steps.breadcrumbIndexChanged.connect(self._on_breadcrumb_changed)

		# self.login_widget.loginPressed.connect(self.create_username_widget.update)
		# self.username_widget.nextPressed.connect(self._on_user_next_pressed)
		# self.workspace_widget.nextPressed.connect(self._on_workspace_next_pressed)
		# self.create_project_widget.complete.connect(self.create_project_widget.launch_armada)

	# def _on_breadcrumb_changed(self, index):
	# 	# self.breadcrumb_steps.setCurrentIndex(index)
	# 	self.sw_creation_flows.setCurrentIndex(index)
	# 	print(self.breadcrumb_steps.currentIndex())
	# 	print(index)
	#
	# def _on_user_next_pressed(self):
	# 	self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.WORKSPACE)
	# 	self.workspace_widget.update()
	#
	# def _on_workspace_next_pressed(self):
	# 	self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.PROJECT)
	# 	self.project_widget.update()

	def on_s0_username_entered(self):
		print('entered user')
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.ABOUT_YOU)
		self.sw_creation_flows.setCurrentIndex(0)

	def on_s1_workspace_entered(self):
		print('entered workspace')
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.WORKSPACE)
		self.sw_creation_flows.setCurrentIndex(1)
		self.workspace_widget.update_gui(self.username_widget.le_username.text())

	def on_s2_project_entered(self):
		print('entered project')
		self.breadcrumb_steps.setCurrentIndex(breadcrumb_startup_steps.PROJECT)
		self.sw_creation_flows.setCurrentIndex(2)

	def on_s3_structure_workflow_entered(self):
		print('entered structure workflow')
		self.sw_creation_flows.setCurrentIndex(3)

	def on_s4_structure_sel_entered(self):
		print('entered structure selection')
		self.sw_creation_flows.setCurrentIndex(4)

	def on_s5_software_entered(self):
		print('entered software')
		self.sw_creation_flows.setCurrentIndex(5)

	def on_s6_complete(self):
		print('write data signal on completion')
		self.setup_completed.emit()
