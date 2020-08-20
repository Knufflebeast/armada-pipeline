import os

from Qt import QtCore, QtWidgets, QtGui

from core import armada
import utilsa

logging = utilsa.Logger('armada')


class MountSetupPopup(QtWidgets.QDialog):
	"""Setup for selecting a mount point for the pipeline
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self, parent=None):
		""""""
		super(MountSetupPopup, self).__init__(parent)

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Building folders tree view...')

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.installEventFilter(self)

		self.setStyleSheet(armada.resource.style_sheet('popup_window'))

		# GUI ------------------------------
		name_font = QtGui.QFont("Roboto", 13, QtGui.QFont.DemiBold | QtGui.QFont.NoAntialias)
		self.lbl_title = QtWidgets.QLabel("Mount Point Setup")
		self.lbl_title.setFont(name_font)

		self.btn_hint = QtWidgets.QPushButton()
		self.btn_hint.setIcon(armada.resource.color_svg('help', 128, "#FFFFFF"))
		self.btn_hint.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))

		self.lbl_asset_name = QtWidgets.QPushButton(
			armada.resource.color_svg(
				'folder_pipeline_root',
				1024,
				'#FFFFFF'
			), ''
		)
		self.lbl_asset_name.setText("Pipeline root directory:")
		self.lbl_asset_name.setStyleSheet(armada.resource.style_sheet('icon_label'))

		self.le_mount_path = QtWidgets.QLineEdit()
		self.le_mount_path.setAlignment(QtCore.Qt.AlignLeft)
		self.le_mount_path.setText("Root path")

		self.btn_browse = QtWidgets.QPushButton("Browse")

		self.btn_accept = QtWidgets.QPushButton("Accept")
		self.btn_cancel = QtWidgets.QPushButton("Cancel")

		# Layout ---------------------------
		self.title_layout = QtWidgets.QVBoxLayout()
		# self.name_layout.addWidget(self.icon_asset_name)
		self.title_layout.addWidget(self.lbl_title)

		self.rename_layout = QtWidgets.QHBoxLayout()
		self.rename_layout.addWidget(self.lbl_asset_name)
		self.rename_layout.addWidget(self.le_mount_path)
		self.rename_layout.addWidget(self.btn_browse)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_accept)
		self.button_layout.addWidget(self.btn_cancel)
		self.button_layout.setAlignment(QtCore.Qt.AlignTop)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addLayout(self.rename_layout)
		self.main_layout.addLayout(self.button_layout)
		self.main_layout.addStretch()

		self.setLayout(self.main_layout)

		self.le_mount_path.setFocus()
		# Connections
		self.btn_accept.clicked.connect(self.on_accept_pressed)
		self.btn_cancel.clicked.connect(self.on_cancel_pressed)
		self.le_mount_path.textChanged.connect(self.on_text_changed)
		self.btn_browse.clicked.connect(self.on_browse_pressed)

		self.enter_pressed.connect(self.on_accept_pressed)
		self.esc_pressed.connect(self.on_cancel_pressed)

		self.exec_()

	def on_browse_pressed(self):
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.Directory)
		path = self.file_dialog.getExistingDirectory(self, "Choose mount directory")
		self.le_mount_path.setText(path)
		print(path)


	# def eventFilter(self, source, event):
	# 	"""
	# 	Close window on focus exit of popup
	# 	"""
	# 	if event.type() == QtCore.QEvent.WindowDeactivate:
	# 		self.close()
	# 	# elif event.type() == QtCore.QEvent.Close:
	# 	# 	self.parent.repaint()
	# 	# return true here to bypass default behaviour
	# 	return super(MountSetupPopup, self).eventFilter(source, event)

	def on_accept_pressed(self):
		"""
		Accept button pressed.

		Emits the *data_accepted* signal to the library tree view.

		Signal contains new file name, cleaned up asset type, and software
		"""
		# Get path from line edit
		mount_path = self.le_mount_path.text()
		config_name = os.environ['ARMADA_CONFIG_FILE_NAME']

		# Set mount point path in config
		config_user_data = armada.resource.json_read(armada.resource.get('config_user'), filename=config_name)
		config_user_data['env_vars']['ARMADA_MOUNT_PREFIX'] = mount_path
		armada.resource.json_save(armada.resource.get('config_user'), filename=config_name, data=config_user_data)

		# Set mount path for current session
		os.environ['ARMADA_MOUNT_PREFIX'] = mount_path

		self.close()

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		import sys
		sys.exit()

	def on_text_changed(self, text):
		"""
		Remove banned characters from name string
		"""
		# Format text with convention
		typed_name = self.le_mount_path.text()
		self.le_mount_path.setText(typed_name)

		# Determine new width of popup
		init_width = self.frameGeometry().width()
		lbl_name_width = self.lbl_asset_name.frameGeometry().width()
		le_asset_name_width = self.le_mount_path.frameGeometry().width()
		font_metrics = self.le_mount_path.fontMetrics()
		text_width = font_metrics.boundingRect(text).width()
		new_width = max(lbl_name_width + text_width + 50, init_width)

		if new_width > init_width:
			self.setFixedWidth(new_width)
			diff = int((new_width-init_width)/2)
			self.move(QtCore.QPoint(self.pos().x()-diff, self.pos().y()))

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(MountSetupPopup, self).keyPressEvent(event)

