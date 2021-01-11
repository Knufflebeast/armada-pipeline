import os
import sys
import json
import jsonschema

from Qt import QtWidgets, QtGui

from core import definitions
from core import resource
from core import schema
from core import exceptions
from launcher.gui import main_window as launcher_main_window
from startup.gui import main_window as startup_main_window

import utilsa
logging = utilsa.Logger('armada')
logger = logging.getLogger('main')

def _parse_settings():
	"""Gets data from current workspace file that is set by user

	Config properties
		ARMADA_DEBUG: str, Whether or not debug mode is active
		ARMADA_MOUNT_PREFIX: str, Path that contains the *_armadadata* folder
		ARMADA_{APP}_LOCATION: str, Path that contains the app root folder. For example the path to
			*Autodesk* directory or *Blender Foundation* directory. | "C:/Program Files/Autodesk" | "C:/Program Files"
		ARMADA_STUDIO: str, Company name | "ustwo"
		ARMADA_SITE: str, Where are you located? | "NYC-work" | "home-harlem"
	"""

	# Check if config exists
	if os.path.exists(definitions.GLOBAL_LOCAL_SETTINGS_FILE):
		logger.info('Default config detected...')
		pass
	#
	else:
		logger.info('No armada global settings detected, _armada_pipeline folder and start again')

	# Get json_data
	try:
		with open(definitions.GLOBAL_LOCAL_SETTINGS_FILE, 'r') as config_file:
			json_data = json.loads(config_file.read())
	# Check for config file's existance
	except FileNotFoundError as e:
		logger.exception(exceptions.path_error(
			definitions.GLOBAL_LOCAL_SETTINGS_FILE.rpartition(os.sep)[2],
			definitions.GLOBAL_LOCAL_SETTINGS_FILE,
			'Make sure a config file exists and the path is correct'
		))
		raise

	# Validate data
	# try:
	# 	jsonschema.validate(json_data, schema.get('user_config'))
	#
	# except jsonschema.exceptions.ValidationError as e:
	# 	raise jsonschema.exceptions.ValidationError(
	# 		"""{0}
	# 		\nLocation of file containing failed data:
	# 		\r\t{1}
	# 		\nSuggested Fixes:
	# 		\r\t"Check your config.json file to make sure it conforms to the config_schema.json"
	# 		""".format(e, definitions.GLOBAL_LOCAL_SETTINGS_FILE.replace('\\', '/')))

	# Create environment variables for each key in user_data
	for key, val in json_data['settings'].items():
		os.environ['{}'.format(key)] = val

	for key, val in json_data['workspaces'][json_data['settings']['ARMADA_CURRENT_WORKSPACE']].items():
		os.environ['{}'.format(key)] = val

def launch_armada():

	# Create log file
	logging.create_logfile()

	# Logging
	logger.warning('--- Armada root path: {} ---'.format(definitions.ROOT_PATH))
	logger.warning('--- Armada log path: {} ---'.format(os.path.join(definitions.TEMP_PATH, 'logs')))

	# Qt env vars
	os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
	os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # High dpi setting

	# Run Armada launcher
	app = QtWidgets.QApplication(sys.argv)
	QtGui.QFontDatabase.addApplicationFont("../../resources/fonts/Roboto/Roboto-Thin.ttf")
	# QtGui.QFontDatabase.addApplicationFont('resources/fonts/Roboto/Roboto-Thin.ttf')

	# Check for global local settings (True if no account exists)
	if not os.path.exists(definitions.USER_PATH):
		# Start setup
		window = startup_main_window.StartupMainWindow()
		window.exec()

	_parse_settings()

	window = launcher_main_window.MainWindow()
	window.show()
	print('starting launcher')

	sys.exit(app.exec_())


if __name__ == "__main__":
	launch_armada()
