""".. _search_line_edit:

mb_armada.gui.search_line_edit
*************************
"""
from Qt import QtWidgets

from core import armada

import utilsa
logging = utilsa.Logger('armada')
logger = logging.getLogger(__name__)


class SearchLineEdit(QtWidgets.QLineEdit):
	"""
	Search bar for library filter
	"""

	def __init__(self, parent=None):
		super(SearchLineEdit, self).__init__(parent)

		self.logger = logging.getLogger('launcher.gui.' + self.__class__.__name__)
		self.logger.info('Building search line edit...')

		self.setClearButtonEnabled(True)
		self.addAction(armada.resource.icon('search_icon', 'png'), self.LeadingPosition)
		self.setPlaceholderText("Search files...")

