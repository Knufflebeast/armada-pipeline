from lucidity import Template

def register():
	"""Register templates."""

	templates = [
		# User file name
		Template('asset_file_name', '{major_component}-{major_ver}.{minor_ver}.{extension}'),

		# Asset
		Template('asset_library', '{@project}/{asset_library}'),
		Template('asset_type', '{@asset_library}/{asset_type}'),
		Template('asset', '{@asset_type}/{asset}'),
		Template('asset_task', '{@asset}/Production/{task}'),
		Template('asset_software', '{@asset_task}/{software}'),
		Template('asset_working_dir', '{@asset_software}/{working_dir}'),
		Template('asset_major_component', ''),
		Template('asset_minor_component', '{@asset_working_dir}/{@asset_file_name}'),

		# Data paths
		Template('asset_library_data', '{@project_data}/{asset_library}'),
		Template('asset_type_data', '{@asset_library_data}/{asset_type}'),
		Template('asset_data', '{@asset_type_data}/{asset}'),
		Template('asset_task_data', '{@asset_data}/{task}'),
		Template('asset_major_component_data', '{@asset_task_data}/{major_component}'),
		Template('asset_minor_component_data', '{@asset_major_component_data}/{minor_component}')
	]

	return templates
