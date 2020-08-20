'''get_parent @ mmm_cmds.universal_cmds

Gets the main UI's parent window
'''

import os

from Qt import QtWidgets

try:
	import hou
except:
	pass

def get_parent():
	"""Get parent window based on software"""

	software = os.getenv('_SOFTWARE')
	try:
		if software == 'maya':
			for obj in QtWidgets.QApplication.topLevelWidgets():
				if obj.objectName() == 'MayaWindow':
					return obj
			raise RuntimeError('Could not find MayaWindow instance')

		if software == 'houdini':
			return hou.ui.mainQtWindow()

		if software == 'nuke':
			for obj in QtWidgets.qApp.topLevelWidgets():
				if (obj.inherits('QMainWindow') and
						obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
					return obj
			else:
				raise RuntimeError('Could not find DockMainWindow instance')

		if software == 'blender':
			pass
			# for obj in QtWidgets.qApp.topLevelWidgets():
			# 	print(obj.metaObject().className())
			# 	if (obj.inherits('QMainWindow') and
			# 			obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
			# 		return obj
			# else:
			# 	raise RuntimeError('Could not find DockMainWindow instance')

	except:
		print('Running from dev')