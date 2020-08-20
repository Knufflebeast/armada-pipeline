""".. _main_window:

launcher.gui.main_window
*************************

- Launches applications to work on project files or assets
"""
import webbrowser

from Qt import QtCore, QtWidgets

from core import armada
from packages import launcher

import utilsa

logging = utilsa.Logger('armada')


class MainWindow(QtWidgets.QWidget):
	"""
	Connections:
		:ref:`main_tab_bar.currentChanged <main_tab_bar>` --> :ref:`main_stacked_widget.setCurrentIndex <main_stacked_widget>`
	"""
	
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building main window...')

		self.setObjectName('armada_MainWindow')
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.resize(1700, 800)
		# self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setStyleSheet(armada.resource.style_sheet('main_window'))

		# GUI -----------------------------------
		# Window Title Bar
		self.setWindowIcon(armada.resource.icon('armada_logo', 'png'))
		self.setWindowTitle('Armada Launcher')

		# Logo
		self.logo_image = QtWidgets.QLabel(self)
		self.logo_image.setObjectName('MainLogo')
		self.logo_image.resize(self.logo_image.sizeHint())
		# self.logo_image_pixmap = resource.svg('banner', 128, 'pixmap')
		# self.logo_image_pixmap = resource.pixmap('banner_left').scaled(
		self.logo_image_pixmap = armada.resource.pixmap('banner').scaled(
			230, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self.logo_image.setPixmap(self.logo_image_pixmap)
		self.logo_image.setAlignment(QtCore.Qt.AlignTop)

		# Tab bar main
		self.tbar_main_context = launcher.main_tab_bar.MainTabBar(self)
		self.tbar_main_context.setObjectName('MainTabBar')

		# Github repo
		self.btn_github = QtWidgets.QPushButton(armada.resource.color_svg('github', 128, '#9E9E9E'), "GitHub")
		self.btn_github.setIconSize(QtCore.QSize(20, 20))
		self.btn_github.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_github.setMinimumSize(80, 30)

		# Discord repo
		self.btn_discord = QtWidgets.QPushButton(armada.resource.color_svg('discord', 128, '#9E9E9E'), "Discord")
		self.btn_discord.setIconSize(QtCore.QSize(20, 20))
		self.btn_discord.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_discord.setMinimumSize(80, 30)

		# Patreon repo
		self.btn_patreon = QtWidgets.QPushButton(armada.resource.color_svg('patreon', 128, '#9E9E9E'), "Patreon")
		self.btn_patreon.setIconSize(QtCore.QSize(20, 20))
		self.btn_patreon.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))
		self.btn_patreon.setMinimumSize(80, 30)

		# Search bar
		self.le_search_bar = launcher.search_line_edit.SearchLineEdit(self)
		self.le_search_bar.setObjectName('MainSearchBar')
		self.le_search_bar.setFixedWidth(250)
		self.le_search_bar.setFixedHeight(30)

		# Avatar
		self.user_avatar = launcher.label_image.LabelImage('mike.bourbeau', size=30)#, name='mike_photo')
		self.user_avatar.setObjectName('CurrentUser')

		# Separation line
		self.lineB = QtWidgets.QFrame()
		self.lineB.setFixedHeight(1)
		self.lineB.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.lineB.setStyleSheet("background-color: #636363;")

		# Stacked widget
		self.sw_main = launcher.main_stacked_widget.MainStackedWidget(self)

		# Layout -----------------------------
		logo_layout = QtWidgets.QVBoxLayout()
		logo_layout.addWidget(self.logo_image)
		logo_layout.setAlignment(QtCore.Qt.AlignTop)

		tabbar_layout = QtWidgets.QVBoxLayout()
		tabbar_layout.addWidget(self.tbar_main_context)
		tabbar_layout.setAlignment(QtCore.Qt.AlignBottom)

		link_layout = QtWidgets.QHBoxLayout()
		link_layout.addWidget(self.btn_discord)
		link_layout.addSpacing(7)
		link_layout.addWidget(self.btn_github)
		link_layout.addSpacing(7)
		link_layout.addWidget(self.btn_patreon)
		link_layout.setAlignment(QtCore.Qt.AlignTop)

		search_layout = QtWidgets.QVBoxLayout()
		search_layout.addWidget(self.le_search_bar)
		search_layout.setAlignment(QtCore.Qt.AlignRight)
		search_layout.setAlignment(QtCore.Qt.AlignTop)

		avatar_layout = QtWidgets.QVBoxLayout()
		avatar_layout.addWidget(self.user_avatar)
		avatar_layout.setAlignment(QtCore.Qt.AlignTop)

		header_items_layout = QtWidgets.QHBoxLayout()
		header_items_layout.addLayout(logo_layout)
		header_items_layout.addSpacing(144)
		header_items_layout.addLayout(tabbar_layout)
		header_items_layout.addStretch()
		header_items_layout.addLayout(link_layout)
		header_items_layout.addSpacing(7)
		header_items_layout.addLayout(search_layout)
		header_items_layout.addSpacing(7)
		header_items_layout.addLayout(avatar_layout)

		self.header_layout = QtWidgets.QVBoxLayout()
		self.header_layout.addLayout(header_items_layout)
		self.header_layout.addWidget(self.lineB)
		# self.header_layout.setContentsMargins(7, 0, 7, 0)
		self.header_layout.setSpacing(0)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.header_layout)
		self.main_layout.addWidget(self.sw_main)
		self.main_layout.setContentsMargins(8, 8, 8, 8)

		self.setLayout(self.main_layout)

		# Connections -------------------------------------------
		# Change stacked widget's visible widget
		self.tbar_main_context.currentChanged.connect(self.sw_main.setCurrentIndex)
		self.btn_github.clicked.connect(self.open_github)
		self.btn_discord.clicked.connect(self.open_discord)
		self.btn_patreon.clicked.connect(self.open_patreon)

	def open_github(self):
		"""Open Armada Pipeline's github page
		"""
		webbrowser.open('https://github.com/mikebourbeauart/armada-pipeline')

	def open_discord(self):
		"""Open Armada Pipeline's discord server
		"""
		webbrowser.open('https://discord.com/invite/Gt2ux4D')

	def open_patreon(self):
		"""Open Armada Pipeline's patreon page
		"""
		webbrowser.open('https://www.patreon.com/armadapipeline')