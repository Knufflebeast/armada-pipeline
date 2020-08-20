"""
file_manip @ mmm_cmds.universal_cmds
"""

import os

from core import armada

# Maya
try:
	import maya.cmds as mc
	import maya.mel as mel
except:
	pass

# Houdini
try:
	import hou
except:
	pass

# Nuke
try:
	import nuke
except:
	pass

# Blender
try:
	import bpy
except:
	pass

# Logging
import utilsa

logging = utilsa.Logger('marina')


software = os.getenv('SOFTWARE')


class FileManip(object):

	EXISTING, NEW = (0, 1)
	MAYA, HOUDINI, NUKE, BLENDER = ('maya', 'houdini', 'nuke', 'blender')

	def __init__(self, software=None, save_type=EXISTING,):
		super(FileManip, self).__init__()
		self.logger = logging.getLogger('file.' + self.__class__.__name__)

		self.software = software
		self.save_type = save_type

	def open_file(self, index_source):
		"""Opens *filePath*"""

		file_path = armada.resolver.generate_path(index_source, 'user')
		self.logger.info('Opening file : %s' % file_path)
		print('open file path = {}'.format(file_path))

		if self.software == self.MAYA:
			mc.file(file_path, open=1, force=1)
			print('open file path = {}'.format(file_path))
			mel.eval('setProject "{0}"'.format(os.getenv('WORKING_DIR')))

		if self.software == self.HOUDINI:
			hou.hipFile.load(file_path, suppress_save_prompt=True)

		if self.software == self.NUKE:
			nuke.openScript(file_path)

		if self.software == self.BLENDER:
			bpy.ops.wm.open_mainfile(filepath=file_path)

	def rename_file(self, init_file_path, new_file_path):
		"""Moves *srcFilePath* file to *dstFilePath* by renaming srcFile."""

		self.logger.info('Renaming this file... : %s' % init_file_path)
		self.logger.info('To this file          : %s' % new_file_path)

		if self.software == self.MAYA:
			mc.sysFile(init_file_path, rename=new_file_path)

		if self.software == self.HOUDINI:
			os.rename(init_file_path, new_file_path)

		if self.software == self.NUKE:
			os.rename(init_file_path, new_file_path)

		if self.software == self.BLENDER:
			print('need rename')

	def save_file(self, new_file_path=None):
		"""If saving from an existing file, rename current *init_file_path*
		to *new_file_path*, then save.

		If creating a file (done while opening a minor for the first time
		from a new software), then just create the file at the *new_file_path*

		Args:
			init_file_path:
			new_file_path:
			save_type: str, existing | new

		Returns:

		"""

		if self.software == self.MAYA:
			if self.save_type == self.EXISTING:
				self.logger.info('Existing save')
				# Get current file path
				init_file_path = mc.file(q=True, sn=True)
				# Rename file
				mc.file(init_file_path, rename=new_file_path)
				# Save file (this opens the file as well)
				mc.file(force=True, save=True)
			if self.save_type == self.NEW:
				self.logger.info('New save')
				new_file = mc.file(force=True, new=True)
				mc.file(new_file, rename=new_file_path)
				mc.file(force=True, save=True)

		if self.software == self.HOUDINI:
			if self.save_type == self.EXISTING:
				hou.hipFile.save(new_file_path)
			elif self.save_type == self.NEW:
				hou.hipFile.clear(suppress_save_prompt=False)
				hou.hipFile.save(new_file_path)

		if self.software == self.NUKE:
			pass

		if self.software == self.BLENDER:
			if self.save_type == self.EXISTING:
				self.logger.info('Existing save')
				bpy.ops.wm.save_mainfile(filepath=new_file_path)
				bpy.ops.wm.open_mainfile(filepath=new_file_path)
			if self.save_type == self.NEW:
				# self.logger.info('New save')
				print('new file path = {}'.format(new_file_path))
				bpy.ops.wm.save_as_mainfile(filepath=new_file_path)
				# bpy.ops.wm.save_as_mainfile(filepath=r'D:/OneDrive/Job_Stuff/Projects/ARMADA/Projects/Facebook/Go_Go_Bots/Characters/Halo/Production/Abilities/Shield/blender/scenes/Aaa-001.0001.blend')
				# bpy.ops.wm.open_mainfile(filepath=repr(new_file_path))
				print('file should have been saved')

	def copy_file(self, init_file_path, new_file_path):
		"""Copies *srcFilePath* to *dstFilePath*."""

		self.logger.info('Copying file')

		if self.software == self.MAYA:
			mc.sysFile(init_file_path, copy=new_file_path)

		if self.software == self.HOUDINI:
			new_file = hou.hipFile.setName(new_file_path)
			hou.hipFile.save(new_file)

		if self.software == self.NUKE:
			pass

		if self.software == self.BLENDER:
			pass

	def increment_save(self):
		"""Increments file using software's native increment command."""

		self.logger.info('Incremental save')

		if self.software == self.MAYA:
			mc.IncrementAndSave()

		if self.software == self.HOUDINI:
			hou.hipFile.saveAndIncrementFileName()

		if self.software == self.NUKE:
			pass

		if self.software == self.BLENDER:
			bpy.ops.file.filenum(increment=1)