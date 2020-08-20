"""
Module for prep asset popup. 
"""
import os
import platform
import errno
# from pathlib import Path
import shutil

from Qt import QtCore, QtWidgets, QtGui

from core import armada

import utilsa
logging = utilsa.Logger('armada')

op_sys = platform.system()
if op_sys == 'Darwin':
	from Foundation import NSURL

class ThumbnailPopup(QtWidgets.QDialog):
	"""Updates the thumbnail of the item
	"""

	# Signal vars
	enter_pressed = QtCore.Signal(str)
	enter_signal_str = "returnPressed"
	esc_pressed = QtCore.Signal(str)
	esc_signal_str = "escPressed"

	def __init__(self, parent=None, index_proxy_sel=None, index_proxy_folders=None, tree_proxy=None):
		"""

		Args:
			parent: RightClickMenu widget
			index_proxy_sel: QModelIndex being deleted
			index_proxy_folders: QModelIndex selected in folder view
			tree_proxy: QSortFilterProxyModel
		"""

		super(ThumbnailPopup, self).__init__()

		self.logger = logging.getLogger('gui.' + self.__class__.__name__)
		self.logger.info('Delete popup open...')

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setStyleSheet(armada.resource.style_sheet('popup_window'))
		self.installEventFilter(self)

		self.parent = parent
		self.index_proxy_sel = index_proxy_sel
		self.index_source_sel = self.index_proxy_sel.model().mapToSource(self.index_proxy_sel)
		self.index_proxy_folders = index_proxy_folders
		self.index_source_folders = self.index_proxy_folders.model().mapToSource(self.index_proxy_sel)
		self.index_source_sel_type = self.index_source_sel.data(QtCore.Qt.UserRole + 1)
		self.index_source_sel_name = self.index_source_sel.data(QtCore.Qt.DisplayRole)
		self.tree_proxy = tree_proxy
		self.tree_model = self.tree_proxy.sourceModel()
		self.sel_type = self.index_source_sel_type
		# Enable dragging and dropping onto the GUI
		self.setAcceptDrops(True)

		# GUI ------------------------------
		self.lbl_title = QtWidgets.QLabel('Update Thumbnail')
		self.new_icon = armada.structure.get_type_data(self.sel_type, armada.structure.ICON)

		self.lbl_asset_name = QtWidgets.QPushButton(
			armada.resource.color_svg(
				self.new_icon,
				1024,
				'#FFFFFF'
			), ''
		)
		# self.lbl_asset_name.setText("{0}'s new thumbnail path:".format(self.index_source_sel_name))
		self.lbl_asset_name.setText("New thumbnail path:")
		self.lbl_asset_name.setStyleSheet(armada.resource.style_sheet('icon_label'))

		self.le_thumbnail_path = QtWidgets.QLineEdit()
		self.le_thumbnail_path.setAlignment(QtCore.Qt.AlignLeft)

		self.btn_mount_browse = QtWidgets.QPushButton("Browse")
		self.btn_mount_browse.setMinimumWidth(100)

		self.lbl_preview = QtWidgets.QLabel("Browse or drag and drop an image into this window \n\nOnly 'png' files at the moment.")
		self.lbl_preview.setAlignment(QtCore.Qt.AlignCenter)

		icon_upload = armada.resource.color_svg('upload', 128, '#969696', return_type=armada.resource.PIXMAP)
		self.lbl_upload = QtWidgets.QLabel()
		self.lbl_upload.setPixmap(icon_upload)

		self.btn_accept = QtWidgets.QPushButton("Accept")
		self.btn_cancel = QtWidgets.QPushButton("Cancel")

		# Layout ---------------------------
		self.title_layout = QtWidgets.QVBoxLayout()
		self.title_layout.addWidget(self.lbl_title)
		self.title_layout.setAlignment(QtCore.Qt.AlignTop)

		self.name_layout = QtWidgets.QHBoxLayout()
		self.name_layout.addWidget(self.lbl_asset_name)
		self.name_layout.addWidget(self.le_thumbnail_path)
		self.name_layout.addWidget(self.btn_mount_browse)
		self.name_layout.setAlignment(QtCore.Qt.AlignTop)

		self.upload_layout = QtWidgets.QVBoxLayout()
		self.upload_layout.addWidget(self.lbl_upload, 0, QtCore.Qt.AlignCenter)
		self.upload_layout.addWidget(self.lbl_preview, 0, QtCore.Qt.AlignCenter)
		self.upload_layout.setAlignment(QtCore.Qt.AlignCenter)

		self.button_layout = QtWidgets.QHBoxLayout()
		self.button_layout.addWidget(self.btn_accept)
		self.button_layout.addWidget(self.btn_cancel)
		self.button_layout.setAlignment(QtCore.Qt.AlignBottom)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.title_layout)
		self.main_layout.addLayout(self.name_layout, QtCore.Qt.AlignTop)
		self.main_layout.addLayout(self.upload_layout, QtCore.Qt.AlignCenter)
		# self.main_layout.addStretch()
		self.main_layout.addLayout(self.button_layout)

		self.setLayout(self.main_layout)

		# Connections
		self.le_thumbnail_path.textChanged.connect(self.on_text_changed)
		self.btn_mount_browse.clicked.connect(self.on_browse_pressed)
		self.btn_accept.clicked.connect(self.on_accept_pressed)
		self.btn_cancel.clicked.connect(self.on_cancel_pressed)

		self.enter_pressed.connect(self.on_accept_pressed)
		self.esc_pressed.connect(self.on_cancel_pressed)

	def on_text_changed(self, text):
		"""Remove banned characters from name string
		"""
		# Determine new width of popup
		init_width = self.frameGeometry().width()
		lbl_name_width = self.lbl_asset_name.frameGeometry().width()
		le_asset_name_width = self.le_thumbnail_path.frameGeometry().width()
		font_metrics = self.le_thumbnail_path.fontMetrics()
		text_width = font_metrics.boundingRect(text).width()
		new_width = max(lbl_name_width + text_width + 50, init_width)

		if new_width > init_width:
			self.setFixedWidth(new_width)
			diff = int((new_width - init_width) / 2)
			self.move(QtCore.QPoint(self.pos().x() - diff, self.pos().y()))

	def on_browse_pressed(self):
		"""

		Returns:

		"""

		if armada.structure.get_type_data(self.index_source_sel_type, armada.structure.TEMPLATE_ID) == 'major_component':
			current_dir = armada.resolver.generate_path(self.index_source_sel.parent(), armada.resolver.USER)
		else:
			current_dir = armada.resolver.generate_path(self.index_source_sel, armada.resolver.USER)
		self.file_dialog = QtWidgets.QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.AnyFile)
		self.file_dialog.setDirectory(current_dir)
		self.file_dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
		self.file_dialog.setOption(self.file_dialog.HideNameFilterDetails, False)
		path = self.file_dialog.getOpenFileName(self, 'Choose thumbnail file', directory=current_dir, filter="*.png")[0]
		if path:
			self.le_thumbnail_path.setText(path)
			self.load_image()

	def load_image(self):
		"""
		Set the image to the pixmap
		:return:
		"""
		self.pixmap_preview_updated = QtGui.QPixmap(self.le_thumbnail_path.text())

		pixmap_scaled = self.pixmap_preview_updated.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
		self.lbl_preview.setPixmap(pixmap_scaled)
		self.lbl_upload.hide()
		# The following three methods set up dragging and dropping for the app

	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		"""
		Drop files directly onto the widget
		File locations are stored in fname
		:param e:
		:return:
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			# Workaround for OSx dragging and dropping
			for url in e.mimeData().urls():
				if platform.system().lower() in ['windows']:
					fname = str(url.toLocalFile())
				elif platform.system().lower() in ['darwin']:
					fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
			print(fname.rpartition('.')[0] + '.' + fname.rpartition('.')[2].lower())

			self.le_thumbnail_path.setText(fname)

			self.load_image()
		else:
			e.ignore()

	def on_accept_pressed(self):
		"""Updates thumbnail
		"""
		image_path = self.le_thumbnail_path.text()

		if os.path.exists(image_path):
			icon_preview_update = QtGui.QIcon(QtGui.QPixmap(image_path))

			item = self.tree_model.itemFromIndex(self.index_source_sel)
			item.setData(icon_preview_update, QtCore.Qt.UserRole + 2)

			init_image_path = self.le_thumbnail_path.text()
			new_image_path = "{0}/image.png".format(armada.resolver.generate_path(self.index_source_sel, armada.resolver.DATA))
			shutil.copy(init_image_path, new_image_path)

			# Update model
			self.tree_model.setData(self.index_source_sel, icon_preview_update, QtCore.Qt.UserRole + 2)

			# Update views
			self.tree_model.dataChanged.emit(self.index_source_sel.parent(), self.index_source_sel)

			# Select item in view
			# self.parent.parent.folders_view._selection_changed()
			# self.parent.parent.folders_view.setCurrentIndex(self.index_source_sel)
			self.parent.parent.library_view._selection_changed()

			self.close()

		else:
			self.logger.warning(
				'Path to image not found! Browse to an image file or drag and drop an image into the "Update Thumbnail" window.')

	def on_cancel_pressed(self):
		"""Cancel button pressed
		"""
		self.deleteLater()
		self.close()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Return:
			self.enter_pressed.emit(self.enter_signal_str)
			return True
		if event.key() == QtCore.Qt.Key_Escape:
			self.esc_pressed.emit(self.esc_signal_str)
			return True
		else:
			super(ThumbnailPopup, self).keyPressEvent(event)


