from lucidity import Template


def register():
	"""Register templates."""

	templates = [
		# User file name
		Template('shot_file_name', '{major_component}-{major_ver}.{minor_ver}.{extension}'),

		# Shot
		Template('sequences', '{@project}/{sequences}'),
		Template('sequence', '{@sequences}/{sequence}'),
		Template('shot', '{@sequence}/{shot}'),
		Template('shot_task', '{@shot}/Production/{task}'),
		Template('shot_software', '{@shot_task}/{software}'),
		Template('shot_working_dir', '{@shot_software}/{working_dir}'),
		Template('shot_major_component', ''),
		Template('shot_minor_component', '{@shot_working_dir}/{@shot_file_name}'),

		# Data paths
		Template('sequences_data', '{@project_data}/{sequences}'),
		Template('sequence_data',  '{@sequences_data}/{sequence}'),
		Template('shot_data', '{@sequence_data}/{shot}'),
		Template('shot_task_data', '{@shot_data}/{task}'),
		Template('shot_major_component_data', '{@shot_task_data}/{major_component}'),
		Template('shot_minor_component_data', '{@shot_major_component_data}/{minor_component}')
	]

	return templates
