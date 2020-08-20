import json
import os
import sys

import jsonschema

from Qt import QtWidgets

from core import armada
from packages import launcher
import utilsa

logging = utilsa.Logger('armada')
logger = logging.getLogger('main')


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
		logger.exception(armada.exceptions.path_error(
			config_file_path.rpartition(os.sep)[2],
			config_file_path,
			'Make sure a config file exists and the path is correct'
		))
		raise

	# Validate data
	try:
		jsonschema.validate(json_data, armada.schema.get('user_config'))

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


def launch_armada():
	# Vars
	config_file_path = armada.definitions.CONFIG_FILE_PATH

	# Set environment variables from config.json
	_parse_config(config_file_path)

	# Create log file
	logging.create_logfile()
	# Logging
	logger.warning('--- Armada root path: {} ---'.format(armada.definitions.ROOT_PATH))
	logger.warning('--- CONFIG ACTIVATED: {0} ---'.format(config_file_path))
	logger.warning('--- Debug mode: {0} ---'.format(os.environ['ARMADA_DEBUG']))
	logger.warning('--- Mount prefix: {0} ---'.format(os.environ['ARMADA_MOUNT_PREFIX']))

	# Qt env vars
	os.environ['QT_PREFERRED_BINDING'] = 'PySide2'
	os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
	os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # High dpi setting

	# Run Armada launcher
	app = QtWidgets.QApplication(sys.argv)
	# QtGui.QFontDatabase.addApplicationFont('resources/fonts/Roboto/Roboto-Thin.ttf')

	window = launcher.main_window.MainWindow()
	window.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	launch_armada()
