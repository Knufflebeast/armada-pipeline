import os
import sys

from Qt import QtWidgets, QtGui

from core import definitions
from core import resource
from startup.gui import main_window

import utilsa
logging = utilsa.Logger('armada')
logger = logging.getLogger('main')


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

	# Check for existing user or workspace
	data = resource.json_read(definitions.USER_PATH, filename='armada_settings')

	window = main_window.StartupMainWindow()
	window.show()

	# if data['CURRENT_USER'] is "":
	# 	print('need user')
	# 	window = log_in.LogIn()
	# 	window.show()
	# else:
	# 	print('have user')
	# 	pass

	# if data['CURRENT_WORKSPACE'] is "":
	# 	print('need workspace')
	# 	window = create_workspace.CreateWorkspace()
	# 	window.show()
	# else:
	# 	print('have workspace')
	# 	window = launcher_main_window.MainWindow()
	# 	window.show()
	# 	print('starting launcher')

	sys.exit(app.exec_())


if __name__ == "__main__":
	launch_armada()
