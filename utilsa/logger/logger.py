import os
import tempfile
from logging import *
import logging.config
import datetime
import getpass

from core import definitions

class Logger():
	def __init__(self, logger_name=None):
		"""Use:
		import utilsa
		logging = utilsa.Logger('rootLogger')
		logger = logging.getLogger(__name__)

		:param logger_name: root logger name
		"""

		self.log_dir = os.path.join(definitions.ROOT_PATH, 'logs')
		self.logger_name = logger_name

		if not self.log_dir:
			sys_temp = tempfile.gettempdir()
			self.log_dir = os.path.join(sys_temp, self.logger_name)

		if not os.path.exists(self.log_dir):
			os.makedirs(self.log_dir)

	def create_logfile(self):
		"""
		:return:
		"""

		logfile = tempfile.NamedTemporaryFile(
			prefix=self.get_logger_prefix(),
			suffix='.log',
			delete=False,
			dir=self.log_dir
		).name

		# formatter_relative_path = os.path.join(
		# 	os.path.relpath(os.path.dirname(__file__), os.getenv('ARMADA_ROOT_PATH')),
		# 	'formatters',
		# 	'ColorFormatter'
		# ).replace('\\', '.')
		#
		# print('formatter path: {}'.format(formatter_relative_path))

		default_log_settings = {
			'version': 1,
			'handlers': {
				'console': {
					'class': 'logging.StreamHandler',
					'level': 'WARNING',
					'formatter': 'default',
					'stream': 'ext://sys.stdout',
				},
				'file': {
					'class': 'logging.handlers.RotatingFileHandler',
					'level': 'DEBUG',
					'formatter': 'file',
					'filename': logfile,
					'mode': 'a',
					'maxBytes': 10485760,
					'backupCount': 5,
				},

			},
			'formatters': {
				'default': {
					'()': ColorFormatter,
					'format': (
						'%(levelname)s [%(asctime)s] %(name)s.%(funcName)s() @%(lineno)d - '
						'%(message)s '
					),
					'datefmt': (
						'%m/%d/%Y %I:%M:%S %p'
					)
				},
				'file': {
					'format': (
						'%(levelname)s [%(asctime)s] %(name)s.%(funcName)s() @%(lineno)d - '
						'%(message)s '
					),
					'datefmt': (
						'%m/%d/%Y %I:%M:%S %p'
					)
				},
				'email': {
					'format': (
						'Timestamp: %(asctime)s\nModule: %(module)s\n'
						'Line: %(lineno)d\nMessage: %(message)s'
					),
					'datefmt': (
						'%m/%d/%Y %I:%M:%S %p'
					)
				},
			},
			'loggers': {
				self.logger_name: {
					'level': 'DEBUG',
					'handlers': ['console', 'file'],
					'propagate': False
				},
			}
		}

		logging.config.dictConfig(default_log_settings)
		logging.captureWarnings(True)

		root_logger = getLogger(self.logger_name)
		root_logger.warning('Saving log file: %s' % logfile)
		root_logger.setLevel(DEBUG)
		
	def get_logger_prefix(self):
		"""
		:return: logger file name depending on where the logger gets created from
		"""

		modules = ['maya', 'nuke', 'hou', 'bpy']
		application = 'main'

		for mod in modules:
			try:
				__import__(mod)
				application = mod
				break
			except ImportError:
				application = 'launcher'
				pass

		studio = os.getenv('ARMADA_STUDIO', 'no_studio')
		site = os.getenv('ARMADA_SITE', 'no_site')
		ctime = datetime.datetime.now().strftime('%Y%m%d')
		user = getpass.getuser()

		logfilename = '{0}.{1}.{2}.{3}.{4}.{5}.'.format(ctime, self.logger_name, studio, site, user, application)

		return logfilename

	def getLogger(self, name='default'):
		"""
		:rtype:
		:param name:
		:return:
		"""

		if os.getenv('ARMADA_DEBUG', str(0)) == str(1):
			for handler in getLogger(self.logger_name).handlers:
				handler.setLevel(DEBUG)

		return logging.getLogger('{0}.{1}'.format(self.logger_name, name))

	def exception(self, message):
		logging.exception(message)


import logging
import sys
import platform


class ColorFormatter(logging.Formatter):

	BLACK = (0, 30)
	RED = (0, 31)
	LRED = (1, 31)

	GREEN = (0, 32)
	LGREEN = (1, 32)

	YELLOW = (0, 33)
	LYELLOW = (1, 33)

	BLUE = (0, 34)
	MAGENTA = (0, 35)

	CYAN = (0, 36)
	LCYAN = (1, 36)

	WHITE = (0, 37)

	COLORS = {
		'WARNING': YELLOW,
		'INFO': CYAN,
		'DEBUG': WHITE,
		'CRITICAL': MAGENTA,
		'ERROR': RED,
	}

	RESET_SEQ = "\033[0m"
	COLOR_SEQ = "\033[%d;%dm"

	def format(self, record):
		levelname = record.levelname

		text_color = self.COLOR_SEQ % self.COLORS[levelname]

		# print text_color
		message = super(ColorFormatter, self).format(record)

		color_message = []
		color_message.append(text_color)
		color_message.append(message)
		color_message.append(self.RESET_SEQ)
		color_message = "".join(color_message)

		if 'win' not in platform.platform():
			if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
				return color_message
		return message
