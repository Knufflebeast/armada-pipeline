import zipfile
import stat
import subprocess
import os
zip_path = '/Applications/testzip/armada_pipeline.zip'
zip_dir = '/Applications/testzip'

zf = zipfile.ZipFile(zip_path)
# print(zf.namelist())
for file in zf.infolist():
	print(file.filename)
	f = os.path.join(zip_dir, file.filename)
	# exec("chmod u+x " + str())
	# if file.filename == 'armada_pipeline/armada_pipeline':
	# print('adsfadf')
	zf.extract(file, zip_dir)
		# f.chmod(f.stat().st_mode | stat.S_IEXEC)
	subprocess.call(['chmod', 'u+x', f])
		# st = os.stat(file_path)
		# os.chmod(file_path, st.st_mode | 0o111)
		# path = os.path.join(zip_dir, file.filename)
		# os.chmod(path, 0o775)
		# zf.extract(path)
	# zf.extract(file, zip_dir)

zf.close()
print('done')
