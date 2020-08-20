"""
Module for contextually filling the options tab.

Context is based on asset type
"""

from Qt import QtWidgets

class OptionsTabContents(QtWidgets.QWidget):
	"""
	Fills options tab with contents based on asset selection

	Connections are created contextually based on asset type

	note, currently only supports signals for geometry asset type
	"""
	
	def __init__(self, parent=None):
		super(OptionsTabContents, self).__init__(parent)
		
		self.setMinimumWidth(600)
		
		self.create_items1 = []
		self.create_items2 = []
		
		self.create_gui()
		self.create_layout()
		

	# ------------------------------------------------------
	def create_gui( self ):
		self.chbx_groups = QtWidgets.QCheckBox('Groups')
		self.chbx_groups.toggle()
		self.create_items1.append(self.chbx_groups)

		self.chbx_point_groups = QtWidgets.QCheckBox('Point Groups')
		self.chbx_point_groups.toggle()
		self.create_items1.append(self.chbx_point_groups)

		self.chbx_materials = QtWidgets.QCheckBox('Materials')
		self.chbx_materials.toggle()
		self.create_items1.append(self.chbx_materials)

		self.chbx_smoothing = QtWidgets.QCheckBox('Smoothing')
		self.chbx_smoothing.toggle()
		self.create_items2.append(self.chbx_smoothing)

		self.chbx_normals = QtWidgets.QCheckBox('Constraints')
		self.chbx_normals.toggle()
		self.create_items2.append(self.chbx_normals)
		

	#------------------------------------------------------
	def create_layout(self):

		self.options_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
		
		if self.create_items1:
			self.options_column_layout1 = QtWidgets.QVBoxLayout()
			for widget in self.create_items1:
				self.options_column_layout1.addWidget(widget)
		
			self.options_layout.addLayout(self.options_column_layout1)
		
		if self.create_items2:
			self.options_column_layout2 = QtWidgets.QVBoxLayout()
			for widget in self.create_items2:
				self.options_column_layout2.addWidget(widget)

			self.options_layout.addLayout(self.options_column_layout2)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.options_layout)

		self.setLayout(self.main_layout)
		
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	def create_connections(self):
		pass
		#self.chbx_obj_export.stateChanged.connect(self.on_type_selected )

	