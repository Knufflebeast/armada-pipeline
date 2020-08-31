"""
Module for prep asset popup.
"""
import os
import sys
import platform
from distutils.dir_util import copy_tree

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource
from core import path_maker

import utilsa

logging = utilsa.Logger('armada')

FULL, MOUNT, STRUCTURE = (1, 2, 3)


class ArmadaInstaller(QtWidgets.QDialog):
	"""Downloads armada-pipeline release from GitHub repo
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"
	newCreated = QtCore.Signal()

	def __init__(self, setup=FULL):
		"""
		Args:
			setup: What part of setup is the user entering into?
		"""
		super(ArmadaInstaller, self).__init__()

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Setup starting...')

		self.setup = setup
		self.setObjectName('armada_Installer')
		self.armada_root_path = definitions.ROOT_PATH

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.setFixedSize(900, 600)
		self.sizeHint()

		# GUI ------------------------------
		pixmap_banner = resource.pixmap(name='banner_setup', scope='help')
		self.lbl_banner = QtWidgets.QLabel()
		self.lbl_banner.setPixmap(pixmap_banner)

		self.cb_style_sheet = """
		QCheckBox::indicator:checked:disabled {{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #29dff7;
		}}
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
		}}
		""".format(self.armada_root_path)

		self.cb_s0_install = QtWidgets.QCheckBox('Install Armada Pipeline')
		self.cb_s0_install.setStyleSheet(self.cb_style_sheet)
		self.cb_s0_install.setEnabled(False)

		self.cb_s1_complete = QtWidgets.QCheckBox('Complete installation')
		self.cb_s1_complete.setStyleSheet(self.cb_style_sheet)
		self.cb_s1_complete.setEnabled(False)

		self.lbl_title = QtWidgets.QLabel("Mount Point Setup")
		# self.lbl_title.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
		# self.lbl_title.setMinimumHeight(400)
		self.lbl_title.setStyleSheet("""
		QLabel {
			font-size: 30px;
			font-family: Roboto;
			color: #FFFFFF;
		}""")

		# Mount point setup
		self.lbl_install_dir = QtWidgets.QLabel()
		self.lbl_install_dir.setText("Install to:")
		self.lbl_install_dir.setStyleSheet(resource.style_sheet('setup'))

		self.le_install_dir = QtWidgets.QLineEdit()
		# Path defaults
		if platform.system().lower() in ['windows']:
			install_dir = "C:/Program Files"
		elif platform.system().lower() in ['darwin']:
			install_dir = "/Applications"
		else:
			raise
		self.le_install_dir.setText(install_dir)
		self.le_install_dir.setTextMargins(10, 5, 10, 5)

		self.lbl_full_path = QtWidgets.QLabel()
		self.lbl_full_path.setText("Full path:")
		self.lbl_full_path.setStyleSheet(resource.style_sheet('setup'))
		self.le_full_path = QtWidgets.QLabel()
		serifFont = QtGui.QFont("Roboto", 10, QtGui.QFont.StyleItalic)
		self.le_full_path.setFont(serifFont)
		self.le_full_path.setText('{0}/Armada Pipeline'.format(self.le_install_dir.text()))
		self.le_full_path.setWordWrap(True)

		self.btn_mount_browse = QtWidgets.QPushButton("Browse")
		self.btn_mount_browse.setMinimumWidth(100)

		self.btn_left = QtWidgets.QPushButton("Cancel")
		self.btn_left.setStyleSheet("""
			QPushButton{			
				background-color:#636363;
				height: 30px;			
				}
				QPushButton:hover{
					background: #369593;
				}
				QPushButton:hover:pressed{
					background: #2e7a78;
				}
				QPushButton:pressed{
					background:  #2a615f;
				}
				QPushButton:disabled{
					background: #3b3b3b;
				}
			""")
		self.btn_right = QtWidgets.QPushButton("Install")
		self.btn_right.setStyleSheet("""
			QPushButton{			
				background-color:#636363;
				height: 30px;
				border-style: solid;
				border-width: 3px;
				border-color: #369593;

				}
				QPushButton:hover{
					background: #369593;
				}
				QPushButton:hover:pressed{
					background: #2e7a78;
					border-style: solid;
					border-width: 3px;
					border-color: #2e7a78;
				}
				QPushButton:pressed{
					background:  #2a615f;
				}
				QPushButton:disabled{
					background: #3b3b3b;
					border-style: solid;
					border-width: 0px;
					border-color: #4abdbb;
					border-radius: 0px;
				}
		""")
		self.btn_right.setDisabled(True)

		self.lbl_description = QtWidgets.QTextBrowser()
		self.lbl_description.setReadOnly(True)
		self.lbl_description.setOpenExternalLinks(True)
		self.lbl_description.setStyleSheet("""
		QTextEdit {
			background-color: #262626;
			color: #FFFFFF;
			font: 14px "Roboto-thin";
			border: 0px;
		}""")

		# State machine ------------------
		self.state_machine = QtCore.QStateMachine()
		self.s0_install = QtCore.QState()
		self.s1_complete = QtCore.QState()

		# Entry point for setup
		# Transitions
		self.trans_s0_s1 = self.s0_install.addTransition(self.btn_right.clicked, self.s1_complete)
		self.trans_s1_s0 = self.s1_complete.addTransition(self.btn_left.clicked, self.s0_install)

		# Add states
		self.state_machine.addState(self.s0_install)
		self.state_machine.addState(self.s1_complete)
		self.state_machine.setInitialState(self.s0_install)

		# Connections
		self.s0_install.entered.connect(self.on_s0_install_entered)
		self.s1_complete.entered.connect(self.on_install_pressed)
		self.s1_complete.entered.connect(self.on_s1_complete_entered)

		# Properties
		self.s0_install.assignProperty(self.btn_left, "text", "Cancel")
		self.s0_install.assignProperty(self.btn_right, "text", "Install")
		self.s1_complete.assignProperty(self.btn_left, "text", "Back")
		self.s1_complete.assignProperty(self.btn_right, "text", "Set Sail!")

		self.state_machine.start()

		# Layout ---------------------------
		self.steps_layout = QtWidgets.QVBoxLayout()
		self.steps_layout.addWidget(self.lbl_banner, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
		self.steps_layout.addWidget(self.cb_s0_install, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.addWidget(self.cb_s1_complete, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.setContentsMargins(30, 30, 30, 100)

		self.title_layout = QtWidgets.QHBoxLayout()
		self.title_layout.addWidget(self.lbl_title)
		# self.title_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
		self.title_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.title_layout.setContentsMargins(20, 20, 20, 20)

		# Mount point layout
		self.install_dir_layout = QtWidgets.QHBoxLayout()
		self.install_dir_layout.addWidget(self.lbl_install_dir, 0, QtCore.Qt.AlignLeft)
		self.install_dir_layout.addWidget(self.le_install_dir, 1)
		self.install_dir_layout.addWidget(self.btn_mount_browse, 0, QtCore.Qt.AlignRight)
		self.install_dir_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.full_path_layout = QtWidgets.QHBoxLayout()
		self.full_path_layout.addWidget(self.lbl_full_path, 0, QtCore.Qt.AlignLeft)
		self.full_path_layout.addWidget(self.le_full_path, 1)

		# Structure layout
		self.description_layout = QtWidgets.QHBoxLayout()
		self.description_layout.addWidget(self.lbl_description, 1, QtCore.Qt.AlignTop)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_left)
		self.button_layout.addWidget(self.btn_right)
		self.button_layout.setAlignment(QtCore.Qt.AlignBottom)
		self.button_layout.setContentsMargins(20, 20, 20, 20)

		self.info_layout = QtWidgets.QVBoxLayout()
		self.info_layout.addLayout(self.description_layout)
		self.info_layout.addLayout(self.install_dir_layout)
		self.info_layout.addLayout(self.full_path_layout)
		self.info_layout.setContentsMargins(30, 30, 30, 30)

		self.user_layout = QtWidgets.QVBoxLayout()
		self.user_layout.addLayout(self.title_layout)
		self.user_layout.addLayout(self.info_layout)
		self.user_layout.addLayout(self.button_layout, QtCore.Qt.AlignBottom)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(self.steps_layout)
		self.main_layout.addLayout(self.user_layout)

		self.setLayout(self.main_layout)

		# Connections
		self.btn_mount_browse.clicked.connect(self.on_browse_pressed)
		self.le_install_dir.textChanged.connect(self.on_le_mount_text_changed)

		self.esc_pressed.connect(self.on_cancel_pressed)

		# Wait for user input
		self.exec_()

	def on_le_mount_text_changed(self, text):
		"""
		Remove banned characters from name string
		"""
		self.le_full_path.setText('{0}/Armada Pipeline'.format(self.le_install_dir.text()))

		# Check if path exists
		if os.path.exists(text):
			self.btn_right.setEnabled(True)

		else:
			self.btn_right.setEnabled(False)

	def on_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Choose install directory")
		self.le_install_dir.setText(path)

	def on_s0_install_entered(self):
		# Steps
		self.cb_s0_style = """
		QCheckBox::indicator:checked:disabled {{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #29dff7;
		}}
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
		}}
		""".format(self.armada_root_path)
		self.cb_s0_install.setChecked(True)
		self.cb_s0_install.setStyleSheet(self.cb_s0_style)
		self.cb_s1_complete.setChecked(False)
		self.cb_s1_complete.setStyleSheet(self.cb_s0_style)

		self.lbl_description.clear()
		self.lbl_description.setHtml("""<p>Choose an installation directory.</p>
		""")

		self.lbl_description.setFixedHeight(int(self.lbl_description.document().size().height()))

		self.lbl_title.setText('Install Armada Pipeline')
		self.install_dir_layout.setContentsMargins(0, 0, 0, 0)

		# Show mount gui
		self.lbl_install_dir.show()
		self.le_install_dir.show()
		self.btn_mount_browse.show()
		self.lbl_full_path.show()
		self.le_full_path.show()

		try:
			self.btn_right.clicked.disconnect(self.on_accept_pressed)
			self.enter_pressed.disconnect(self.on_accept_pressed)
		except:
			pass

		# S0
		self.enter_pressed.connect(self.on_accept_pressed)
		self.btn_left.clicked.connect(self.on_cancel_pressed)
		# Global gui update
		self.btn_right.setDisabled(False)

		self.adjustSize()

	def on_s1_complete_entered(self):
		# Steps
		self.cb_s1_style = """
		QCheckBox::indicator:checked:disabled {{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #3693f6;
		}}
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
		}}
		""".format(self.armada_root_path)
		self.cb_s0_style = """
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #29dff7;
		}}
		""".format(self.armada_root_path)
		self.cb_s0_install.setChecked(False)
		self.cb_s0_install.setStyleSheet(self.cb_s0_style)
		self.cb_s1_complete.setChecked(True)
		self.cb_s1_complete.setStyleSheet(self.cb_s1_style)

		# Show mount gui
		self.lbl_install_dir.hide()
		self.le_install_dir.hide()
		self.btn_mount_browse.hide()
		self.lbl_full_path.hide()
		self.le_full_path.hide()

		self.lbl_description.clear()
		self.lbl_description.setFixedHeight(int(self.lbl_description.document().size().toSize().width()))

		self.lbl_description.setHtml("""
		<p>You're ready to shove off!<br>
		</br>
		<br></br>
		<br></br>
		Armada Pipeline was successfully installed in:</p>
		<blockquote><i>{0}</i></blockquote>""".format(self.le_full_path.text()))

		self.install_dir_layout.setContentsMargins(0, 0, 0, 0)
		self.lbl_title.setText('Bon Voyage!')

		# Global gui update
		self.btn_left.clicked.disconnect(self.on_cancel_pressed)
		self.btn_left.setDisabled(True)
		self.btn_left.hide()
		self.btn_right.clicked.connect(self.on_accept_pressed)
		self.enter_pressed.connect(self.on_accept_pressed)

		self.adjustSize()

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		import sys
		sys.exit()

	def on_install_pressed(self):
		print('installing')
		# Make path
		path_maker.make_dirs(self.le_full_path.text())

		release_url = 'https://github.com/Armada-Pipeline/armada-pipeline/releases/download/v2020.08.30b/armada_pipeline_2020.8.28b_macos.zip'
		save_path = '{0}/armada_pipeline.zip'.format(self.le_full_path.text())

		##Python 3
		import urllib.request
		print("download start!")
		filename, headers = urllib.request.urlretrieve(release_url, filename=save_path)
		print("download complete!")
		print("download file location: ", filename)
		print("download headers: ", headers)

		import zipfile, urllib.request, shutil
		#
		# with urllib.request.urlopen(release_url) as response, open(save_path, 'wb') as out_file:
		# 	shutil.copyfileobj(response, out_file)
		# 	# with zipfile.ZipFile(save_path) as zf:
		# 	# 	zf.extractall()
		#
		params = headers.get('Content-Disposition', '')
		print(params)
		filename = params.split(';')[1]
		print(filename)
		with zipfile.ZipFile(save_path, 'r') as zip_ref:
			zip_ref.extractall('{0}/{1}'.format(self.le_full_path.text(), filename))


		# import requests
		# import zipfile
		# import io
		#
		# r = requests.get(release_url)
		# z = zipfile.ZipFile(io.BytesIO(r.content))
		# z.extractall(save_path)


	def on_accept_pressed(self):
		"""

		"""

		install_dir = self.le_install_dir.text()
		print(install_dir)
		self.close()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(ArmadaInstaller, self).keyPressEvent(event)


if __name__ == "__main__":
	# Run Armada launcher
	app = QtWidgets.QApplication(sys.argv)
	# QtGui.QFontDatabase.addApplicationFont('resources/fonts/Roboto/Roboto-Thin.ttf')

	ArmadaInstaller()

	# sys.exit(app.exec_())
