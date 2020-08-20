"""
Module for main AssetsWidget

The AssetsWidget a library context where users can browse for files based on asset attributes
"""
from utilsa import Logger

from Qt import QtWidgets

logging = Logger('armada')
logger = logging.getLogger(__name__)


class AssetsWidget(QtWidgets.QWidget):
	"""
	Fills Assets UI with contents

	Connection gets data from folders_tree_view and sends it to assets_tree_view
	"""

	def __init__(self, parent=None):
		super(AssetsWidget, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building assets tab...')

		self.parent = parent
		self.setObjectName('armada_AssetsWidget')

		# # GUI
		# self.tw_selected_tab = selected_widget.SelectedWidget()
		# self.tw_options = options_tab_widget.OptionsTabWidget()
		# self.le_search = search_line_edit.SearchLineEdit()
		# self.library_options_widget = library_options_widget.LibraryOptionsWidget()
		#
		# # Layout
		# self.search_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		# self.search_split.addWidget(self.le_search)
		# self.search_split.addWidget(self.library_options_widget)
		# self.search_split.setChildrenCollapsible(False)
		# self.search_split.setStretchFactor(0,1)
		# self.search_split.setHandleWidth(5)
		#
		# self.asset_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		# self.asset_split.addWidget(self.tw_selected_tab)
		# self.asset_split.setChildrenCollapsible(False)
		# self.asset_split.setStretchFactor(1,1)
		# self.asset_split.setHandleWidth(5)
		#
		# self.vert_split = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		# self.vert_split.addWidget(self.search_split)
		# self.vert_split.addWidget(self.asset_split)
		# self.vert_split.setChildrenCollapsible(False)
		# self.vert_split.setStretchFactor(1,0)
		# self.vert_split.setHandleWidth(5)
		#
		# self.main_layout = QtWidgets.QVBoxLayout()
		# self.main_layout.addWidget(self.vert_split)
		# self.main_layout.setContentsMargins(0, 0, 0, 0)

		# self.setLayout(self.main_layout)

		# Connections
		# self.folders_widget.tv_folders.itemSelectionChanged.connect(self.library_widget.lv_library.folder_selection_changed)

		# self.library_widget.lv_library.itemSelectionChanged.connect(self.tw_selected_tab.selected_widget.preview_image)

		# self.le_search.textChanged.connect(self.library_widget.lv_library.search_text_changed)

		# self.library_options_widget.sort_state.connect(self.library_widget.tv_library.toggle_sorting)
		# self.library_options_widget.order_state.connect(self.library_widget.tv_library.set_order)
		# self.library_options_widget.role_state.connect(self.library_widget.tv_library.set_role)


