"""
Startup main window
"""
import os
import platform
from distutils.dir_util import copy_tree
import uuid

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource
from core import path_maker

import utilsa

logging = utilsa.Logger('armada')

USER, WORKSPACE = ('user', 'workspace')


class LoginFlow(QtWidgets.QDialog):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	loginPressed = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(LoginFlow, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Setup starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent

		self.armada_root_path = definitions.ROOT_PATH

		self.setWindowIcon(resource.icon('armada_logo', 'png'))
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.setWindowTitle('Armada Startup')

		# GUI -----------------------------------------------
		self.frame_login = QtWidgets.QFrame()
		self.frame_login.setStyleSheet("QFrame{background: #202020;}")
		self.frame_login.setFixedSize(300, 500)

		# Logo
		self.logo_image = QtWidgets.QLabel(self)
		self.logo_image.setObjectName('MainLogo')
		self.logo_image.resize(self.logo_image.sizeHint())
		self.logo_image_pixmap = resource.pixmap('banner').scaled(
			230, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self.logo_image.setPixmap(self.logo_image_pixmap)
		self.logo_image.setAlignment(QtCore.Qt.AlignCenter)

		self.btn_log_in_google = QtWidgets.QPushButton("Log in with Google")
		self.btn_log_in_google.setIcon(resource.icon('google', 'png'))
		self.btn_log_in_google.setFixedHeight(40)

		self.hline_or1 = QtWidgets.QFrame()
		self.hline_or1.setFixedHeight(1)
		self.hline_or1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_or1.setStyleSheet("background-color: #656565;")

		self.lbl_or = QtWidgets.QLabel("or")
		self.lbl_or.setStyleSheet("color: #656565")

		self.hline_or2 = QtWidgets.QFrame()
		self.hline_or2.setFixedHeight(1)
		self.hline_or2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_or2.setStyleSheet("background-color: #656565;")

		# Input
		self.lbl_email = QtWidgets.QLabel('Email address')

		self.le_email = QtWidgets.QLineEdit()
		self.le_email.setFocus()
		regexp = QtCore.QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_email.setValidator(validator)

		self.hline_email = QtWidgets.QFrame()
		self.hline_email.setFixedHeight(1)
		self.hline_email.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_email.setStyleSheet("background-color: #636363;")

		self.btn_log_in = QtWidgets.QPushButton('Log in')
		self.btn_log_in.setStyleSheet('''
			QPushButton{
				Background:#2e7a78;
				height: 30px;
				font: 12px "Roboto-Thin"
			}
			QPushButton:hover{
				Background: #369593;
			}
			QPushButton:hover:pressed{
				Background: #2a615f;
			}
			QPushButton:pressed{
				Background:  #2a615f;
			}
			QPushButton:disabled{
				Background: #3b3b3b;
			}'''
		)
		self.btn_log_in.setFixedHeight(30)
		self.btn_log_in.setEnabled(False)

		# self.lbl_disclaimer = QtWidgets.QTextBrowser()
		# self.lbl_disclaimer.setReadOnly(True)
		# self.lbl_disclaimer.setText('Armada Pipeline does not store passwords or account data at this time. Your acocunt is stored locally and only used to add another degree of flexibility project')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		self.lbl_made_by = QtWidgets.QLabel('Made with')
		self.lbl_made_by.setAlignment(QtCore.Qt.AlignCenter)

		self.pix_heart_ = QtGui.QPixmap(resource.pixmap('heart'))
		self.pix_heart = self.pix_heart_.scaled(20, 20)
		self.lbl_heart = QtWidgets.QLabel()
		self.lbl_heart.setPixmap(self.pix_heart)

		self.lbl_new_york = QtWidgets.QLabel('in New York City')
		self.lbl_new_york.setAlignment(QtCore.Qt.AlignCenter)

		self.pix_city_ = QtGui.QPixmap(resource.pixmap('statue_of_liberty'))
		self.pix_city = self.pix_city_.scaled(20, 20)
		self.lbl_city = QtWidgets.QLabel()
		self.lbl_city.setPixmap(self.pix_city)

		# Layout -----------------------------
		frame_layout = QtWidgets.QHBoxLayout()
		frame_layout.addWidget(self.frame_login, 0, QtCore.Qt.AlignCenter)
		frame_layout.setAlignment(QtCore.Qt.AlignCenter)
		frame_layout.setContentsMargins(0, 0, 0, 0)
		frame_layout.setSpacing(0)

		logo_layout = QtWidgets.QHBoxLayout()
		logo_layout.addWidget(self.logo_image)
		logo_layout.setAlignment(QtCore.Qt.AlignTop)
		logo_layout.setContentsMargins(0, 40, 0, 40)
		logo_layout.setSpacing(0)

		google_layout = QtWidgets.QHBoxLayout()
		google_layout.addWidget(self.btn_log_in_google)
		google_layout.setAlignment(QtCore.Qt.AlignTop)
		google_layout.setContentsMargins(0, 20, 0, 20)
		google_layout.setSpacing(0)

		or_layout = QtWidgets.QHBoxLayout()
		or_layout.addWidget(self.hline_or1)
		or_layout.addWidget(self.lbl_or)
		or_layout.addWidget(self.hline_or2)
		or_layout.setContentsMargins(0, 20, 0, 20)
		or_layout.setSpacing(10)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_email)
		input_layout.addSpacing(5)
		input_layout.addWidget(self.le_email)
		input_layout.addWidget(self.hline_email)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(0, 20, 0, 20)
		input_layout.setSpacing(0)

		btn_layout = QtWidgets.QVBoxLayout()
		btn_layout.addWidget(self.btn_log_in)
		btn_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_layout.setContentsMargins(0, 20, 0, 20)
		btn_layout.setSpacing(0)

		with_love_layout = QtWidgets.QHBoxLayout()
		with_love_layout.addWidget(self.lbl_made_by)
		with_love_layout.addWidget(self.lbl_heart)
		with_love_layout.addWidget(self.lbl_new_york)
		with_love_layout.addWidget(self.lbl_city)
		with_love_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
		with_love_layout.setContentsMargins(0, 0, 0, 40)
		with_love_layout.setSpacing(5)

		contents_layout = QtWidgets.QVBoxLayout(self.frame_login)
		contents_layout.addLayout(logo_layout)
		contents_layout.addLayout(google_layout)
		contents_layout.addLayout(or_layout)
		contents_layout.addLayout(input_layout)
		contents_layout.addLayout(btn_layout)
		contents_layout.addStretch()
		contents_layout.addLayout(with_love_layout)
		contents_layout.setAlignment(QtCore.Qt.AlignTop)
		contents_layout.setContentsMargins(30, 0, 30, 0)
		contents_layout.setSpacing(0)

		# disclaimer_layout = QtWidgets.QVBoxLayout()
		# disclaimer_layout.addWidget(self.lbl_disclaimer)
		# disclaimer_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
		# disclaimer_layout.setContentsMargins(0, 20, 0, 20)
		# disclaimer_layout.setSpacing(0)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(frame_layout)
		# self.main_layout.addLayout(disclaimer_layout)
		self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.btn_log_in_google.clicked.connect(self._on_google_log_in)
		self.btn_log_in.clicked.connect(self._on_log_in)
		self.le_email.textChanged.connect(self.check_le_state)

	def check_le_state(self, *args, **kwargs):
		"""
		Makes sure line edit input is an email address
		"""
		sender = self.sender()
		validator = sender.validator()
		state = validator.validate(sender.text(), 0)[0]
		if state == QtGui.QValidator.Acceptable:
			self.btn_log_in.setEnabled(True)
		elif state == QtGui.QValidator.Intermediate:
			self.btn_log_in.setEnabled(False)
		else:
			self.btn_log_in.setEnabled(False)

	def _on_google_log_in(self):
		from google_auth_oauthlib.flow import InstalledAppFlow

		flow = InstalledAppFlow.from_client_secrets_file(
			'W:/OneDrive/Knufflebeast/Technology/ArmadaPipeline/Google_API/client_secret.json',
			['openid'])

		cred = flow.run_local_server()
		account_uuid = str(uuid.uuid4())
		# data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		# data['CURRENT_ACCOUNT'] = cred.token
		# print(cred.token)
		# resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)

		os.environ['ARMADA_CURRENT_ACCOUNT'] = cred.token
		os.environ['ARMADA_SETUP_ACCOUNT_UUID'] = account_uuid

		self.parent.sw_main.setCurrentIndex(1)

	def _on_log_in(self):
		account_name = self.le_email.text()
		account_uuid = str(uuid.uuid4())
		os.environ['ARMADA_CURRENT_ACCOUNT'] = account_name
		os.environ['ARMADA_SETUP_ACCOUNT_UUID'] = account_uuid

		self.loginPressed.emit()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			if self.btn_log_in.isEnabled():
				self._on_log_in()
				return True
			else:
				return False
		if event.key() == QtCore.Qt.Key_Escape:
			return False
		else:
			super(LoginFlow, self).keyPressEvent(event)
