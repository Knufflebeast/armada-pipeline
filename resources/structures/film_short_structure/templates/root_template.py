from lucidity import Template


def register():
	"""Register templates."""

	templates = [

		# User paths
		Template('pipeline_root', '{pipeline_root}'),
		Template('client', '{@pipeline_root}/{client}'),
		Template('project', '{@client}/{project}'),

		# Data paths
		Template('pipeline_root_data', '{pipeline_root}'),
		Template('client_data', '{@pipeline_root_data}/{client}'),
		Template('project_data', '{@client_data}/{project}'),
		]

	return templates
