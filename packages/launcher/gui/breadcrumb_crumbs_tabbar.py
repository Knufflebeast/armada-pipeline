from Qt import QtWidgets, QtCore, QtGui

from core import armada

import utilsa
logging = utilsa.Logger('armada')


class BreadcrumbCrumbsTabbar(QtWidgets.QTabBar):
	"""Breadcrumb address bar
	"""

	breadcrumbSelectionChanged = QtCore.Signal(QtGui.QStandardItem)

	def __init__(self, parent=None, index_source=None):
		"""

		Args:
			parent:
			index_source: QModelIndex from folder tree view
		"""
		super(BreadcrumbCrumbsTabbar, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

		# Set start tab
		self.folder_selection_changed(index_source)

		self.setMinimumWidth(10)
		self.setDrawBase(False)  # Prevents a weird line from drawing at the bottom of the tabs

		# Connections
		self.tabBarClicked.connect(self.breadcrumb_selection_changed)

	def minimumSizeHint(self):
		return QtCore.QSize(10, 90)

	def breadcrumb_selection_changed(self, index):
		"""Triggered when the breadcrumb tab item changes selection.

		Emits itemSelectionChanged signal and send

		Args:
			index:

		Returns:

		"""
		if index == -1:
			pass
		else:
			self.logger.debug('Breadcrumb selection signal emit')
			self.logger.debug('Breadcrumb selected index = {}'.format(self.tabData(index)))
			self.logger.debug('Breadcrumb selected name = {}'.format(self.tabData(index).data(QtCore.Qt.DisplayRole)))

			self.breadcrumbSelectionChanged.emit(self.tabData(index))

	def path_from_index(self, index_source):
		"""Sets self.emit_dict so that data can be sent to library view

		Args:
			index_source: QtCore.QModelIndex
		"""

		parent_index = index_source.parent()
		parent_data = parent_index.data(QtCore.Qt.DisplayRole)
		index_data = index_source.data(QtCore.Qt.DisplayRole)
		tab_count = self.count()

		# If index has a parent, keep going up hierarchy
		if parent_data is not None:
			# Don't create arrow tab on this item (last item)
			template_id = armada.structure.get_type_data(index_source.data(QtCore.Qt.UserRole + 1), armada.structure.TEMPLATE_ID)
			if template_id == 'task':
				pass
			# Make tab arrow
			else:
				tab_arrow = self.insertTab(0, '')
				self.setTabData(tab_arrow, None)
				self.setTabIcon(tab_arrow, armada.resource.color_svg('arrow_right', 128, '#FFFFFF'))
				self.setTabEnabled(tab_arrow, False)

			# Make tab
			tab = self.insertTab(0, index_data)
			self.setTabData(tab, index_source)

			self.path_from_index(parent_index)

		# Last index
		elif parent_data is None:
			# Create arrow tab
			tab_arrow = self.insertTab(0, '')
			self.setTabData(tab_arrow, None)
			self.setTabIcon(tab_arrow, armada.resource.color_svg('arrow_right', 128, '#FFFFFF'))
			self.setTabEnabled(tab_arrow, False)

			# Tab
			tab = self.insertTab(0, index_data)
			self.setTabData(tab, index_source)

	def folder_selection_changed(self, index_source=None):
		"""On folder tree view selection changed

		Args:
			index_source: QModelIndex

		Returns:

		"""
		if index_source.column() == 1:
			index_source = index_source.model().index(index_source.row(), 0, index_source.parent())

		# Clear breadcrumbs
		for i in range(self.count()-1, -1, -1):
			self.removeTab(i)

		self.path_from_index(index_source)

		# # Make breadcrumbs
		# for i in range(len(dir_list)-1, -1, -1):
		#
		# 	# Last tab
		# 	if dir_list[i] == dir_list[0]:
		# 		tab = self.addTab(str(dir_list[i]))
		# 		self.setTabData(tab, index)
		#
		# 	# Other tabs
		# 	else:
		# 		tab = self.addTab(str(dir_list[i]))
		# 		self.setTabData(tab, index)
		# 		# Create arrow tab
		# 		tab_arrow = self.addTab(None)
		# 		self.setTabData(tab_arrow, 'hey')
		# 		self.setTabIcon(tab_arrow, resource.color_svg('arrow_right', 128, '#FFFFFF'))
		# 		self.setTabEnabled(tab_arrow, False)

		# self.setCurrentIndex(self.count()-1)

	def paintEvent(self, _e):
		"""Override paintEvent to draw the tabs like we want to.

		Args:
			_e:

		Returns:

		"""
		painter = QtWidgets.QStylePainter(self)
		tab = QtWidgets.QStyleOptionTab()
		selected = self.currentIndex()

		for idx in range(self.count()):
			# painter.begin(self)
			self.initStyleOption(tab, idx)

			# Text
			if tab.text is not '':
				painter.setRenderHint(QtGui.QPainter.Antialiasing)

				path = QtGui.QPainterPath()
				# path.addRoundedRect(
				# 	tab.rect.left(),
				# 	tab.rect.top(),
				# 	tab.rect.width(),
				# 	tab.rect.height(),
				# 	15,
				# 	15
				# )
				path.addRect(
					tab.rect.left(),
					tab.rect.top() + tab.rect.height() - 5,
					tab.rect.width(),
					5
				)

				if tab.state & QtWidgets.QStyle.State_MouseOver:
					painter.fillPath(path, QtGui.QColor('#5a5a5a'))
				# if tab.state & QtWidgets.QStyle.State_Selected:
				# 	painter.fillPath(path, QtGui.QColor('#2c998e'))
				# else:
				# 	painter.fillPath(path, QtGui.QColor('#5a5a5a'))

				rect_text = QtCore.QRect(
					tab.rect.left(),
					tab.rect.top() - 2,
					tab.rect.width(),
					tab.rect.height() + 2
				)

				QtWidgets.QApplication.style().drawItemText(
					painter, rect_text, QtCore.Qt.AlignCenter, tab.palette, True, tab.text
				)

			# Separator
			else:
				index_icon = tab.icon

				pixmap_icon = index_icon.pixmap(128, 128)
				pixmap_icon_scaled = pixmap_icon.scaled(
					tab.rect.width() + 8,
					tab.rect.height() + 8,
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation
				)
				QtWidgets.QApplication.style().drawItemPixmap(
					painter,
					tab.rect,
					QtCore.Qt.AlignCenter,
					pixmap_icon_scaled
				)

			# painter.end()

			if tab.rect.right() < 0 or tab.rect.left() > self.width():
				# Don't bother drawing a tab if the entire tab is outside of
				# the visible tab bar.
				continue

			# painter.drawControl(QtWidgets.QStyle.CE_TabBarTab, tab)







