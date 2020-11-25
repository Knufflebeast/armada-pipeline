"""
Startup main window
"""
import os
import platform
from distutils.dir_util import copy_tree

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource

import utilsa

logging = utilsa.Logger('armada')


class CreateWorkspace(QtWidgets.QWidget):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	nextPressed = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(CreateWorkspace, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent
		self.armada_root_path = definitions.ROOT_PATH

		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.sizeHint()

		# GUI -----------------------------------------------
		self.btn_back = QtWidgets.QPushButton()
		self.btn_back.setIcon(resource.color_svg('arrow_left', 128, '#9E9E9E'))
		self.btn_back.setIconSize(QtCore.QSize(30, 30))
		self.btn_back.setFixedHeight(30)
		self.btn_back.setStyleSheet(resource.style_sheet('push_button_w_icon'))

		self.tb_welcome = QtWidgets.QLabel()

		self.tb_description = QtWidgets.QLabel()
		self.tb_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal
		""")
		self.tb_description.setText("""
			<p>A <b>workspace</b> is where all of your projects will be stored.
			<p>Name it after the company you work for, a series of projects you're starting, or the type of work you'll be doing.</p>
			<p>You can change the name later, but it's strongly advised that you don't!</p>"""
		)
		self.tb_description.setWordWrap(True)

		# Mount point
		self.lbl_mount_point = QtWidgets.QLabel('Choose an empty directory to mount your workspace to')

		self.le_mount_point = QtWidgets.QLineEdit()
		self.le_mount_point.setPlaceholderText('e.g D:/OneDrive/Work')
		self.le_mount_point.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9_/:]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_mount_point.setValidator(validator)

		self.btn_mount_browse = QtWidgets.QPushButton("Browse")
		self.btn_mount_browse.setMinimumWidth(100)

		self.hline_mount_point = QtWidgets.QFrame()
		self.hline_mount_point.setFixedHeight(1)
		self.hline_mount_point.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_mount_point.setStyleSheet("background-color: #636363;")

		# Workspace name
		self.lbl_workspace = QtWidgets.QLabel('What should we call this workspace?')

		self.le_workspace = QtWidgets.QLineEdit()
		self.le_workspace.setPlaceholderText('e.g. Knufflebeast, Junior Year Projects, Solo Show, Research and Development, etc.')
		self.le_workspace.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9- ]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_workspace.setValidator(validator)

		self.hline_workspace = QtWidgets.QFrame()
		self.hline_workspace.setFixedHeight(1)
		self.hline_workspace.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_workspace.setStyleSheet("background-color: #636363;")

		# # Full path name
		# self.lbl_full_path = QtWidgets.QLabel('Full mount point path')
		#
		# self.lbl_path_example = QtWidgets.QLabel()
		# self.lbl_path_example.setWordWrap(True)
		# self.lbl_path_example.setStyleSheet("""
		# 			background-color: transparent;
		# 			font: 12px;
		# 			font-weight: normal"""
		# 											 )
		# self.hline_full_path = QtWidgets.QFrame()
		# self.hline_full_path.setFixedHeight(1)
		# self.hline_full_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		# self.hline_full_path.setStyleSheet("background-color: #636363;")

		self.btn_next = QtWidgets.QPushButton('Next')
		self.btn_next.setStyleSheet('''
			QPushButton{
				Background:#2e7a78;
				height: 30px;
				font: 12px "Roboto-Thin"
			}
			QPushButton:hover{
				Background: #369593;
			}
			QPushButton:hover:pressed{
				Background: #2e7a78;
			}
			QPushButton:pressed{
				Background:  #2a615f;
			}
			QPushButton:disabled{
				Background: #3b3b3b;
			}'''
		)
		self.btn_next.setFixedSize(100, 40)
		self.btn_next.setEnabled(False)

		# self.lbl_disclaimer = QtWidgets.QTextBrowser()
		# self.lbl_disclaimer.setReadOnly(True)
		# self.lbl_disclaimer.setText('Armada Pipeline does not store passwords or account data at this time. Your acocunt is stored locally and only used to add another degree of flexibility project')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		# Layout --------------------------------------------
		btn_back_layout = QtWidgets.QVBoxLayout()
		btn_back_layout.addWidget(self.btn_back)
		btn_back_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_back_layout.setContentsMargins(0, 0, 0, 0)
		btn_back_layout.setSpacing(0)

		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_welcome)
		description_layout.addWidget(self.tb_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(0, 0, 0, 0)
		description_layout.setSpacing(30)

		mount_layout = QtWidgets.QHBoxLayout()
		mount_layout.addWidget(self.le_mount_point)
		mount_layout.addWidget(self.btn_mount_browse)
		mount_layout.setContentsMargins(0, 0, 0, 0)
		mount_layout.setSpacing(0)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_mount_point)
		input_layout.addSpacing(10)
		input_layout.addLayout(mount_layout)
		input_layout.addWidget(self.hline_mount_point)
		input_layout.addSpacing(20)
		input_layout.addWidget(self.lbl_workspace)
		input_layout.addSpacing(10)
		input_layout.addWidget(self.le_workspace)
		input_layout.addWidget(self.hline_workspace)
		# input_layout.addSpacing(20)
		# input_layout.addWidget(self.lbl_full_path)
		# input_layout.addSpacing(10)
		# input_layout.addWidget(self.lbl_path_example)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(0, 0, 0, 0)
		input_layout.setSpacing(0)

		btn_layout = QtWidgets.QVBoxLayout()
		btn_layout.addWidget(self.btn_next)
		btn_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_layout.setContentsMargins(0, 0, 0, 0)
		btn_layout.setSpacing(0)

		contents_layout = QtWidgets.QVBoxLayout()
		contents_layout.addLayout(description_layout)
		contents_layout.addLayout(input_layout)
		contents_layout.addLayout(btn_layout)
		contents_layout.addStretch()
		contents_layout.setAlignment(QtCore.Qt.AlignTop)
		contents_layout.setContentsMargins(0, 0, 0, 0)
		contents_layout.setSpacing(50)

		# disclaimer_layout = QtWidgets.QVBoxLayout()
		# disclaimer_layout.addWidget(self.lbl_disclaimer)
		# disclaimer_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
		# disclaimer_layout.setContentsMargins(0, 20, 0, 20)
		# disclaimer_layout.setSpacing(0)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(btn_back_layout)
		self.main_layout.addLayout(contents_layout)
		# self.main_layout.addLayout(disclaimer_layout)
		# self.main_layout.setAlignment(QtCore.Qt.AlignBottom)
		self.main_layout.setContentsMargins(20, 20, 60, 20)
		self.main_layout.setSpacing(10)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.le_workspace.textChanged.connect(self.check_le_state)
		self.le_mount_point.textChanged.connect(self.check_le_state)
		self.btn_mount_browse.clicked.connect(self.on_browse_pressed)

	def on_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Choose mount directory")
		self.le_mount_point.setText(path)

	def check_le_state(self, *args, **kwargs):
		"""
		Makes sure line edit input is an email address
		"""
		# sender = self.sender()
		validator_mount = self.le_mount_point.validator()
		state_mount = validator_mount.validate(self.le_mount_point.text(), 0)[0]

		validator_workspace = self.le_workspace.validator()
		state_workspace = validator_workspace.validate(self.le_workspace.text(), 0)[0]

		# Check validator
		if state_workspace == QtGui.QValidator.Acceptable and state_mount == QtGui.QValidator.Acceptable and os.path.exists(self.le_mount_point.text()):
			self.btn_next.setEnabled(True)
		elif state_workspace == QtGui.QValidator.Intermediate and state_mount == QtGui.QValidator.Intermediate:
			self.btn_next.setEnabled(False)
		else:
			self.btn_next.setEnabled(False)

		# Set exmaple text
		# self.lbl_path_example.setText(os.path.join(self.le_mount_point.text(), self.le_workspace.text()).replace('\\', '/'))

	def update_gui(self, username):
		first_name = username.split(' ')[0]
		self.tb_welcome.setText("""
					<p style="font-size:30px;font-weight: normal;">Ahoy, {0}!</p>
					<p style="font-size:30px;font-weight: normal;">Lets set up your first workspace</p>""".format(
			first_name
		))

	# def _on_next(self):
		# Save workspace data
		# data = resource.json_read(definitions.CONFIG_DIR, filename=self.le_workspace.text())
		# data = {
		# 	'env_vars': {
		# 		'ARMADA_MOUNT_PREFIX': self.lbl_full_path.text()
		# 	}
		# }
		# # Set env_var mount prefix to mount path
		# os.environ['ARMADA_MOUNT_PREFIX'] = self.lbl_full_path.text()  # should do this all in one place maybe?
		# resource.json_save(definitions.CONFIG_DIR, filename=self.le_workspace.text(), data=data)

		# data['CURRENT_WORKSPACE'] = self.le_workspace.text()
		# resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)
