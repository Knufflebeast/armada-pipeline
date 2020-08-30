# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('./core', 'core'),
    ('./resources', 'resources'),
    ('./config_user/config.json', 'config_user'),
    ('./packages/marina', 'packages/marina'),
    ('./packages/launcher', 'packages/launcher'),
    ('./packages/atlantis', 'packages/atlantis'),
#    ('./packages/mb_tools', 'packages/mb_tools'),
    ('./utilsa', 'utilsa'),
    ('./vendor', 'vendor'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/PySide2', 'PySide2'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/shiboken2', 'shiboken2')
	('./venv/lib/python3.7/site-packages/PySide2', 'PySide2'),
	('./venv/lib/python3.7/site-packages/shiboken2', 'shiboken2'),
]

a = Analysis(['packages/launcher/main.py'],
             pathex=[
             './',
    		 './armada'
    		 ],
             binaries=[],
             datas=added_files,
             hiddenimports=[
             'logging.config',
             'Qt',
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
          [],
          exclude_binaries=True,
          name='armada_pipeline',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='armada_logo.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='armada_pipeline')
