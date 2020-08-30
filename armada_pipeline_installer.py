"""
Module for prep asset popup.
"""
import os
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

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.setFixedSize(1100, 750)
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

		self.cb_s0_install = QtWidgets.QCheckBox('Beta guidelines')
		self.cb_s0_install.setStyleSheet(self.cb_style_sheet)
		self.cb_s0_install.setEnabled(False)

		self.cb_s1_mount_point = QtWidgets.QCheckBox('Mount point setup')
		self.cb_s1_mount_point.setStyleSheet(self.cb_style_sheet)
		self.cb_s1_mount_point.setEnabled(False)

		self.cb_s2_structure_workflow = QtWidgets.QCheckBox('Choose a workflow')
		self.cb_s2_structure_workflow.setEnabled(False)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_style_sheet)

		self.cb_s3_structure_sel = QtWidgets.QCheckBox('Choose a structure')
		self.cb_s3_structure_sel.setEnabled(False)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_style_sheet)

		self.cb_s4_software = QtWidgets.QCheckBox('Software setup')
		self.cb_s4_software.setEnabled(False)
		self.cb_s4_software.setStyleSheet(self.cb_style_sheet)

		self.lbl_title = QtWidgets.QLabel("Mount Point Setup")
		# self.lbl_title.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
		# self.lbl_title.setMinimumHeight(400)
		self.lbl_title.setStyleSheet("""
		QLabel {
			font-size: 30px;
			font-family: Roboto;
			color: #FFFFFF;
		}""")

		self.btn_hint = QtWidgets.QPushButton()
		self.btn_hint.setIcon(resource.color_svg('help', 128, "#777777"))
		self.btn_hint.setStyleSheet(resource.style_sheet('push_button_w_icon'))

		# Mount point setup
		self.lbl_mount_path = QtWidgets.QPushButton(resource.color_svg('folder_pipeline_root', 1024, '#FFFFFF'), '')
		self.lbl_mount_path.setText("Mount point directory:")
		self.lbl_mount_path.setStyleSheet(resource.style_sheet('icon_label'))

		self.le_mount_path = QtWidgets.QLineEdit()
		self.le_mount_path.setText("")

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
		self.btn_right = QtWidgets.QPushButton("Next")
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

		# Helper image
		self.lbl_helper_image = QtWidgets.QLabel()
		self.lbl_helper_image.hide()

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
		self.s1_complete.entered.connect(self.on_s1_complete_entered)

		# Properties
		self.s0_install.assignProperty(self.btn_left, "text", "Cancel")
		self.s0_install.assignProperty(self.btn_right, "text", "Begin Setup!")
		self.s1_complete.assignProperty(self.btn_left, "text", "Back")
		self.s1_complete.assignProperty(self.btn_right, "text", "Finish!")

		self.state_machine.start()

		# Layout ---------------------------
		self.steps_layout = QtWidgets.QVBoxLayout()
		self.steps_layout.addWidget(self.lbl_banner, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
		if setup == FULL:
			self.steps_layout.addWidget(self.cb_s0_install, 0, QtCore.Qt.AlignCenter)
			self.steps_layout.addWidget(self.cb_s1_mount_point, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.addWidget(self.cb_s2_structure_workflow, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.addWidget(self.cb_s3_structure_sel, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.addWidget(self.cb_s4_software, 0, QtCore.Qt.AlignCenter)
		self.steps_layout.setContentsMargins(30, 30, 30, 100)

		self.title_layout = QtWidgets.QHBoxLayout()
		self.title_layout.addWidget(self.lbl_title)
		# self.title_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
		self.title_layout.addWidget(self.btn_hint)
		self.title_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.title_layout.setContentsMargins(20, 20, 20, 20)

		# Mount point layout
		self.mount_layout = QtWidgets.QHBoxLayout()
		self.mount_layout.addWidget(self.lbl_mount_path, 0, QtCore.Qt.AlignLeft)
		self.mount_layout.addWidget(self.le_mount_path, 1)
		self.mount_layout.addWidget(self.btn_mount_browse, 0, QtCore.Qt.AlignRight)
		self.mount_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.maya_layout = QtWidgets.QHBoxLayout()
		self.maya_layout.addWidget(self.lbl_maya_path, 0, QtCore.Qt.AlignLeft)
		self.maya_layout.addWidget(self.le_maya_path, 1)
		self.maya_layout.addWidget(self.btn_maya_browse, 0, QtCore.Qt.AlignRight)
		self.maya_layout.setAlignment(QtCore.Qt.AlignTop)

		self.blender_layout = QtWidgets.QHBoxLayout()
		self.blender_layout.addWidget(self.lbl_blender_path, 0, QtCore.Qt.AlignLeft)
		self.blender_layout.addWidget(self.le_blender_path, 1)
		self.blender_layout.addWidget(self.btn_blender_browse, 0, QtCore.Qt.AlignRight)
		self.blender_layout.setAlignment(QtCore.Qt.AlignLeft)

		# Structure layout
		self.items_layout = QtWidgets.QVBoxLayout()
		self.items_layout.addWidget(self.lbl_items_title, 0, QtCore.Qt.AlignLeft)
		self.items_layout.addWidget(self.lw_items)

		self.description_layout = QtWidgets.QHBoxLayout()
		self.description_layout.addWidget(self.lbl_description, 1, QtCore.Qt.AlignTop)

		self.helper_image_layout = QtWidgets.QHBoxLayout()
		self.helper_image_layout.addWidget(self.lbl_helper_image, 1, QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_left)
		self.button_layout.addWidget(self.btn_right)
		self.button_layout.setAlignment(QtCore.Qt.AlignBottom)
		self.button_layout.setContentsMargins(20, 20, 20, 20)

		self.info_layout = QtWidgets.QVBoxLayout()
		if self.setup == FULL:
			self.info_layout.addLayout(self.mount_layout)
		self.info_layout.addLayout(self.maya_layout)
		self.info_layout.addLayout(self.blender_layout)
		self.info_layout.addLayout(self.items_layout)
		self.info_layout.addLayout(self.description_layout)
		# self.interactive_layout.addStretch()
		self.info_layout.setContentsMargins(30, 30, 30, 30)

		self.interactive_layout = QtWidgets.QHBoxLayout()
		self.interactive_layout.addLayout(self.info_layout)
		self.interactive_layout.addLayout(self.helper_image_layout)

		self.user_layout = QtWidgets.QVBoxLayout()
		self.user_layout.addLayout(self.title_layout)
		self.user_layout.addLayout(self.interactive_layout)
		self.user_layout.addLayout(self.button_layout, QtCore.Qt.AlignBottom)

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(self.steps_layout)
		self.main_layout.addLayout(self.user_layout)

		self.setLayout(self.main_layout)

		# Connections
		self.lw_items.itemClicked.connect(self._lw_sel_changed)
		self.btn_hint.clicked.connect(self._hint_popup)
		self.btn_mount_browse.clicked.connect(self.on_browse_pressed)
		self.btn_maya_browse.clicked.connect(self.on_maya_browse_pressed)
		self.btn_blender_browse.clicked.connect(self.on_blender_browse_pressed)
		self.le_mount_path.textChanged.connect(self.on_le_mount_text_changed)
		self.le_maya_path.textChanged.connect(self.on_le_mount_text_changed)
		self.le_blender_path.textChanged.connect(self.on_le_mount_text_changed)

		self.esc_pressed.connect(self.on_cancel_pressed)

		# Wait for user input
		self.exec_()

	# def on_listview_clicked(self, index):
	# 	if index.isValid():
	# 		self.lw_items.selectionModel.select(index, QtCore.QItemSelectionModel.Toggle | QtCore.QItemSelectionModel.Rows)

	def on_le_mount_text_changed(self, text):
		"""
		Remove banned characters from name string
		"""
		# Check if path exists
		if os.path.exists(text):
			self.btn_right.setEnabled(True)

			shared_path = resource.get(text, '_armadadata', 'shared_data').replace('\\', '/')
			if os.path.exists(shared_path):
				self.setup = MOUNT

				# Remove old transitions
				self.s1_complete.removeTransition(self.trans_s1_s2)
				self.s2_structure_workflow.removeTransition(self.trans_s2_s3)
				self.s3_structure_sel.removeTransition(self.trans_s3_s4)
				self.s4_software.removeTransition(self.trans_s4_s3)
				self.s3_structure_sel.removeTransition(self.trans_s3_s2)
				self.s2_structure_workflow.removeTransition(self.trans_s2_s1)

				# Add new transitions
				self.trans_s1_s4 = self.s1_complete.addTransition(self.btn_right.clicked, self.s4_software)
				self.trans_s4_s1 = self.s4_software.addTransition(self.btn_left.clicked, self.s1_complete)

				# Disconnect
				try:
					self.s2_structure_workflow.entered.disconnect(self.on_s2_structure_workflow_entered)
					self.s3_structure_sel.entered.disconnect(self.on_s3_structure_sel_entered)
				except:
					pass

				self.cb_s2_structure_workflow.hide()
				self.cb_s3_structure_sel.hide()
				redText = "<span style=\" font-size:13pt; color:#d76efe;\" >"
				redText += """<pre>



							</pre><p>Good news! Armada data was found at your mount point. 
											You'll be skipping the structure setup and moving right onto software linking.</p>"""
				self.lbl_description.append(redText)


			else:
				if self.setup == MOUNT:
					# Switch back to full
					self.setup = FULL

					# Remove old transitions
					self.s1_complete.addTransition(self.trans_s1_s2)
					self.s2_structure_workflow.addTransition(self.trans_s2_s3)
					self.s3_structure_sel.addTransition(self.trans_s3_s4)
					self.s4_software.addTransition(self.trans_s4_s3)
					self.s3_structure_sel.addTransition(self.trans_s3_s2)
					self.s2_structure_workflow.addTransition(self.trans_s2_s1)

					# Add new transitions
					self.s1_complete.removeTransition(self.trans_s1_s4)
					self.s4_software.removeTransition(self.trans_s4_s1)

					# Connect
					try:
						self.s2_structure_workflow.entered.connect(self.on_s2_structure_workflow_entered)
						self.s3_structure_sel.entered.connect(self.on_s3_structure_sel_entered)
					except:
						pass

					self.lbl_description.setHtml("""
						<p>The <b>mount point</b> is the root directory in which all of your work will live</p>
						<p><i>- Example mount point:</i> D:/OneDrive/Work </p>
						<p>- You should only mount to an empty directory</p>
						<p>- For cloud collaboration mount to a cloud drive like 
						<a style=\"color: #FF64DEDB;\" href=\"https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage\"><b>OneDrive</b></a>,
						<a style=\"color: #FF64DEDB;\" href=\"https://support.google.com/a/answer/7491144?hl=en\"><b>Google File Stream</b></a>,
						<a style=\"color: #FF64DEDB;\" href=\"https://www.dropbox.com/?_hp=c\"><b>DropBox</b></a>, etc</p>""")

					self.cb_s2_structure_workflow.show()
					self.cb_s3_structure_sel.show()


		else:
			self.btn_right.setEnabled(False)

	def on_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Choose mount directory")
		self.le_mount_path.setText(path)

	def on_maya_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setDirectory(self.le_maya_path.text())
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Parent directory of '{}' folder".format(self.maya_ver))
		if path:
			self.le_maya_path.setText(path)

	def on_blender_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setDirectory(self.le_blender_path.text())
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Parent directory of '{}' folder".format(self.blender_ver))
		if path:
			self.le_blender_path.setText(path)

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
		self.cb_s1_mount_point.setChecked(False)
		self.cb_s1_mount_point.setStyleSheet(self.cb_s0_style)
		self.cb_s2_structure_workflow.setChecked(False)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_s0_style)
		self.cb_s3_structure_sel.setChecked(False)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_s0_style)

		self.lbl_description.clear()
		redText = "<span style=\" font-size:13pt; color:#ff0000;\" >"
		redText += "<p><b>[WARNING! NOT READY FOR PRODUCTION!]</b></p>"
		self.lbl_description.insertHtml(redText)
		self.lbl_description.insertHtml("""<pre></pre>
		<p>Please read everything below before beginning the setup process:</p>
		<p>Armada is still in active development. There is no guarantee of stability or compatiblity with future 
		releases of Armada. This beta is for testing purposes only</p>
		<p><b>-Thank you!-</b></p>
		<p>I appreciate you taking the time to help with testing! The pace of future development will depend on
		community interest and feedback during beta... AKA you! Please join the 
		<a style=\"color: #FF64DEDB;\" href=\"https://discord.gg/Gt2ux4D\"><b>Discord server</b></a> (A link to the server is also 
		provided in-app via 
		the discord button) and share within your networks.</p>
		<p><b>-Beta Guidelines-</b></p>
		<li>- All feedback should be given in the beta-feedback channel in the 
		<a style=\"color: #FF64DEDB;\" href=\"https://discord.gg/Gt2ux4D\"><b>Discord server</b></a>.</li>
		<li>- Keep up to date by checking the 
		<a style=\"color: #FF64DEDB;\" href=\"https://github.com/mikebourbeauart/armada-pipeline\"><b>GitHub repo</b></a> 
		for the latest release (until I figure out how to add in-app updates). You can find a link to repo via the 
		GitHub button.
		<li>- You'll be testing Armada Launcher and Marina File Manager. Atlantis Asset Manager will have its own beta 
		later this year depending on community interest.</li>
		<li>- Windows 10 and MacOS 10+. Linux is not currently supported only because I don't have a linux machine 
		to test with. It should work with a few tweaks.
		<li>- No new features will be added during the beta. I'll be focusing on making Armada's current 
		features more stable.</li>
		<li>- I repeat, do not use this in production! The foundation is still being laid so things will break as I 
		refine systems based on your feedback.</li>
		""".format(self.armada_root_path))
		self.lbl_description.setFixedHeight(int(self.lbl_description.document().size().height()))

		self.lbl_title.setText('Welcome to the Armada Beta!')
		self.mount_layout.setContentsMargins(0, 0, 0, 0)
		self.btn_hint.hide()

		# Hide mount gui
		self.lbl_mount_path.hide()
		self.le_mount_path.hide()
		self.btn_mount_browse.hide()

		# Global gui update
		self.btn_right.setDisabled(False)

		# S0
		self.btn_left.clicked.connect(self.on_cancel_pressed)
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
		self.cb_s1_mount_point.setChecked(True)
		self.cb_s1_mount_point.setStyleSheet(self.cb_s1_style)
		self.cb_s2_structure_workflow.setChecked(False)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_s1_style)
		self.cb_s3_structure_sel.setChecked(False)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_s1_style)
		self.cb_s4_software.setChecked(False)
		self.cb_s4_software.setStyleSheet(self.cb_s1_style)

		self.lbl_description.clear()

		self.lbl_description.setHtml("""
		<p>The <b>mount point</b> is the root directory in which all of your work will live</p>
		<p><i>- Example mount point:</i> D:/OneDrive/Work </p>
		<p>- You should only mount to an empty directory</p>
		<p>- For cloud collaboration mount to a cloud drive like 
		<a style=\"color: #FF64DEDB;\" href=\"https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage\"><b>OneDrive</b></a>,
		<a style=\"color: #FF64DEDB;\" href=\"https://support.google.com/a/answer/7491144?hl=en\"><b>Google File Stream</b></a>,
		<a style=\"color: #FF64DEDB;\" href=\"https://www.dropbox.com/?_hp=c\"><b>DropBox</b></a>, etc</p>""")
		if self.setup == MOUNT:
			redText = "<span style=\" font-size:13pt; color:#d76efe;\" >"
			redText += """<pre>



			</pre><p>Good news! Armada data was found at your mount point. 
							You'll be skipping the structure setup and moving right onto software linking.</p>"""
			self.lbl_description.append(redText)
		self.mount_layout.setContentsMargins(20, 20, 20, 20)
		self.lbl_title.setText('Mount Point Setup')
		self.btn_hint.show()
		self.hint_text = """################ \n
		### Mount Point Setup Help ###
		The Mount Point is the root path for all of your projects.
		\tTo collaborate in the cloud set your Mount Point to a cloud drive location
		\t\t- For example: D/OneDrive/MyStudioProjects"""

		# Show mount gui
		self.lbl_mount_path.show()
		self.le_mount_path.show()
		self.btn_mount_browse.show()

		# Hide structure gui
		self.lbl_items_title.hide()
		self.lw_items.hide()

		# Hide software gui
		self.lbl_maya_path.hide()
		self.le_maya_path.hide()
		self.btn_maya_browse.hide()
		self.maya_layout.setContentsMargins(0, 0, 0, 0)
		self.lbl_blender_path.hide()
		self.le_blender_path.hide()
		self.btn_blender_browse.hide()
		self.blender_layout.setContentsMargins(0, 0, 0, 0)

		# Global gui update
		self.btn_right.setDisabled(True)

		# Check path in le
		if os.path.exists(self.le_mount_path.text()):
			self.btn_right.setEnabled(True)
		else:
			self.btn_right.setEnabled(False)

		# S0
		if self.setup == FULL or self.setup == MOUNT:
			# S1
			try:
				self.btn_left.clicked.disconnect(self.on_cancel_pressed)
			except:
				pass

		try:
			self.btn_right.clicked.disconnect(self.on_accept_pressed)
			self.enter_pressed.disconnect(self.on_accept_pressed)
		except:
			pass

		self.adjustSize()

	def on_s2_structure_workflow_entered(self):
		# Steps
		self.cb_s2_style = """
		QCheckBox::indicator:checked:disabled {{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #927bfb;

		}}
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
		}}
		""".format(self.armada_root_path)
		self.cb_s1_style = """
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);
				background: #3693f6;
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
		self.cb_s1_mount_point.setChecked(False)
		self.cb_s1_mount_point.setStyleSheet(self.cb_s1_style)
		self.cb_s2_structure_workflow.setChecked(True)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_s2_style)
		self.cb_s3_structure_sel.setChecked(False)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_s2_style)

		self.lbl_title.setText('Structure Setup')
		self.hint_text = """################ \n
			### Structure Setup Help:
			A Structure is a user defined object hierarchy template which is used to enforce a project's
			\tfolder structure and conventions. 
			- It defines context and parameters of an object"""
		if self.setup == STRUCTURE:
			self.lbl_description.setText("You've already configured a mount point, but no structure was found. "
										 "Please set one up.")

		# Hide mount gui
		self.lbl_mount_path.hide()
		self.le_mount_path.hide()
		self.btn_mount_browse.hide()
		self.mount_layout.setContentsMargins(0, 0, 0, 0)

		# Show structure gui
		self.lbl_items_title.show()
		self.lw_items.show()

		# Global gui update
		self.btn_right.setDisabled(True)
		self.lbl_items_title.setText('Choose a workflow:')
		self.lbl_items_title.show()
		self.lw_items.clear()

		# Structure workflow options
		builtin_icon = resource.color_svg('folder_folder', 1024, '#F9D085')
		lw_item = QtWidgets.QListWidgetItem(builtin_icon, 'Built-in Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		self.lw_items.addItem(lw_item)

		custom_icon = resource.color_svg('structure_create', 1024, '#7D7D7D')
		lw_item = QtWidgets.QListWidgetItem(custom_icon, 'Custom Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		# lw_item.setFlags(QtCore.Qt.ItemIsSelectable)  # TODO: enable when custom structures workflow is figured out
		self.lw_items.addItem(lw_item)

		try:
			self.btn_right.clicked.disconnect(self.on_accept_pressed)
			self.enter_pressed.disconnect(self.on_accept_pressed)
		except RuntimeError:
			pass

		if self.setup == FULL:
			# S1
			try:
				self.btn_left.clicked.disconnect(self.on_cancel_pressed)
			except:
				pass

		if self.setup == STRUCTURE:
			self.btn_left.clicked.connect(self.on_cancel_pressed)

		self.lbl_helper_image.hide()

	def on_s3_structure_sel_entered(self):
		# Steps
		self.cb_s3_style = """
		QCheckBox::indicator:checked:disabled {{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
			background: #de6cff;
		}}
		QCheckBox::indicator:unchecked:disabled{{
			image: url({0}/resources/icon/checkbox_unchecked.svg);
		}}
		""".format(self.armada_root_path)
		self.cb_s2_style = """
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);
				background: #927bfb;
			}}
			""".format(self.armada_root_path)
		self.cb_s1_style = """
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);

				background: #3693f6;
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
		self.cb_s1_mount_point.setChecked(False)
		self.cb_s1_mount_point.setStyleSheet(self.cb_s1_style)
		self.cb_s2_structure_workflow.setChecked(False)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_s2_style)
		self.cb_s3_structure_sel.setChecked(True)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_s3_style)
		self.cb_s4_software.setChecked(False)
		self.cb_s4_software.setStyleSheet(self.cb_s3_style)

		self.btn_right.setDisabled(True)
		self.lbl_title.setText('Structure Setup')
		self.lbl_items_title.setText('Choose a structure:')
		self.lbl_items_title.show()
		self.btn_hint.show()
		self.lw_items.show()
		self.lw_items.clear()
		self.lbl_description.setText('')

		# Hide software gui
		self.lbl_maya_path.hide()
		self.le_maya_path.hide()
		self.btn_maya_browse.hide()
		self.maya_layout.setContentsMargins(0, 0, 0, 0)

		self.lbl_blender_path.hide()
		self.le_blender_path.hide()
		self.btn_blender_browse.hide()
		self.blender_layout.setContentsMargins(0, 0, 0, 0)

		# Structure workflow options
		builtin_icon = resource.color_svg('folder_game', 1024, '#F9D085')
		lw_item = QtWidgets.QListWidgetItem(builtin_icon, 'Game Dev Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		lw_item.setData(QtCore.Qt.UserRole, 'gaming_short_structure')
		self.lw_items.addItem(lw_item)

		custom_icon = resource.color_svg('folder_film', 1024, '#F9D085')
		lw_item = QtWidgets.QListWidgetItem(custom_icon, 'Film Structure')
		lw_item.setSizeHint(self.lw_items.sizeHint())
		lw_item.setData(QtCore.Qt.UserRole, 'film_short_structure')
		self.lw_items.addItem(lw_item)

		# S2
		try:
			self.btn_right.clicked.disconnect(self.on_accept_pressed)
			self.enter_pressed.disconnect(self.on_accept_pressed)
		except:
			pass

		# S1
		try:
			self.btn_left.clicked.disconnect(self.on_cancel_pressed)
		except:
			pass

	def on_s4_software(self):
		# Steps
		self.cb_s4_style = """
			QCheckBox::indicator:checked:disabled {{
				image: url({0}/resources/icon/checkbox_checked.svg);
			}}
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);
			}}
			""".format(self.armada_root_path)
		self.cb_s3_style = """
			QCheckBox::indicator:unchecked:disabled {{
				image: url({0}/resources/icon/checkbox_unchecked.svg);
				background: #de6cff;
			}}
			""".format(self.armada_root_path)
		self.cb_s2_style = """
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);
				background: #927bfb;
			}}
			""".format(self.armada_root_path)
		self.cb_s1_style = """
			QCheckBox::indicator:unchecked:disabled{{
				image: url({0}/resources/icon/checkbox_unchecked.svg);

				background: #3693f6;
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
		self.cb_s1_mount_point.setChecked(False)
		self.cb_s1_mount_point.setStyleSheet(self.cb_s1_style)
		self.cb_s2_structure_workflow.setChecked(False)
		self.cb_s2_structure_workflow.setStyleSheet(self.cb_s2_style)
		self.cb_s3_structure_sel.setChecked(False)
		self.cb_s3_structure_sel.setStyleSheet(self.cb_s3_style)
		self.cb_s4_software.setChecked(True)
		self.cb_s4_software.setStyleSheet(self.cb_s4_style)

		self.lbl_title.setText('Link Software Packages')
		self.lbl_items_title.hide()
		self.lw_items.hide()
		self.btn_hint.hide()
		self.le_mount_path.hide()
		self.lbl_mount_path.hide()
		self.btn_mount_browse.hide()
		self.mount_layout.setContentsMargins(0, 0, 0, 0)
		self.lbl_helper_image.hide()

		self.lbl_description.setHtml("""
		<p>Armada needs your help linking software to it's launcher settings.</p>
		<p>- Only Maya and Blender are currently supported.</p>
		<p>- If your name is Bill and you're a writer, browse to some random folders. It's important that they exist.""")
		self.btn_right.setDisabled(False)

		# Maya
		self.lbl_maya_path.show()
		self.le_maya_path.show()
		self.btn_maya_browse.show()
		self.maya_layout.setContentsMargins(20, 20, 20, 20)

		# Blender
		self.lbl_blender_path.show()
		self.le_blender_path.show()
		self.btn_blender_browse.show()
		self.blender_layout.setContentsMargins(20, 20, 20, 20)

		# S2
		self.btn_right.clicked.connect(self.on_accept_pressed)
		self.enter_pressed.connect(self.on_accept_pressed)

		try:
			self.btn_left.clicked.disconnect(self.on_cancel_pressed)
		except:
			pass

	def _hint_popup(self):

		print(self.hint_text)

	def _lw_sel_changed(self, index):
		# Structure setup
		if index.data(QtCore.Qt.DisplayRole) == "Built-in Structure":
			self.lbl_description.setHtml("""
			<p>Choose between 2 <b>built-in structures</b>:</p>
			<li>- Game Development</li> 
			<li>- Film Production</li>
			<p><b>[NOTE]</b> Structures cannot be changed at this time without destroying the project. In order to try 
			a different structure close Armada and the delete the contents of your mount directory. 
			Reset instructions will be provided in-app and the documentation as well. Future releases will automate
			this process</p>""")
			self.btn_right.setDisabled(False)

		elif index.data(QtCore.Qt.DisplayRole) == "Custom Structure":
			self.lbl_description.setHtml("""[IN DEVELOPMENT] Create your own <b>custom structure</b>.""")
			self.btn_right.setDisabled(True)

		# Structure selection
		elif index.data(QtCore.Qt.DisplayRole) == "Game Dev Structure":
			self.lbl_description.setHtml("""
			<p>Features an asset library and support for levels</p>""")
			self.btn_right.setDisabled(False)
			image = resource.pixmap('game_structure', scope='help')
			self.lbl_helper_image.setPixmap(image)
			self.lbl_helper_image.show()

		elif index.data(QtCore.Qt.DisplayRole) == "Film Structure":
			self.lbl_description.setHtml("""Features an asset library and support for sequences and shots""")
			self.btn_right.setDisabled(False)
			image = resource.pixmap('film_structure', scope='help')
			self.lbl_helper_image.setPixmap(image)
			self.lbl_helper_image.show()

	# self.lbl_description.setText(self.description_text)
	# def eventFilter(self, source, event):
	# 	"""
	# 	Close window on focus exit of popup
	# 	"""
	# 	if event.type() == QtCore.QEvent.WindowDeactivate:
	# 		self.close()
	# 	# elif event.type() == QtCore.QEvent.Close:
	# 	# 	self.parent.repaint()
	# 	# return true here to bypass default behaviour
	# 	return super(ArmadaSetupPopup, self).eventFilter(source, event)

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		import sys
		sys.exit()

	def on_accept_pressed(self):
		"""

		"""

		if self.setup == FULL or self.setup == STRUCTURE:
			# Make sure there's a structure option selected
			try:
				structure_sel_data = self.lw_items.currentIndex().data(QtCore.Qt.UserRole).lower()
				self.logger.info('Selected structure = {}'.format(structure_sel_data))
			except AttributeError:
				raise AttributeError('No type selected, please select one')

		# Set mount prefix in user config and env var
		if self.setup == FULL or self.setup == MOUNT:
			mount_path = self.le_mount_path.text()
			maya_path = self.le_maya_path.text()
			blender_path = self.le_blender_path.text()

			# Get config data
			config_name = definitions.CONFIG_FILE_NAME
			config_user_data = resource.json_read(resource.get('config_user'), filename=config_name)

			# Set env_var mount prefix to mount path
			config_user_data['env_vars']['ARMADA_MOUNT_PREFIX'] = mount_path
			config_user_data['env_vars']['ARMADA_MAYA_LOCATION'] = maya_path
			config_user_data['env_vars']['ARMADA_BLENDER_LOCATION'] = blender_path
			resource.json_save(resource.get('config_user'), filename=config_name, data=config_user_data)

			# Set mount path for current session
			os.environ['ARMADA_MOUNT_PREFIX'] = mount_path
			os.environ['ARMADA_MAYA_LOCATION'] = maya_path
			os.environ['ARMADA_BLENDER_LOCATION'] = blender_path

		if self.setup == FULL or self.setup == STRUCTURE:
			# Set structure settings data
			shared_settings_path = resource.data_path(data_type='shared')
			structure_settings_data = {"structure_name": structure_sel_data}
			resource.json_save(shared_settings_path, filename='shared_settings', data=structure_settings_data)

			# Make directories in shared location
			structures_data_root_path = resource.data_path('structures', data_type='shared')
			path_maker.make_dirs(structures_data_root_path)

			# Copy default structures to shared location
			shared_settings_data = resource.json_read(resource.data_path(data_type='shared'),
													  filename='shared_settings')
			default_structure_path = resource.get('resources', 'structures', shared_settings_data['structure_name'])
			pipeline_structures_data_path = resource.data_path('structures', shared_settings_data['structure_name'],
															   data_type='shared')
			copy_tree(default_structure_path, pipeline_structures_data_path)

		self.close()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(ArmadaSetupPopup, self).keyPressEvent(event)
