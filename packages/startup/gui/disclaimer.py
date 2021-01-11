"""
Startup main window
"""
import os
import platform
from distutils.dir_util import copy_tree

from Qt import QtCore, QtWidgets, QtGui

from core import definitions
from core import resource
from core import renaming_convention

import utilsa

logging = utilsa.Logger('armada')


class Disclaimer(QtWidgets.QWidget):
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
		super(Disclaimer, self).__init__(parent)

		self.logger = logging.getLogger('menu.' + self.__class__.__name__)
		self.logger.info('Workplace creation starting...')
		self.setObjectName('launcher_{0}'.format(self.__class__.__name__))

		self.parent = parent

		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.installEventFilter(self)
		self.setStyleSheet(resource.style_sheet('setup'))
		self.sizeHint()

		self.armada_root_path = definitions.ROOT_PATH

		# GUI -----------------------------------------------
		self.btn_back = QtWidgets.QPushButton()
		self.btn_back.setIcon(resource.color_svg('arrow_left', 128, '#9E9E9E'))
		self.btn_back.setIconSize(QtCore.QSize(30, 30))
		self.btn_back.setFixedHeight(30)
		self.btn_back.setStyleSheet(resource.style_sheet('push_button_w_icon'))

		self.tb_description = QtWidgets.QTextBrowser()
		self.tb_description.setMinimumHeight(550)
		redText = "<span style=\" font-size:13pt; color:#ff0000;\" >"
		redText += "<p><b>[WARNING! NOT READY FOR PRODUCTION!]</b></p>"
		self.tb_description.insertHtml(redText)
		self.tb_description.setStyleSheet("""
			background-color: transparent;
			font: 12px;
			font-weight: normal
		""")
		self.tb_description.insertHtml("""<pre></pre>
		<p>Please read everything below before beginning the setup process:</p>
		<p>Armada is still in active development. There is no guarantee of stability or compatiblity with future 
		releases of Armada. This beta is for testing purposes only</p>
		<p>Armada does not keep records of usernames, passwords, files, etc anywhere other than your local documents drive. 
		Your files and accounts are solely protected by you and/or your cloud drives provider.</p>
		<p>In the future I'd like to use google/gumroad accounts for license verification and extra little goodies but that's a ways away.</p>
		<p><b>-Thank you!-</b></p>
		<p>I appreciate you taking the time to help with testing! The pace of future development will depend on my availability but also
		community interest, feedback during beta, and volunteers... AKA you! Please join the 
		<a style=\"color: #FF64DEDB;\" href=\"https://discord.gg/Gt2ux4D\"><b>Discord server</b></a> (A link to the server is also 
		provided in-app via 
		the discord button) and share within your networks.</p>
		<p><b>-Beta Guidelines-</b></p>
		<li>- All feedback should be given in the beta-feedback channel in the 
		<a style=\"color: #FF64DEDB;\" href=\"https://discord.gg/Gt2ux4D\"><b>Discord server</b></a>.</li>
		<li>- You'll be notified of new releases via Gumroad emails and/or Discord so make sure to keep an eye out in either channel.
		Pre relases will be available on the <a style=\"color: #FF64DEDB;\" href=\"https://github.com/mikebourbeauart/armada-pipeline\"><b>GitHub repo</b></a>. 
		You can find a link to repo via the GitHub button.
		<li>- You'll be testing Armada Launcher and Marina File Manager. Atlantis Asset Manager will have its own alpha 
		soon.</li>
		<li>- Windows 10 is currently the only supported platform. MacOS is also supported but not hooked up at this time due to the amount of time it took for me to 
		maintain both versions. Linux is not currently supported only because I don't have a linux machine to test with. It should work with a few tweaks.
		<li>- No new features will be added during the beta. I'll be focusing on making Armada's current 
		features more stable.</li>
		<li>- I repeat, do not use this in production! The foundation is still being laid so things will break as I 
		refine systems based on your feedback.</li>
		""".format(self.armada_root_path))
		# self.tb_description.setWordWrap(True)

		self.cb_agree_to_terms = QtWidgets.QCheckBox("By checking this box, you acknowledge that you have read the above "
													 "\ndisclaimer and agree to the terms laid out within it. "
													 "\nYou cannot use Armada without agreeing.")

		self.btn_next = QtWidgets.QPushButton('Next')
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
		# self.lbl_disclaimer.setText('')
		# self.lbl_disclaimer.setMinimumSize(100, 50)

		# Layout --------------------------------------------
		description_layout = QtWidgets.QVBoxLayout()
		description_layout.addWidget(self.tb_description)
		description_layout.setAlignment(QtCore.Qt.AlignTop)
		description_layout.setContentsMargins(0, 0, 0, 0)
		description_layout.setSpacing(30)

		btn_layout = QtWidgets.QVBoxLayout()
		btn_layout.addWidget(self.btn_next)
		btn_layout.setAlignment(QtCore.Qt.AlignTop)
		btn_layout.setContentsMargins(0, 0, 0, 0)
		btn_layout.setSpacing(0)

		contents_layout = QtWidgets.QVBoxLayout()
		contents_layout.addLayout(description_layout)
		contents_layout.addWidget(self.cb_agree_to_terms)
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
		self.main_layout.addLayout(contents_layout)
		# self.main_layout.addLayout(disclaimer_layout)
		# self.main_layout.setAlignment(QtCore.Qt.AlignBottom)
		self.main_layout.setContentsMargins(20, 20, 60, 20)
		self.main_layout.setSpacing(10)

		self.setLayout(self.main_layout)

		# Connections -----------------------------------
		self.cb_agree_to_terms.stateChanged.connect(self._on_checked)

	def _on_checked(self):
		if self.cb_agree_to_terms.isChecked():
			self.btn_next.setDisabled(False)
		else:
			self.btn_next.setDisabled(True)


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
			super(Disclaimer, self).keyPressEvent(event)