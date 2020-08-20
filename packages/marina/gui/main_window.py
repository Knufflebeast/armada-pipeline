"""
Builds MMM UI

Main Module
"""

import os
import webbrowser

from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCore

from core import armada
from packages import launcher
from packages import marina

from utilsa.logger import Logger
logging = Logger('marina')

software = os.getenv('_SOFTWARE')

def base_class():
	"""Dynamic base class that passes classes into MainMMM() depending on software it's being called from.
	Need this because i'm using dockable mixin for maya to dock.

	It's a nice setup to have in case other software packages require custom mixins
	"""
	bases = [QtWidgets.QWidget]
	if software == 'maya':
		try:
			from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
			class Mixin(MayaQWidgetDockableMixin, object): pass
			bases.insert(0, Mixin)
		except:
			return type('BuildBase', tuple(bases), {})
	return type('BuildBase', tuple(bases), {})


class MarinaWindow(base_class(), QtWidgets.QWidget):
	"""Build main MMM window."""

	def __init__(self, parent=None):
		super(MarinaWindow, self).__init__(parent)
		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.warning('Building main window...')

		# Context
		self.software = os.getenv('_SOFTWARE')

		self.logger.info('Software : {0}'.format(self.software))

		# self.setMinimumSize(400, 700)
		self.sizeHint()
		self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
		self.setStyleSheet(armada.resource.style_sheet('main_window'))
		self.setObjectName('MMM_Main_Window')
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

		# -----------------------------------------------------------
		# GUI -------------------------------------------------------
		##################################################
		# Model
		self.tree_model = armada.tree_model.TreeModel(self, armada.resource.data_path())

		# Add items to model
		path_list = os.getenv('ARMADA_MAJOR_PARENTS').split()
		library_data = self.tree_model.create_uuid_list_data_dict(armada.resource.data_path(), uuid_list=path_list, depth=10)
		self.tree_model.fill_model(library_data)

		# Index for start selection
		start = self.tree_model.index(0, 0)
		self.major_index = self.tree_model.match(start, QtCore.Qt.UserRole, os.getenv('_MAJOR_UUID'), 1, QtCore.Qt.MatchRecursive)[0]

		# Watcher activated
		self.file_system_watcher = armada.directory_watcher.Watcher()
		self.file_system_watcher.run()

		#####################################################
		# Header
		self.btn_open_browser = QtWidgets.QPushButton(self)
		self.btn_open_browser.setCheckable(True)
		self.btn_open_browser.setFixedSize(30, 30)
		icon_open_library = armada.resource.color_svg('open_library', 128, '#FFFFFF')
		self.btn_open_browser.setIcon(icon_open_library)
		self.btn_open_browser.setIconSize(QtCore.QSize(30, 30))
		self.btn_open_browser.setStyleSheet(armada.resource.style_sheet('push_button_w_icon'))

		self.logo_image = QtWidgets.QLabel(self)
		self.logo_image.setObjectName('MainLogo')
		self.logo_image.resize(self.logo_image.sizeHint())
		self.logo_image_pixmap = armada.resource.pixmap('banner').scaled(
			230, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		self.logo_image.setPixmap(self.logo_image_pixmap)
		self.logo_image.setAlignment(QtCore.Qt.AlignTop)

		##########################################################
		# Details widget
		self.details_widget = launcher.details_widget.DetailsWidget(self)
		self.details_widget.update_widget(self.major_index)

		##########################################################
		# Line
		self.line = QtWidgets.QFrame(self)
		self.line.setFixedHeight(1)
		self.line.setStyleSheet("background-color: #636363;")

		########################################################
		# Minors list view
		minors_proxy_model = launcher.minors_list_proxy_model.MinorsListProxyModel(self)
		minors_proxy_model.setSourceModel(self.tree_model)

		self.lv_minors = launcher.minors_list_view.MinorsListView(self)
		self.lv_minors.setModel(minors_proxy_model)
		self.minor_delegate = launcher.minors_list_item_delegate.MinorsListItemDelegate(self.lv_minors)
		self.lv_minors.setItemDelegate(self.minor_delegate)
		self.lv_minors.update_widget(self.major_index)

		# Save button
		self.btn_minor_save = FloatingButton(self)

		self.browser_popup = marina.browser_popup.BrowserPopup(
			self,
			major_index=self.major_index,
			tree_model=self.tree_model
		)

		# ---------------------------------------
		# Layout --------------------------------
		logo_image_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
		logo_image_layout.addWidget(self.btn_open_browser, QtCore.Qt.AlignLeft)
		logo_image_layout.addWidget(self.logo_image, QtCore.Qt.AlignRight)

		lv_layout = QtWidgets.QHBoxLayout(self.lv_minors)
		lv_layout.addWidget(self.btn_minor_save)
		lv_layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
		lv_layout.setContentsMargins(0, 0, 40, 40)

		sel_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
		sel_layout.addLayout(logo_image_layout)
		sel_layout.addWidget(self.details_widget)
		sel_layout.addWidget(self.line)
		sel_layout.addWidget(self.lv_minors)
		sel_layout.setAlignment(QtCore.Qt.AlignTop)
		sel_layout.setContentsMargins(0, 0, 0, 0)
		sel_layout.setSpacing(0)
		sel_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.addLayout(sel_layout)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.main_layout)

		# -----------------------------------------------
		# Connections -----------------------------------
		# Open browser
		self.btn_open_browser.clicked.connect(self.on_toggle_lib)

		# Saving
		self.btn_minor_save.clicked.connect(self.minor_save)

		# Launching
		self.minor_delegate.softwareLaunched.connect(self.on_launch_minor)
		self.lv_minors.softwareLaunched.connect(self.on_open_minor)
		self.lv_minors.softwareLaunched.connect(self.save_button_toggle)

		# Folder selection changed
		self.browser_popup.folders_view.folderSelectionChanged.connect(self.details_widget.update_widget)
		self.browser_popup.folders_view.folderSelectionChanged.connect(self.lv_minors.update_widget)
		self.browser_popup.folders_view.folderSelectionChanged.connect(self.save_button_toggle)

		# Update model
		self.browser_popup.folders_view.expanded.connect(self.tree_model.lazy_load_update_model)
		self.browser_popup.folders_view.folderSelectionChanged.connect(self.tree_model.lazy_load_update_model)

		# Library selection changed
		self.browser_popup.library_view.librarySelectionChanged.connect(self.details_widget.update_widget)
		self.browser_popup.library_view.librarySelectionChanged.connect(self.lv_minors.update_widget)
		self.browser_popup.library_view.librarySelectionChanged.connect(self.save_button_toggle)

		# Watchers
		self.file_system_watcher.event_handler.sender.fileCreated.connect(self.tree_model.create_row)
		self.file_system_watcher.event_handler.sender.fileModified.connect(self.tree_model.modify_row)
		self.file_system_watcher.event_handler.sender.fileDeleted.connect(self.tree_model.delete_row)
		self.file_system_watcher.event_handler.sender.fileMoved.connect(self.tree_model.move_row)

		try:
			marina.dock_ui.dock_ui(wParent=self)
		except NameError:
			self.logger.info('Running from IDE')

		#self.setFocus

		#cl_user_messages = UserMessages.UserMessages( mInViewMessage=True, fMessageType='welcome' )

	def on_toggle_lib(self):
		if self.browser_popup.isHidden():
			self.browser_popup.show()
		else:
			self.browser_popup.hide()

	def on_launch_minor(self, index_source):
		import importlib
		software = index_source.data(QtCore.Qt.UserRole + 3)
		module = importlib.import_module('armada.app.{0}.{0}_hook'.format(software))
		module.Launch(index_source, module.Launch.EXTERNAL)

	def on_open_minor(self, index_source):

		# File path
		self.file_path_abs = armada.resolver.generate_path(index_source, armada.resolver.USER)

		# Set update MMM env vars
		os.environ['OPEN_FILE_PATH'] = str(self.file_path_abs)
		os.environ['WORKING_DIR'] = str(os.path.join(self.file_path_abs.rpartition('maya')[0], 'maya').replace('\\', '/'))
		os.environ['_MAJOR_UUID'] = str(index_source.parent().data(QtCore.Qt.UserRole))
		self.major_index = index_source.parent()

		manip = marina.file_manip.FileManip(software=self.software)
		manip.open_file(index_source)

		# Hide browser window maybe?
		self.btn_open_browser.setChecked(False)
		self.browser_popup.hide()

	def save_button_toggle(self):
		"""Turn minor save button on only if user has opened major selected
		"""
		# Current folder selection uuid
		index_source_folders = self.browser_popup.folders_view.model().mapToSource(self.browser_popup.folders_view.currentIndex())
		index_source_folders_uuid = index_source_folders.data(QtCore.Qt.UserRole)

		# Current lib selection uuid
		index_source_library = self.browser_popup.library_view.model().mapToSource(self.browser_popup.library_view.currentIndex())
		index_source_library_uuid = index_source_library.data(QtCore.Qt.UserRole)

		major_index_uuid = self.major_index.data(QtCore.Qt.UserRole)

		self.logger.info('Minor UUID for lib {0}: {1}'.format(index_source_library.data(QtCore.Qt.DisplayRole), index_source_library_uuid))
		self.logger.info('Minor UUID for fol {0}: {1}'.format(index_source_folders.data(QtCore.Qt.DisplayRole), index_source_folders_uuid))
		self.logger.info('Current UUID {0}'.format(major_index_uuid))

		if index_source_library_uuid == major_index_uuid or index_source_folders_uuid == major_index_uuid:
			self.btn_minor_save.show()
		else:
			self.btn_minor_save.hide()

	def minor_save(self):
		self.minor_save_popup = marina.minor_save_popup.MinorSavePopup(
			self,
			index_source=self.major_index,
			tree_model=self.tree_model
		)
		self.minor_save_popup.show()

	def closeEvent(self, a0):
		super(MarinaWindow, self).closeEvent(a0)
		self.deleteLater()
		self.browser_popup.close()

	def idea_or_bug_report(self):
		webbrowser.open('https://trello.com/b/AXewDrEu/mb-armada-roadmap')


class FloatingButton(QtWidgets.QPushButton):
	def __init__(self, parent=None):
		super(FloatingButton, self).__init__(parent)

		# self.setLayout(QtWidgets.QHBoxLayout())
		size = 80
		self.setFixedSize(size, size)

		self.setIcon(armada.resource.color_svg('minor_save', 128, '#FFFFFF'))
		self.setStyleSheet("""
			QPushButton{
				background:#2c998e;
				height: 30px;
				font: 12px "Roboto-Thin";
				border-radius: 40
			}
			QPushButton:hover{
				background: #2fa89b;
			}
			# QPushButton:hover:pressed{
			# 	background: #2c998e;
			# }
			QPushButton:pressed{
				background:  #32ada9;
			}
			""")


	def paintEvent(self, qpaintevent):
		option = QtWidgets.QStyleOptionButton()
		option.initFrom(self)

		if self.isDown():
			option.state = QtWidgets.QStyle.State_Sunken
		else:
			pass

		if self.isDefault():
			option.features = option.features or QtWidgets.QStyleOptionButton.DefaultButton
		option.text = self.text()
		option.icon = self.icon()
		option.iconSize = QtCore.QSize(40, 40)

		painter = QtGui.QPainter(self)

		self.style().drawControl(QtWidgets.QStyle.CE_PushButton, option, painter, self)

		# offset = 30
		# win_point = self.parent().rect().bottomRight()
		#
		# self.move(
		# 	win_point.x() - self.rect().width() - offset,
		# 	win_point.y() - self.rect().height() - offset
		# )

