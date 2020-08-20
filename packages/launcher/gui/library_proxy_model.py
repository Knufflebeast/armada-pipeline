from Qt import QtCore

from utilsa import Logger
logging = Logger('armada')


class LibraryProxyModel(QtCore.QSortFilterProxyModel):

	def __init__(self, parent=None):
		"""Defines sorting rules for library widget

		:type folder_widget: FileSystemWidget
		"""
		super(LibraryProxyModel, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building Library Proxy Model...')

		self.sort(0)
		self.setDynamicSortFilter(True)
		self.setRecursiveFilteringEnabled(True)
		self.setObjectName("library_proxy_model")

		self.text = ''
		self.index_selected_uuid = None

	def filterAcceptsColumn(self, source_column, source_parent):
		if source_column == 0:
			return True
		else:
			return False

	def filterAcceptsRow(self, source_row, source_parent):

		index_col1 = self.sourceModel().index(source_row, 0, source_parent)

		if index_col1.isValid():

			# index_parent_uuid = index_col1.parent().data(QtCore.Qt.UserRole)
			#
			# # Only show items that are below path
			# if self.index_selected_uuid == index_parent_uuid:
			#
			# 	return True

			return True

		# if len(self.text) > 0:
		# 	if text.find(self.text) >= 0:
		# 		return True
		#
		# 	for child_num in range(index.model().rowCount(parent=index)):
		# 		if self._accept_index(index.model().index(child_num, 0, parent=index)):
		# 			return True
		return False

	def lessThan(self, left, right):
		left_data = self.sourceModel().data(left)
		right_data = self.sourceModel().data(right)
		return left_data < right_data

