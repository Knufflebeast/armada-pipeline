"""
Startup main window
"""
import os
import uuid
import platform
from distutils.dir_util import copy_tree

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource
from core import resolver
from core import path_maker
from core import structure
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

		# # Wait for user input
		# self.exec_()

		# Connections -----------------------------------
		self.login_flow_widget.loginPressed.connect(self._on_login_pressed)
		self.creation_flow_widget.setup_completed.connect(self._on_setup_completed)

	def _on_login_pressed(self):
		self.sw_main.setCurrentIndex(1)
		self.creation_flow_widget.username_widget.update_gui(self.login_flow_widget.le_email.text())

	def _on_setup_completed(self):
		account_name = os.getenv('ARMADA_CURRENT_ACCOUNT')
		account_uuid = os.getenv('ARMADA_SETUP_ACCOUNT_UUID')
		username = self.creation_flow_widget.username_widget.le_username.text()
		workspace_name = self.creation_flow_widget.workspace_widget.le_workspace.text()
		workspace_mount = self.creation_flow_widget.workspace_widget.le_mount_point.text()
		project_name = self.creation_flow_widget.project_widget.le_project.text()
		maya_location = os.getenv('ARMADA_MAYA_LOCATION')
		blender_location = os.getenv('ARMADA_BLENDER_LOCATION')
		houdini_location = os.getenv('ARMADA_HOUDINI_LOCATION')

		# Set env_var mount prefix to mount path
		armada_settings = {
			'accounts': {
				account_name: {  # This should be uuid
					'account_uuid': account_uuid,  # this should be removed
					'account_name': account_name,  # this should hold whatever the google signin value is
					'username': username
				}
			},
			'settings': {
				'ARMADA_CURRENT_ACCOUNT': account_name,
				'ARMADA_CURRENT_WORKSPACE': workspace_name,
				'ARMADA_CURRENT_PROJECT': project_name,
				'ARMADA_MAYA_LOCATION': maya_location,
				'ARMADA_BLENDER_LOCATION': blender_location,
				'ARMADA_HOUDINI_LOCATION': houdini_location,
				'ARMADA_DEBUG': '1'
			},
			'workspaces': {
				workspace_name: {
					'ARMADA_MOUNT_PREFIX': workspace_mount
				}
			}
		}

		# Set env vars for other modules
		os.environ['ARMADA_MOUNT_PREFIX'] = workspace_mount
		os.environ['ARMADA_CURRENT_ACCOUNT'] = account_name
		os.environ['ARMADA_CURRENT_USERNAME'] = username

		# Save settings data
		resource.json_save(definitions.USER_PATH, filename='global_local_settings', data=armada_settings)

		# Write structure data
		try:
			structure_sel_data = self.creation_flow_widget.structure_selection_widget.lw_items.currentIndex().data(QtCore.Qt.UserRole).lower()
			self.logger.info('Selected structure = {}'.format(structure_sel_data))
		except AttributeError:
			raise AttributeError('No type selected, please select one')

		structure_settings_data = {"structure_name": structure_sel_data}
		shared_settings_path = resource.data_path(data_type='shared')
		resource.json_save(shared_settings_path, filename='shared_settings', data=structure_settings_data)

		# Make directories in shared location
		structures_data_root_path = resource.data_path('structures', data_type='shared')
		path_maker.make_dirs(structures_data_root_path)

		# Copy default structures to shared location
		shared_settings_data = resource.json_read(resource.data_path(data_type='shared'), filename='shared_settings')
		default_structure_path = resource.get('resources', 'structures', shared_settings_data['structure_name'])
		pipeline_structures_data_path = resource.data_path('structures', shared_settings_data['structure_name'], data_type='shared')
		copy_tree(default_structure_path, pipeline_structures_data_path)

		# File data creation
		data_root_path = resource.data_path()

		json_data = structure.get_type_data('workspace', type_data=structure.DATA)

		self.logger.debug('Data structure: {}'.format(structure.get_id()))

		json_data['meta_data']['item_name'] = workspace_name
		json_data['meta_data']['item_type'] = 'workspace'
		json_data['meta_data']['uuid'] = '000'
		json_data['meta_data']['hidden'] = 'False'
		json_data['meta_data']['locked'] = 'True'
		json_data['meta_data']['template_id'] = 'workspace'

		path_maker.make_dirs(data_root_path, workspace_name)
		path_maker.make_data_file(data_root_path, workspace_name, json_data=json_data)
		path_maker.make_uuid_file(data_root_path, workspace_name, uuid='000')

		# Project creation
		user_path = os.path.join(workspace_mount, workspace_name, project_name)
		data_path = os.path.join(data_root_path, workspace_name, project_name)
		project_uuid = str(uuid.uuid4())

		json_data = structure.get_type_data('project', type_data=structure.DATA)
		json_data['meta_data']['item_name'] = project_name
		json_data['meta_data']['item_type'] = 'project'
		json_data['meta_data']['uuid'] = project_uuid
		json_data['meta_data']['hidden'] = 'False'
		json_data['meta_data']['locked'] = 'True'
		json_data['meta_data']['template_id'] = 'project'

		# Make project user path
		user_path_abs = user_path
		path_maker.make_dirs(user_path_abs)

		# Make project data path
		data_path_abs = data_path
		path_maker.make_dirs(data_path_abs)

		# Make data file (data path much exist first)
		path_maker.make_data_file(data_path_abs, json_data=json_data)
		# Make uuid file
		path_maker.make_uuid_file(data_path_abs, uuid=project_uuid)

		self.close()

		print('hey we done')
