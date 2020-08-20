"""
Module for options tab within publish tab
"""
import importlib

from Qt.QtCore import Signal, Qt
from Qt.QtGui import QStandardItem
from Qt.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QBoxLayout

from packages import launcher

import utilsa
logging = utilsa.Logger('armada')


class SelectedWidget(QWidget):
	"""Fills selection info tab with an options tab widget
	"""

	updateInfo = Signal(QStandardItem)

	def __init__(self, parent=None, tree_model=None):
		super(SelectedWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building selected widget...')

		self.tree_model = tree_model
		self.parent = parent

		self.setMinimumWidth(500)

		self.details_frame = QFrame()
		self.details_widget = launcher.details_widget.DetailsWidget(self)
		# self.lv_frame.setStyleSheet("QFrame{background: red; border: 0px;}")

		self.line = QFrame()
		self.line.setFixedHeight(1)
		# self.line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.line.setStyleSheet("background-color: #636363;")
		self.line.setContentsMargins(5, 5, 5, 5)

		###########################################
		# Minors
		# Minors proxy model
		minors_proxy_model = launcher.minors_list_proxy_model.MinorsListProxyModel(self)
		minors_proxy_model.setSourceModel(self.tree_model)

		# Delegate
		self.custom_delegate = launcher.minors_list_item_delegate.MinorsListItemDelegate()

		# Minors list view
		self.lv_minors = launcher.minors_list_view.MinorsListView(self, self.tree_model)
		self.lv_minors.setModel(minors_proxy_model)
		self.lv_minors.setItemDelegate(self.custom_delegate)
		self.lv_minors.setContentsMargins(0, 0, 0, 0)
		self.lv_minors.setSpacing(0)
		self.lv_minors.setStyleSheet("""
		QListView{
			show-decoration-selected: 0;
			background: #262626;
			color:rgb(218,218,218) ;
			font:12px "Roboto-Thin";
			border: none;
			height: 200px;
			outline: 0;
		}""")
		self.lv_minors.hide()

		# Layout
		self.details_layout = QHBoxLayout(self.details_frame)
		self.details_layout.addWidget(self.details_widget)
		self.details_layout.setContentsMargins(0, 0, 0, 0)
		self.details_layout.setAlignment(Qt.AlignLeft)
		self.details_layout.setAlignment(Qt.AlignTop)

		self.list_view_layout = QBoxLayout(QBoxLayout.LeftToRight)
		self.list_view_layout.addWidget(self.lv_minors)
		self.list_view_layout.setContentsMargins(0, 0, 0, 0)
		self.list_view_layout.setAlignment(Qt.AlignLeft)
		self.list_view_layout.setAlignment(Qt.AlignTop)

		# self.data_layout = QtWidgets.QBoxLayout(QtWidgets.QVBoxLayout.Down)
		# self.data_layout.addWidget(self.lbl_path)
		# self.data_layout.addWidget(self.lbl_version)
		# self.data_layout.addWidget(self.lbl_creator)
		# self.data_layout.addWidget(self.lbl_last_edit)
		# self.data_layout.addWidget(self.lbl_status)
		# self.data_layout.addWidget(self.lbl_comments)

		self.main_layout = QVBoxLayout()
		self.main_layout.addWidget(self.details_frame)
		self.main_layout.addWidget(self.line)
		self.main_layout.addWidget(self.lv_minors)
		self.main_layout.setAlignment(Qt.AlignTop)
		# self.main_layout.addStretch(1)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)

		# Connections --------------------------------------
		# Launch software
		# From button
		self.custom_delegate.softwareLaunched.connect(self.software_launched)
		# From double click
		self.lv_minors.softwareLaunched.connect(self.software_launched)

	def software_launched(self, index_source):

		# todo: python 3 way of importing
		# launcher_path = resource.get(
		# 	'armada', 'utilsa', 'hooks', 'launchers',
		# 	'{}_hook.py'.format(index.data(Qt.UserRole + 3))
		# )
		# spec = importlib.util.spec_from_file_location("launch_hook.name", launcher_path)
		# software_hook = importlib.util.module_from_spec(spec)
		# spec.loader.exec_module(software_hook)
		# software_hook.Launch(index, model)

		# works w py2
		# module = importlib.import_module('armada.app.{0}.{0}_hook'.format(index.data(Qt.UserRole + 3)))
		# my_class = getattr(module, 'Launch')
		# my_class(index, model)
		software = index_source.data(Qt.UserRole + 3)

		import sys
		from pprint import pprint
		pprint(sys.path)

		module = importlib.import_module('armada.app.{0}.{0}_hook'.format(software))
		module.Launch(index_source, module.Launch.EXTERNAL)

