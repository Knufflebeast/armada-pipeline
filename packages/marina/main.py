__version__ = '2020.1a'

import json
import os
import sys


from Qt import QtWidgets

import marina
from marina.cmds import get_parent

from utilsa.logger import Logger
logging = Logger('marina')
logger = logging.getLogger('main')


def show_marina(ui_parent=True):
	# Get parent
	if ui_parent is True:
		ui_parent = get_parent.get_parent()
	print('UI parent : "{0}"'.format(ui_parent))

	# from packages import marina_settings
	from marina.gui import main_window

	try:
		# This needs to be before any other import statement due to env var vendor in logging
		# env_vars = EnvVars()
		# env_vars.set_user_data()
		app = QtWidgets.QApplication(sys.argv)
		import os

	except RuntimeError:
		pass

	# logging.create_logfile()

	window = main_window.MarinaWindow(parent=ui_parent)
	window.show()

	try:
		sys.exit(app.exec_())

	except:
		pass

	return window


if __name__ == "__main__":
	import jsonschema
	from armada import definitions
	from armada import exceptions
	from armada import schema
	# Setup python paths
	definitions.setup_python_paths()
	# _root_dir = definitions.ROOT_PATH
	# _source_dir = os.path.join(_root_dir, 'armada')
	# _packages_dir = os.path.join(_root_dir, 'packages')
	# _armada_marina_path = os.path.join(_root_dir, 'packages', 'marina')
	# _armada_launcher_path = os.path.join(_root_dir, 'packages', 'launcher')

	# def setup(path):
	# 	"""Setup the packages that have been decoupled from Marina.
	#
	# 	Args:
	# 		path: str, The foldr location that contains all the packages.
	#
	# 	Returns:
	#
	# 	"""
	# 	if os.path.exists(path):
	# 		print('ispath')
	# 	if os.path.exists(path) and path not in sys.path:
	# 		sys.path.append(path)
	# 		print('done')


	# setup(_root_dir)
	# setup(_source_dir)
	# setup(_packages_dir)
	# setup(_armada_marina_path)
	# setup(_armada_launcher_path)

	def _parse_config(config_file_path):
		"""Gets data from config file that is set by user

		Config properties
			ARMADA_DEBUG: str, Whether or not debug mode is active
			ARMADA_MOUNT_PREFIX: str, Path that contains the *_armadadata* folder
			ARMADA_{APP}_LOCATION: str, Path that contains the app root folder. For example the path to
				*Autodesk* directory or *Blender Foundation* directory. | "C:/Program Files/Autodesk" | "C:/Program Files"
			ARMADA_STUDIO: str, Company name | "ustwo"
			ARMADA_SITE: str, Where are you located? | "NYC-work" | "home-harlem"
		"""

		# Get json_data
		try:
			with open(config_file_path, 'r') as config_file:
				json_data = json.loads(config_file.read())
		# Check for config file's existance
		except FileNotFoundError as e:
			logger.exception(exceptions.path_error(
				config_file_path.rpartition(os.sep)[2],
				config_file_path,
				'Make sure a config file exists and the path is correct'
			))
			raise

		# Validate data
		try:
			jsonschema.validate(json_data, schema.get('user_config'))

		except jsonschema.exceptions.ValidationError as e:
			raise jsonschema.exceptions.ValidationError(
				"""{0}
				\nLocation of file containing failed data: 
				\r\t{1}
				\nSuggested Fixes: 
				\r\t"Check your config.json file to make sure it conforms to the config_schema.json"
				""".format(e, config_file_path.replace('\\', '/')))

		# Create environment variables for each key in user_data
		for key, val in json_data['env_vars'].items():
			os.environ['{}'.format(key)] = val

	# Vars
	config_file_path = definitions.CONFIG_FILE_PATH

	# Set environment variables from config.json
	_parse_config(config_file_path)

	# Create log file
	logging.create_logfile()
	# Logging
	logger.warning('--- Armada root path: {} ---'.format(definitions.ROOT_PATH))
	logger.warning('--- CONFIG ACTIVATED: {0} ---'.format(config_file_path))
	logger.warning('--- Debug mode: {0} ---'.format(os.environ['ARMADA_DEBUG']))
	logger.warning('--- Mount prefix: {0} ---'.format(os.environ['ARMADA_MOUNT_PREFIX']))

	# Qt env vars
	os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
	os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # High dpi setting

	os.environ['ARMADA_MAJOR_PARENTS'] = "000 485e3bfe-75f5-4e74-a06f-630a01dca79e 85fba2d8-74ae-47e3-a291-552b9a3f43b2 8470db56-366c-48bc-b6ea-fe2345127986 6d8ccab1-3062-4cb7-8c64-84c2536e1de4 a0e9e64b-27e0-4dfc-ac80-0d08199a8bdf c52543f1-183b-42e1-9195-3a1b0a9be8cf 805ed17e-56dc-4967-8f66-a629157635dc 1965e14c-11be-428e-b4ca-ed9f3d83ec48"
	os.environ['_MAJOR_UUID'] = '805ed17e-56dc-4967-8f66-a629157635dc'
	os.environ['_SOFTWARE'] = 'maya'

	show_marina(ui_parent=None)
