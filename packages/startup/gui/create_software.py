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
		self.tb_description.setStyleSheet(""""font: 12px;font-weight: normal; color: #CFCFCF;""")
		self.tb_description.setText("""
			<p style="font: 12px;font-weight: normal; color: #CFCFCF;">Let's make sure we have the right path for each software.</p>"""
		)
		self.tb_description.setWordWrap(True)

		# Input
		# Path defaults
		if platform.system().lower() in ['windows']:
			self.maya_ver = 'Maya2020'
			self.blender_ver = 'Blender Foundation'
			self.houdini_ver = 'Houdini 18.5.'
			maya_path = 'C:/Program Files/Autodesk'
			blender_path = 'C:/Program Files/Blender Foundation'
			houdini_path = 'C:/Program Files/Side Effects Software'
		elif platform.system().lower() in ['darwin']:
			self.maya_ver = 'maya2020'
			self.blender_ver = 'Blender.app'
			maya_path = '/Applications/Autodesk'
			blender_path = '/Applications'
			houdini_path = '/Applications'
		else:
			raise

		self.lbl_houdini_install = QtWidgets.QPushButton(resource.icon('houdini', 'png'), '')
		self.lbl_houdini_install.setText("Houdini install location:")
		self.lbl_houdini_install.setStyleSheet(resource.style_sheet('icon_label'))

		self.le_houdini_path = QtWidgets.QLineEdit()
		self.le_houdini_path.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9_/:]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_houdini_path.setValidator(validator)
		self.le_houdini_path.setText(houdini_path)
		self.le_houdini_path.setStyleSheet("background-color: red;")

		self.hline_houdini_path = QtWidgets.QFrame()
		self.hline_houdini_path.setFixedHeight(1)
		self.hline_houdini_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_houdini_path.setStyleSheet("background-color: #636363;")

		self.btn_houdini_browse = QtWidgets.QPushButton("Browse")
		self.btn_houdini_browse.setMinimumWidth(100)
		self.le_houdini_path.setStyleSheet("background-color: green;")

		self.lbl_houdini_version = QtWidgets.QLabel("Versions found:")
		self.lbl_houdini_version.setStyleSheet("background-color: blue;")

		self.lw_houdini_verisons = QtWidgets.QListWidget()
		# self.lw_houdini_verisons.setViewMode(QtWidgets.QListView.IconMode)
		# self.lw_houdini_verisons.setMaximumHeight(50)
		# self.lw_houdini_verisons.setResizeMode(QtWidgets.QListView.Fixed)
		# self.lw_houdini_verisons.setUniformItemSizes(True)
		self.lw_houdini_verisons.setSizeAdjustPolicy(QtWidgets.QListWidget.AdjustIgnored)
		self.lw_houdini_verisons.setMovement(self.lw_houdini_verisons.Static)
		self.lw_houdini_verisons.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents);
		self.lw_houdini_verisons.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
		self.lw_houdini_verisons.setFlow(QtWidgets.QListView.LeftToRight)
		# self.lw_houdini_verisons.setSpacing(5)
		self.lw_houdini_verisons.setFixedHeight(50)
		self.lw_houdini_verisons.setStyleSheet("""
						QListView{
							show-decoration-selected: 0;
							background: #262626;
							color:rgb(218,218,218) ;
							font:12px "Roboto-Thin";
							border: none;
							height: 40px;
							outline: 0;
							padding-left: 10;
							padding-right: 10;
						}
						""")

		# Add versions
		for item in os.listdir(self.le_houdini_path.text()):
			lw_item = QtWidgets.QListWidgetItem(item)
			# lw_item.setSizeHint(self.lw_houdini_verisons.sizeHint())
			self.lw_houdini_verisons.addItem(lw_item)

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
		# self.btn_next.setEnabled(False)

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

		houdini_le_layout = QtWidgets.QHBoxLayout()
		houdini_le_layout.addWidget(self.le_houdini_path)
		houdini_le_layout.addWidget(self.btn_houdini_browse)
		houdini_le_layout.setContentsMargins(0, 0, 0, 0)
		houdini_le_layout.setSpacing(0)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_houdini_install, 0, QtCore.Qt.AlignLeft)
		# input_layout.addSpacing(10)
		input_layout.addLayout(houdini_le_layout)
		input_layout.addWidget(self.hline_houdini_path)
		input_layout.addWidget(self.lbl_houdini_version)
		# input_layout.addWidget(self.lw_houdini_verisons)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(0, 0, 0, 0)
		input_layout.addStretch()
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

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(btn_back_layout)
		self.main_layout.addLayout(contents_layout)
		self.main_layout.setContentsMargins(20, 20, 60, 20)
		self.main_layout.setSpacing(10)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.btn_next.clicked.connect(self._on_next)
		self.le_houdini_path.textChanged.connect(self.check_le_state)
		self.btn_houdini_browse.clicked.connect(self.on_houdini_browse_pressed)

	def on_houdini_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setDirectory(self.le_houdini_path.text())
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Find and select the folder named: Side Effects Software")
		if path:
			self.le_houdini_path.setText(path)

	def check_le_state(self, *args, **kwargs):
		"""
		Makes sure line edit path exists
		"""
		# sender = self.sender()
		houdini_path_validator = self.le_houdini_path.validator()
		houdini_path_state = houdini_path_validator.validate(self.le_houdini_path.text(), 0)[0]

		# Check validator
		if houdini_path_state == QtGui.QValidator.Acceptable and os.path.exists(self.le_houdini_path.text()):
			self.btn_next.setEnabled(True)
		elif houdini_path_state == QtGui.QValidator.Intermediate:
			self.btn_next.setEnabled(False)
		else:
			self.btn_next.setEnabled(False)

	# def update(self):
	# 	data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
	# 	print('getting update data user')
	# 	print(data['CURRENT_ACCOUNT'])
	# 	self.tb_description.setText("""
	# 				<p style="font: 12px;font-weight: normal; color: #CFCFCF;">You're signed in as {0}.</p>""".format(
	# 		data['CURRENT_ACCOUNT']))

	def _on_next(self):
		username = self.le_username.text()
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		data['CURRENT_USERNAME'] = username
		print(username)
		resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)

		self.nextPressed.emit()