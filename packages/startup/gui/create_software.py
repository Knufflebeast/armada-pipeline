"""
Startup main window
"""
import os
import platform

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource

import utilsa

logging = utilsa.Logger('armada')


class CreateSoftware(QtWidgets.QWidget):
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
		super(CreateSoftware, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent
		self.armada_root_path = definitions.ROOT_PATH

		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.sizeHint()

		# GUI ----------------------------------
		self.btn_back = QtWidgets.QPushButton()
		self.btn_back.setIcon(resource.color_svg('arrow_left', 128, '#9E9E9E'))
		self.btn_back.setIconSize(QtCore.QSize(30, 30))
		self.btn_back.setFixedHeight(30)
		self.btn_back.setStyleSheet(resource.style_sheet('push_button_w_icon'))

		self.tb_welcome = QtWidgets.QLabel()
		self.tb_welcome.setText("""
				<p style="font-size:30px;font-weight: normal;">Almost there!</p>"""
								)
		self.tb_welcome.setWordWrap(True)

		self.tb_description = QtWidgets.QLabel()
		self.tb_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal"""
		)
		self.tb_description.setText("""
			<p>Let's make sure we have the right path for each software.</p>"""
		)
		self.tb_description.setWordWrap(True)

		# Input
		# scroll area
		self.scrollArea = QtWidgets.QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setStyleSheet('background-color: #00000000;')
		self.content = QtWidgets.QWidget()
		self.content.setStyleSheet('background-color: #00000000;')

		self.scrollArea.setWidget(self.content)

		layout = QtWidgets.QVBoxLayout(self.content)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(20)

		supported_software = ['maya', 'houdini', 'blender']

		for item in supported_software:
			software_card = SoftwareCard(self, item)
			layout.addWidget(software_card)

		self.btn_next = QtWidgets.QPushButton('Next')
		self.btn_next.setFixedWidth(100)
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

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.scrollArea)

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
		# self.le_houdini_path.textChanged.connect(self.check_le_state)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			if self.btn_next.isEnabled():
				self.btn_next.clicked.emit()
				return True
			else:
				return False
		if event.key() == QtCore.Qt.Key_Escape:
			return False
		else:
			super(CreateSoftware, self).keyPressEvent(event)


class SoftwareCard(QtWidgets.QWidget):
	def __init__(self, parent=None, software=None):
		"""Cards for software
		"""
		super(SoftwareCard, self).__init__(parent)

		self.setStyleSheet(resource.style_sheet('setup'))

		self.frame_bg = QtWidgets.QFrame()
		self.frame_bg.setStyleSheet('background-color: #303030;')

		self.software = software

		# Path defaults
		if platform.system().lower() in ['windows']:
			if self.software == 'maya':
				self.env_var = 'ARMADA_MAYA_LOCATION'
				self.software_dir = 'Autodesk'
				software_path = 'C:/Program Files/Autodesk'
			elif self.software == 'blender':
				self.env_var = 'ARMADA_BLENDER_LOCATION'
				self.software_dir = 'Blender Foundation'
				software_path = 'C:/Program Files/Blender Foundation'
			elif self.software == 'houdini':
				self.env_var = 'ARMADA_HOUDINI_LOCATION'
				self.software_dir = 'Side Effects Software'
				software_path = 'C:/Program Files/Side Effects Software'
			elif self.software == 'mari':
				self.env_var = 'ARMADA_MARI_LOCATION'
				self.software_dir = 'Mari{version}'
				software_path = 'C:/Program Files'

		elif platform.system().lower() in ['darwin']:
			self.maya_ver = 'maya2020'
			self.blender_ver = 'Blender.app'
			maya_path = '/Applications/Autodesk'
			blender_path = '/Applications'
			houdini_path = '/Applications'
		else:
			raise

		# Blender
		self.icon_software = QtWidgets.QPushButton(resource.icon(self.software, 'png'), '')
		self.icon_software.setStyleSheet(resource.style_sheet('icon_label'))
		self.icon_software.setIconSize(QtCore.QSize(30, 30))

		self.lbl_software_install = QtWidgets.QLabel('{0} install location'.format(self.software.capitalize()))

		self.le_software_path = QtWidgets.QLineEdit()
		self.le_software_path.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9_/:]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_software_path.setValidator(validator)
		self.le_software_path.setText(software_path)
		self.le_software_path.setStyleSheet(resource.style_sheet('setup'))

		self.hline_software_path = QtWidgets.QFrame()
		self.hline_software_path.setFixedHeight(1)
		self.hline_software_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_software_path.setStyleSheet("background-color: #636363;")

		self.btn_software_browse = QtWidgets.QPushButton("Browse")
		self.btn_software_browse.setMinimumWidth(100)
		self.btn_software_browse.setStyleSheet('background-color: red;')
		self.btn_software_browse.setStyleSheet(resource.style_sheet('setup'))

		self.lbl_software_version = QtWidgets.QLabel("Versions found:")
		self.lbl_software_version.setStyleSheet("""
								background-color: transparent;
								font: 12px;
								font-weight: normal"""
											   )

		self.lw_software_verisons = QtWidgets.QListWidget()
		# self.lw_houdini_verisons.setViewMode(QtWidgets.QListView.IconMode)
		self.lw_software_verisons.setMaximumHeight(50)
		# self.lw_houdini_verisons.setResizeMode(QtWidgets.QListView.Fixed)
		# self.lw_houdini_verisons.setUniformItemSizes(True)
		# self.lw_houdini_verisons.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustIgnored)
		self.lw_software_verisons.setMovement(self.lw_software_verisons.Static)
		self.lw_software_verisons.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
		self.lw_software_verisons.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.lw_software_verisons.setFlow(QtWidgets.QListView.LeftToRight)
		# self.lw_software_verisons.setSpacing(5)
		self.lw_software_verisons.setMinimumHeight(30)
		self.lw_software_verisons.setStyleSheet("""
						QListView{
							show-decoration-selected: 0;
							background: #00000000;
							color:rgb(218,218,218) ;
							font:12px "Roboto-Thin";
							border: none;
							outline: none;
							padding-left: 10px;
							padding-right: 10px;
						}
						QListView::item{
							background: #606060;
							color:rgb(218,218,218) ;
							font:12px "Roboto-Thin";
							border-radius: 5px;
							outline: none;
							margin-right: 10px;
							padding-left: 10px;
							padding-right: 10px;
						}"""
											   )

		# Add versions
		self._on_update_versions()

		# Layout --------------------------------------------
		frame_layout = QtWidgets.QHBoxLayout()
		frame_layout.addWidget(self.frame_bg)
		frame_layout.setAlignment(QtCore.Qt.AlignLeft)
		frame_layout.setContentsMargins(0, 0, 0, 0)
		frame_layout.setSpacing(0)

		label_layout = QtWidgets.QHBoxLayout()
		label_layout.addWidget(self.icon_software, 0, QtCore.Qt.AlignLeft)
		label_layout.addWidget(self.lbl_software_install, 0, QtCore.Qt.AlignLeft)
		label_layout.setAlignment(QtCore.Qt.AlignLeft)
		label_layout.setContentsMargins(0, 0, 0, 0)
		label_layout.setSpacing(0)

		input_layout = QtWidgets.QHBoxLayout()
		input_layout.addWidget(self.le_software_path)
		input_layout.addWidget(self.btn_software_browse)
		input_layout.setContentsMargins(0, 0, 0, 0)
		input_layout.setSpacing(0)

		contents = QtWidgets.QVBoxLayout(self.frame_bg)
		contents.addLayout(label_layout)
		contents.addLayout(input_layout)
		contents.addWidget(self.hline_software_path)
		contents.addSpacing(10)
		contents.addWidget(self.lbl_software_version)
		contents.addSpacing(10)
		contents.addWidget(self.lw_software_verisons)
		contents.setContentsMargins(10, 10, 10, 10)
		contents.setSpacing(0)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(frame_layout)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Set initial software env variables
		self.set_env_vars()

		# Connections ---------------------------------------------------------------
		self.le_software_path.textChanged.connect(self.check_le_state)
		self.btn_software_browse.clicked.connect(self.on_software_browse_pressed)

	def _on_update_versions(self):
		# Add versions
		try:
			for item in os.listdir(self.le_software_path.text()):
				if self.software == 'maya':
					if item in ['Maya2020', 'Maya2019']:
						lw_item = QtWidgets.QListWidgetItem(item)
						# lw_item.setSizeHint(self.lw_houdini_verisons.sizeHint())
						self.lw_software_verisons.addItem(lw_item)
				else:
					lw_item = QtWidgets.QListWidgetItem(item)
					# lw_item.setSizeHint(self.lw_houdini_verisons.sizeHint())
					self.lw_software_verisons.addItem(lw_item)
		except FileNotFoundError:
			print("Paths aren't correct yet")

	def set_env_vars(self):
		os.environ[self.env_var] = self.le_software_path.text()

	def on_software_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setDirectory(self.le_software_path.text())
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Find and select the folder named: {0}".format(self.software_dir))
		if path:
			self.le_software_path.setText(path)
			self._on_update_versions()

	def maya_version_resolver(self, folder_name):
		# import re
		# r = re.compile('Maya.{4}')
		# if len(s) == 8:
		# 	if r.match(s):
		# 		return s
		# 		print('matches')
		if folder_name == 'Maya2020':
			return 'Maya2020'
		elif folder_name == 'Maya2019':
			return 'Maya2019'
		else:
			pass

	def check_le_state(self, *args, **kwargs):
		"""
		Make sure path exists on edit and update env vars
		"""
		self.set_env_vars()
		print(os.getenv(self.env_var))
		print('this check stated')
	# 	# sender = self.sender()
	# 	_path_validator = self.le_software_path.validator()
	# 	houdini_path_state = houdini_path_validator.validate(self.le_houdini_path.text(), 0)[0]
	#
	# 	# Check validator
	# 	if houdini_path_state == QtGui.QValidator.Acceptable and os.path.exists(self.le_houdini_path.text()):
	# 		self.btn_next.setEnabled(True)
	# 	elif houdini_path_state == QtGui.QValidator.Intermediate:
	# 		self.btn_next.setEnabled(False)
	# 	else:
	# 		self.btn_next.setEnabled(False)

