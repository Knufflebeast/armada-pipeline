
from PySide2 import QtCore


def uuid_path_from_index(*args, **kwargs):
	"""Convenience function for returning an abs path to user dir or data dir.

	Args:
		*args: index_source
		**kwargs: uuid_parents

	Returns:
		str, path
	"""
	return UuidParents().uuid_path_from_index(*args, **kwargs)

class UuidParents(object):
	"""Adds parent items to the

	Used at app startup

	"""
	def __init__(self):
		super(UuidParents, self).__init__()

	def uuid_path_from_index(self, index_source, uuid_parent=''):
		"""Builds a path of UUIDs

		Args:
			index_source: QtCore.QModelIndex
		Returns:
			str, UUID parent
		"""

		index_uuid = str(index_source.data(QtCore.Qt.UserRole))
		index_name = index_source.data(QtCore.Qt.DisplayRole)

		index_parent = index_source.parent()
		index_parent_name = index_parent.data(QtCore.Qt.DisplayRole)

		# If index has a parent, keep going up hierarchy
		if index_parent.isValid():
			# First index
			if not uuid_parent:
				uuid_parent = index_uuid
			# Indices after first
			else:
				uuid_parent = "{1} {0}".format(uuid_parent, index_uuid)

			return self.uuid_path_from_index(index_parent, uuid_parent)

		# Last index
		else:
			uuid_parent = "{1} {0}".format(uuid_parent, index_uuid)

			return uuid_parent