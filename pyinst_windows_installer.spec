# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
#    ('./core', 'core'),
    ('./resources/css/setup.css', 'resources/css'),
    ('./resources/help/banner_setup.png', 'resources/help'),
    ('./resources/icon/checkbox_unchecked.svg', 'resources/icon'),
#    ('./utilsa', 'utilsa'),
#    ('./vendor', 'vendor'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/PySide2', 'PySide2'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/shiboken2', 'shiboken2')
#	('./venv/lib/python3.7/site-packages/PySide2', 'PySide2'),
#	('./venv/lib/python3.7/site-packages/shiboken2', 'shiboken2'),
]

a = Analysis(['armada_pipeline_installer.py'],
             pathex=['D:\\GitStuff\\armada-pipeline-suite-latest'],
             binaries=[],
             datas=added_files,
             hiddenimports=[
			 'Qt',
   			 'logging.config',
			 'lucidity',
    		 'PySide2.QtSvg'
			 ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
#          [],
#          exclude_binaries=True,
          name='armada_pipeline_installer',
          debug=False,
#          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          runtime_tmpdir=None,
          uac_admin=True,
          icon='armada_logo.ico')

#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=False,
#               upx=True,
#               upx_exclude=[],
#               name='armada_pipeline_installer')
