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


class CreateProject(QtWidgets.QWidget):
	"""Sets up user and/or shared data depending on type of setup process
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	complete = QtCore.Signal()

	def __init__(self, parent=None):
		"""
		Args:
			flow: What part of setup is the user entering into?
		"""
		super(CreateProject, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent
		self.armada_root_path = definitions.ROOT_PATH

		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.sizeHint()

		# GUI -----------------------------------------------
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')

		self.tb_workspace_welcome = QtWidgets.QTextBrowser()
		self.tb_workspace_welcome.setHtml("""
			<p style="font-size:30px;">Let's set up your first project</p>""".format(data['CURRENT_USERNAME'])
		)
		# self.tb_workspace_example.setFixedHeight(int(self.tb_workspace_example.document().size().height()))

		self.tb_workspace_description = QtWidgets.QTextBrowser()
		self.tb_workspace_description.setHtml("""
			<p style="font: 12px;font-weight: normal;">What's something you and your team are currently working on?</p>"""
		)
		# self.tb_workspace_description.setMaximumHeight(self.tb_workspace_example.document().size().height())

		self.lbl_project = QtWidgets.QLabel('Project name')

		self.le_project = QtWidgets.QLineEdit()
		self.le_project.setPlaceholderText('e.g. Short Film, Platformer Game, Run Cycle Project, etc.')
		self.le_project.setMinimumHeight(40)
		regexp = QtCore.QRegExp("^[a-zA-Z0-9- ]+$", QtCore.Qt.CaseInsensitive)
		validator = QtGui.QRegExpValidator(regexp)
		self.le_project.setValidator(validator)

		self.hline_project = QtWidgets.QFrame()
		self.hline_project.setFixedHeight(1)
		self.hline_project.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.hline_project.setStyleSheet("background-color: #636363;")

		self.btn_next = QtWidgets.QPushButton('Next!')
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
		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_workspace_welcome)

		description_layout.addWidget(self.tb_workspace_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(30, 20, 30, 20)
		description_layout.setSpacing(0)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_project)
		input_layout.addSpacing(10)
		input_layout.addWidget(self.le_project)
		input_layout.addWidget(self.hline_project)
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

		# disclaimer_layout = QtWidgets.QVBoxLayout()
		# disclaimer_layout.addWidget(self.lbl_disclaimer)
		# disclaimer_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
		# disclaimer_layout.setContentsMargins(0, 20, 0, 20)
		# disclaimer_layout.setSpacing(0)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(contents_layout)
		# self.main_layout.addLayout(disclaimer_layout)
		# self.main_layout.setAlignment(QtCore.Qt.AlignBottom)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.btn_next.clicked.connect(self._on_next)
		self.le_project.textChanged.connect(self.check_le_state)

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

	def launch_armada(self):
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		self.tb_workspace_welcome.setHtml("""
					<p style="font-size:30px;">Arrrrr, {0}!</p>
					<p style="font-size:30px;">What kind of work will you be doing?</p>""".format(
			data['CURRENT_USERNAME']))

	def _on_next(self):
		project = self.le_project.text()
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		data['CURRENT_PROJECT'] = project
		print(project)
		resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)

		self.complete.emit()