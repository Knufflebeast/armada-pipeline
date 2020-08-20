from Qt.QtCore import Qt, QSortFilterProxyModel


class FoldersProxyModel(QSortFilterProxyModel):
	def __init__(self, parent=None):
		super(FoldersProxyModel, self).__init__(parent)

		# self.sort(0)
		self.sortRole()
		self.setDynamicSortFilter(True)
		self.setObjectName("folders_proxy_model")

	def filterAcceptsRow(self, source_row, source_parent):
		# Only first column in model for search
		index = self.sourceModel().index(source_row, 0, source_parent)

		if index.isValid():

			# index_type = index.data(role=Qt.UserRole + 1).lower()
			template_id = index.data(role=Qt.UserRole + 19).lower()

			# Hide all items including and below this type
			if template_id == 'major_component':
				return False

			return True

		return False

	def lessThan(self, left, right):
		left_data = self.sourceModel().data(left)
		right_data = self.sourceModel().data(right)
		return left_data < right_data
