﻿"""
Startup main window
"""
from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource

import utilsa

logging = utilsa.Logger('armada')


class CreateStructureWorkflow(QtWidgets.QWidget):
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
		super(CreateStructureWorkflow, self).__init__(parent)

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
			<p style="font-size:30px;font-weight: normal;">How do you want to organize your work?</p>"""
		)
		self.tb_welcome.setWordWrap(True)

		self.tb_description = QtWidgets.QLabel()
		self.tb_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal"""
		)
		self.tb_description.setText("""
			<p>Armada utilizes a <b>structure</b> system to enforce project-wide folder/file location and naming conventions.  
			<p>These rules automatically determine what files and folders you can make and where they can be placed - so 
			you can focus on what you do best: ART!</p>"""
		)
		self.tb_description.setWordWrap(True)

		# Input
		self.lbl_username = QtWidgets.QLabel("What's your full name?")

		self.le_username = QtWidgets.QLineEdit()
		self.le_username.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9- ]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_username.setValidator(validator)

		self.hline_username = QtWidgets.QFrame()
		self.hline_username.setFixedHeight(1)
		self.hline_username.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_username.setStyleSheet("background-color: #636363;")

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
		self.btn_next.setEnabled(False)

		# self.lbl_disclaimer = QtWidgets.QTextBrowser()
		# self.lbl_disclaimer.setReadOnly(True)
		# self.lbl_disclaimer.setText('Armada Pipeline does not store passwords or account data at this time. Your acocunt is stored locally and only used to add another degree of flexibility project')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		# Layout --------------------------------------------
		btn_back_layout = QtWidgets.QVBoxLayout()
		btn_back_layout.addWidget(self.btn_back)
		btn_back_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_back_layout.setContentsMargins(30, 20, 0, 20)
		btn_back_layout.setSpacing(0)

		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_welcome)
		description_layout.addWidget(self.tb_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(30, 20, 30, 20)
		description_layout.setSpacing(30)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_username)
		input_layout.addSpacing(10)
		input_layout.addWidget(self.le_username)
		input_layout.addWidget(self.hline_username)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(30, 20, 30, 20)
		input_layout.setSpacing(0)

		btn_layout = QtWidgets.QVBoxLayout()
		btn_layout.addWidget(self.btn_next)
		btn_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_layout.setContentsMargins(30, 20, 30, 20)
		btn_layout.setSpacing(0)

		contents_layout = QtWidgets.QVBoxLayout()
		contents_layout.addLayout(description_layout)
		contents_layout.addLayout(input_layout)
		contents_layout.addLayout(btn_layout)
		contents_layout.addStretch()
		contents_layout.setAlignment(QtCore.Qt.AlignTop)
		contents_layout.setContentsMargins(0, 0, 0, 0)
		contents_layout.setSpacing(0)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(btn_back_layout)
		self.main_layout.addLayout(contents_layout)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.btn_next.clicked.connect(self._on_next)
		self.le_username.textChanged.connect(self.check_le_state)

	def check_le_state(self, *args, **kwargs):
		"""
		Makes sure line edit input is an email address
		"""
		sender = self.sender()
		validator = sender.validator()
		state = validator.validate(sender.text(), 0)[0]
		if state == QtGui.QValidator.Acceptable:
			self.btn_next.setEnabled(True)
		elif state == QtGui.QValidator.Intermediate:
			self.btn_next.setEnabled(False)
		else:
			self.btn_next.setEnabled(False)

	def update(self):
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		print('getting update data user')
		print(data['CURRENT_ACCOUNT'])
		self.tb_description.setText("""
					<p style="font: 12px;font-weight: normal; color: #CFCFCF;">You're signed in as {0}.</p>""".format(
			data['CURRENT_ACCOUNT']))

	def _on_next(self):
		username = self.le_username.text()
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		data['CURRENT_USERNAME'] = username
		print(username)
		resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)

		self.nextPressed.emit()