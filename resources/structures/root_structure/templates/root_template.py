from lucidity import Template


def register():
	"""Register templates."""

	templates = [

		# User paths
		Template('workspace', '{workspace}'),
		Template('project', '{@workspace}/{project}'),

		# Data paths
		Template('workspace_data', '{workspace}'),
		Template('project_data', '{@workspace_data}/{project}'),
		]

	return templates
