from lucidity import Template


def register():
	"""Register templates."""

	templates = [
		# User file name
		Template('level_file_name', '{major_component}-{major_ver}.{minor_ver}.{extension}'),

		# Shot
		Template('levels', '{@project}/{levels}'),
		Template('level', '{@levels}/{level}'),
		Template('level_task', '{@level}/Production/{task}'),
		Template('level_software', '{@level_task}/{software}'),
		Template('level_working_dir', '{@level_software}/{working_dir}'),
		Template('level_major_component', ''),
		Template('level_minor_component', '{@level_working_dir}/{@level_file_name}'),

		# Data paths
		Template('levels_data', '{@project_data}/{levels}'),
		Template('level_data',  '{@levels_data}/{level}'),
		Template('level_task_data', '{@level_data}/{task}'),
		Template('level_major_component_data', '{@level_task_data}/{major_component}'),
		Template('level_minor_component_data', '{@level_major_component_data}/{minor_component}')

	]

	return templates
