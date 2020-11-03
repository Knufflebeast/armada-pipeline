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


class CreateUsername(QtWidgets.QWidget):
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
		super(CreateUsername, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent
		self.armada_root_path = definitions.ROOT_PATH

		self.setWindowIcon(resource.icon('armada_logo', 'png'))
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.setFixedWidth(600)
		self.sizeHint()

		# self.lbl_step_username = QtWidgets.QPushButton("ABOUT YOU")
		# self.lbl_step_username.setStyleSheet("""
		# 	QPushButton{
		# 		background: transparent;
		# 		height: 30px;
		# 		font: 10px;
		# 		font-weight: normal;
		# 		color: #a6a6a6
		# 	}
		# 	QPushButton:hover{
		# 		background: transparent;
		# 		color: #FFFFFF
		# 	}
		# 	QPushButton:hover:pressed{
		# 		background: transparent;
		# 	}
		# 	QPushButton:pressed{
		# 		background:  transparent;
		# 	}
		# """)
		#
		# pix_arrow_right_1_ = QtGui.QPixmap(resource.color_svg('arrow_right', 1024, '#a6a6a6', return_type=resource.PIXMAP))
		# self.pix_arrow_right_1 = pix_arrow_right_1_.scaled(20, 20)
		# self.lbl_arrow_right_1 = QtWidgets.QLabel()
		# self.lbl_arrow_right_1.setPixmap(self.pix_arrow_right_1)
		#
		# self.lbl_step_workspace = QtWidgets.QPushButton("CREATE WORKSPACE")
		# self.lbl_step_workspace.setStyleSheet("font: 10px; font-weight: normal;")
		# self.lbl_step_workspace.setStyleSheet("""
		# 	QPushButton{
		# 		background: transparent;
		# 		height: 30px;
		# 		font: 10px;
		# 		font-weight: bold;
		# 		color: #FFFFFF
		# 	}
		# 	QPushButton:hover{
		# 		background: transparent;
		# 		color: #FFFFFF
		# 	}
		# 	QPushButton:hover:pressed{
		# 		background: transparent;
		# 	}
		# 	QPushButton:pressed{
		# 		background:  transparent;
		# 	}
		# """)
		#
		#
		# pix_arrow_right_2_ = QtGui.QPixmap(resource.color_svg('arrow_right', 1024, '#a6a6a6', return_type=resource.PIXMAP))
		# self.pix_arrow_right_2 = pix_arrow_right_2_.scaled(20, 20)
		# self.lbl_arrow_right_2 = QtWidgets.QLabel()
		# self.lbl_arrow_right_2.setPixmap(self.pix_arrow_right_2)
		#
		# self.lbl_step_project = QtWidgets.QPushButton("ADD YOUR FIRST PROJECT")
		# self.lbl_step_project.setStyleSheet("font: 10px;font-weight: normal;")
		# self.lbl_step_project.setStyleSheet("""
		# 	QPushButton{
		# 		background: transparent;
		# 		height: 30px;
		# 		font: 10px;
		# 		font-weight: normal;
		# 		color: #a6a6a6
		# 	}
		# 	QPushButton:hover{
		# 		background: transparent;
		# 		color: #FFFFFF
		# 	}
		# 	QPushButton:hover:pressed{
		# 		background: transparent;
		# 	}
		# 	QPushButton:pressed{
		# 		background:  transparent;
		# 	}
		# """)

		# self.lbl_title = QtWidgets.QLabel('Create Your Workspace')
		# self.lbl_title.setStyleSheet("font: 20pt 'Roboto-Thin';")
		#

		self.tb_workspace_example = QtWidgets.QTextBrowser()
		self.tb_workspace_example.setHtml("""
			<p style="font-size:30px;">Welcome aboard to Armada Pipeline!</p>"""
		)
		# self.tb_workspace_example.setFixedHeight(int(self.tb_workspace_example.document().size().height()))

		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')

		self.tb_workspace_description = QtWidgets.QTextBrowser()

		self.tb_workspace_description.setHtml("""
			<p style="font: 12px;font-weight: normal;">You're signed in as {0}.</p>""".format(data['CURRENT_ACCOUNT'])
		)
		# self.tb_workspace_description.setMaximumHeight(self.tb_workspace_example.document().size().height())

		self.lbl_workspace = QtWidgets.QLabel("What's your full name?")
		self.le_username = QtWidgets.QLineEdit()
		self.le_username.setMinimumHeight(40)

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
			}'''
		)
		self.btn_next.setFixedSize(100, 40)

		# self.lbl_disclaimer = QtWidgets.QTextBrowser()
		# self.lbl_disclaimer.setReadOnly(True)
		# self.lbl_disclaimer.setText('Armada Pipeline does not store passwords or account data at this time. Your acocunt is stored locally and only used to add another degree of flexibility project')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		# Layout --------------------------------------------
		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_workspace_example)

		description_layout.addWidget(self.tb_workspace_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(30, 20, 30, 20)
		description_layout.setSpacing(0)

		input_layout = QtWidgets.QVBoxLayout()
		input_layout.addWidget(self.lbl_workspace)
		input_layout.addWidget(self.le_username)
		input_layout.setAlignment(QtCore.Qt.AlignTop)
		input_layout.setContentsMargins(30, 20, 30, 20)
		input_layout.setSpacing(10)

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
		self.main_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.btn_next.clicked.connect(self._on_next)

	def update(self):
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		self.tb_workspace_description.setHtml("""
					<p style="font: 12px;font-weight: normal;">You're signed in as {0}.</p>""".format(
			data['CURRENT_ACCOUNT']))

	def _on_next(self):
		username = self.le_username.text()
		data = resource.json_read(definitions.USER_PATH, filename='armada_settings')
		data['CURRENT_USERNAME'] = username
		print(username)
		resource.json_save(definitions.USER_PATH, filename='armada_settings', data=data)

		self.nextPressed.emit()