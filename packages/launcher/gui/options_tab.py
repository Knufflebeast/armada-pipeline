"""
Module for options tab within publish tab
"""


from Qt import QtWidgets

from packages import launcher


class OptionsTab(QtWidgets.QTabWidget):
	"""
	Fills publish UI with an options tab widget
	"""
	
	def __init__(self, parent=None):
		super(OptionsTab, self).__init__(parent)

		self.create_gui()
		self.create_layout()

	#------------------------------------------------------
	def create_gui( self ):
		self.le_label = QtWidgets.QLabel('Comments: ')
		self.le_comments = QtWidgets.QLineEdit()

		self.btn_publish = QtWidgets.QPushButton("Publish")
		#self.btn_publish.setStyleSheet("background-color: rgb({0},{0},{0});".format(val))
		self.option_tab_contents = launcher.options_tab_contents.OptionsTabContents()

	#------------------------------------------------------
	def create_layout( self ):
		self.main_layout = QtWidgets.QHBoxLayout()

		self.main_layout.addWidget( self.option_tab_contents )

		comments_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
		comments_layout.addWidget(self.le_label)
		comments_layout.addWidget(self.le_comments)

		pub_layout = QtWidgets.QVBoxLayout()
		pub_layout.addLayout(comments_layout)
		pub_layout.addWidget(self.btn_publish)

		self.main_layout.addLayout(comments_layout)
		self.main_layout.addLayout(pub_layout)

		self.setLayout( self.main_layout )
		
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	def create_connections( self ):
		
		pass