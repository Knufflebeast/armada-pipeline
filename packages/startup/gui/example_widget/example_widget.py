"""
Startup main window
"""
from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource

import utilsa

logging = utilsa.Logger('armada')


class ExampleWidget(QtWidgets.QWidget):
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
		super(ExampleWidget, self).__init__(parent)

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
		self.user_avatar = label_image.LabelImage('mike.bourbeau', size=30)  # name='mike_photo')
		self.user_avatar.setObjectName('CurrentUser')

		self.lbl_workspace = QtWidgets.QLabel('Knufflebeast')
		self.lbl_workspace.setStyleSheet("font:12pt;font-weight:bold;")

		self.lbl_user_name = QtWidgets.QLabel('Mike Bourbeau')
		self.lbl_user_name.setStyleSheet("font:10pt 'Roboto-Thin'; color: #949494;")

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
		input_layout.addWidget(self.lbl_username)
		input_layout.addSpacing(10)
		input_layout.addWidget(self.le_username)
		input_layout.addWidget(self.hline_username)
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

		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(btn_back_layout)
		self.main_layout.addLayout(contents_layout)
		self.main_layout.setContentsMargins(60, 20, 60, 20)
		self.main_layout.setSpacing(10)

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