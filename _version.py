from datetime import datetime

now = datetime.now()
phase = 'beta'
__version__ = '%Y.%m.%d-{0}.%H'.format(phase)
