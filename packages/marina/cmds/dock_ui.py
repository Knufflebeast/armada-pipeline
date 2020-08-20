"""
dock_ui @ mmm_cmds.universal_cmds
"""

import os

# Maya
try:
	import maya.cmds as mc

except:
	pass

# Nuke
try:
	import nuke
	import nukescripts

except:
	pass

# Blender
try:
	import bpy

except:
	pass

import utilsa
logging = utilsa.Logger('marina')
logger = logging.getLogger(__name__)


def dock_ui(wParent=None):
	"""Docks the main window."""

	logger.warning('Docking MMM UI...')

	software = os.getenv('_SOFTWARE')
	parent = wParent

	# Maya
	if software == 'maya':
		# pass
		# if os.getenv('APP_VER') != '2016':

		workspaceControlName = parent.objectName() + 'WorkspaceControl'
		logger.info('Workspace control name : {0}'.format(workspaceControlName))

		# Delete UI if it already exists
		if mc.workspaceControl(workspaceControlName, q=True, exists=True):
			mc.workspaceControl(workspaceControlName, e=True, close=True)
			mc.deleteUI(workspaceControlName, control=True)

		# This class is inheriting MayaQWidgetDockableMixin.show(), which will eventually call maya.cmds.workspaceControl.
		# I'm calling it again, since the MayaQWidgetDockableMixin dose not have the option to use the "tabToControl" flag,
		# which was the only way i found to dock my window next to the channel controls, attributes editor and modelling toolkit.
		parent.show(dockable=True, area='right', floating=False)
		mc.workspaceControl(workspaceControlName,
			e=True,
			tabToControl=["AttributeEditor", -1],
			widthProperty="preferred",
			initialWidth = 500,
			minimumWidth=500,
			retain = False,
			label='mb_Marina')
		#parent.raise_()


		# if os.getenv('APP_VER') == '2016':
		#
		# 	if mc.dockControl(parent.objectName(), q=1, ex=1):
		# 		mc.deleteUI(parent.objectName())
		#
		# 	parent.dockCtrl = mc.dockControl(
		# 		aa='right', a='right',
		# 		content=parent.objectName(),
		# 		w=500, label='mb_Marina'
		# 	)

	# Houdini
	if software == 'houdini':
		'''Panel docking can be found in resource.apps.houdini.scripts.123
		'''
		print('houdini dock logic')
		pass

	# Nuke
	if software == 'nuke':
		pane = nuke.getPaneFor('Properties.1')
		nukescripts.panels.registerWidgetAsPanel(
			'MB_MMV', 'Test Panel', 'MMV_panel', True
		).addToPane(pane)

	# Blender
	if software == 'blender':
		print('need blender logic')
		pass


