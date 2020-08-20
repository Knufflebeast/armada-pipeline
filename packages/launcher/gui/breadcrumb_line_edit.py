import os
import errno
import platform
import subprocess

from Qt import QtWidgets, QtCore

from core import armada

from utilsa import Logger

logging = Logger('armada')


class BreadcrumbLineEdit(QtWidgets.QLineEdit):
    """Search bar for library filter
    """
    btnCopyClicked = QtCore.Signal(bool)
    btnLaunchClicked = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(BreadcrumbLineEdit, self).__init__(parent)

        self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)

        self.setClearButtonEnabled(True)
        self.setMaximumSize(700, 30)
        self.addAction(armada.resource.icon('folder_white', 'png'), self.LeadingPosition)
        self.setPlaceholderText("File path placeholder")

    def on_btn_explorer_clicked(self):
        """Open file explorer path"""

        if platform.system().lower() in ['windows']:
            executable = 'explorer'

        full_path = os.path.join(
            self.text()
        ).replace('/', '\\')

        try:
            subprocess.Popen([executable, full_path], shell=True)

        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

        self.logger.info(u'Opening directory : "%s"' % full_path)

    def on_btn_copy_clicked(self):
        """Copies file path on breadcrumb bar"""

        self.logger.info(u'Copying directory : "%s"' % 'full_path')