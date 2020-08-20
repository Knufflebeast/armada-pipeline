
from Qt import QtWidgets, QtCore

from core import armada
from packages import launcher

import utilsa

logging = utilsa.Logger('armada')


class BreadcrumbWidget(QtWidgets.QWidget):
	"""Breadcrumb widget container
	"""
	btnCopyClicked = QtCore.Signal(bool)
	btnLaunchClicked = QtCore.Signal(bool)

	def __init__(self, parent=None, index_source=None):
		"""
		Args:
			parent:
			index_source: QtCore.QModelIndex folder tree view
		"""
		super(BreadcrumbWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

		self.setMinimumWidth(400)
		self.setMinimumHeight(30)
		self.setContentsMargins(0, 0, 0, 0)
		# self.setStyleSheet("QWidget{background: white;}")

		self.parent = parent

		# Holds folder icon, crumb buttons, finder button, path button
		self.bar_frame = QtWidgets.QFrame()
		self.bar_frame.setFixedHeight(30)
		self.bar_frame.setMinimumWidth(100)
		self.bar_frame.setStyleSheet("QFrame{background: transparent; border: 0px; border-radius: 15;}")

		self.tabbar_crumbs = launcher.breadcrumb_crumbs_tabbar.BreadcrumbCrumbsTabbar(self, index_source=index_source)
		self.tabbar_crumbs.setStyleSheet(armada.resource.style_sheet('tabbar_breadcrumb'))

		self.le_crumbs = launcher.breadcrumb_line_edit.BreadcrumbLineEdit()
		self.le_crumbs.hide()

		self.btn_switch = QtWidgets.QPushButton()
		self.btn_switch.setMinimumWidth(30)
		self.btn_switch.setCheckable(True)
		self.btn_switch.setIcon(armada.resource.color_svg('edit', 1024, '#FFFFFF'))
		self.btn_switch.setStyleSheet("""QPushButton{
											background-color: rgba(0, 0, 0, 0);
										}
										QPushButton:hover{
											background-color: #909090;
										}""")

		self.btn_copy_path = QtWidgets.QPushButton()
		self.btn_copy_path.setFixedSize(30, 30)
		self.btn_copy_path.setIcon(armada.resource.color_svg('copy', 1024, '#FFFFFF'))
		self.btn_copy_path.setStyleSheet("""QPushButton{
											background-color: rgba(0, 0, 0, 0);
											color: #9E9E9E;
										}
										QPushButton:hover{
											color: #FFFFFF;
											background-color: #5a5a5a;
											border-radius: 15;
										}
										QPushButton:pressed{
											color: #2c998e;
											background-color: #2c998e;
										}
										""")

		self.btn_launch_explorer = QtWidgets.QPushButton()
		self.btn_launch_explorer.setFixedSize(30, 30)
		self.btn_launch_explorer.setIcon(armada.resource.color_svg('launch', 1024, '#FFFFFF'))
		self.btn_launch_explorer.setIconSize(QtCore.QSize(15, 15))
		self.btn_launch_explorer.setStyleSheet("""QPushButton{
											background-color: rgba(0, 0, 0, 0);
											color: #9E9E9E;
										}
										QPushButton:hover{
											color: #FFFFFF;
											background-color: #5a5a5a;
											border-radius: 15;
										}
										QPushButton:pressed{
											color: #2c998e;
											background-color: #2c998e;
										}
										""")

		self.bar_widget_layout = QtWidgets.QHBoxLayout(self.bar_frame)
		self.bar_widget_layout.addWidget(self.tabbar_crumbs, 0, QtCore.Qt.AlignLeft)
		self.bar_widget_layout.addWidget(self.le_crumbs, 0, QtCore.Qt.AlignLeft)
		# self.bar_widget_layout.addWidget(self.btn_switch, 0)  # Removing until it makes sense to put in qlineedit
		self.bar_widget_layout.addWidget(self.btn_copy_path)
		self.bar_widget_layout.addWidget(self.btn_launch_explorer)
		self.bar_widget_layout.setContentsMargins(0, 0, 0, 0)
		self.bar_widget_layout.setSpacing(5)

		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(self.bar_frame, 0, QtCore.Qt.AlignLeft)
		layout.setContentsMargins(0, 0, 0, 0)

		self.setLayout(layout)

		self.btn_switch.clicked.connect(self.toggle_crumb_widget)
		self.btn_launch_explorer.clicked.connect(self.open_file_explorer)
		self.btn_copy_path.clicked.connect(self.copy_file_path)

	def toggle_crumb_widget(self, checked):
		if checked:
			self.tabbar_crumbs.hide()
			self.le_crumbs.show()
		else:
			self.tabbar_crumbs.show()
			self.le_crumbs.hide()

	def open_file_explorer(self):
		"""Opens file explorer
		"""
		armada.hooks.open_explorer_hook.OpenExplorer(self.parent.folders_view.currentIndex())

	def copy_file_path(self):
		"""Copies file path
		"""
		armada.hooks.copy_path_hook.CopyPath(self.parent.folders_view.currentIndex())


