# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('./core', 'core'),
    ('./resources', 'resources'),
#    ('./config_user/config.json', 'config_user'),
#    ('./logs', 'logs' ),
    ('./packages/marina', 'packages/marina'),
    ('./packages/launcher', 'packages/launcher'),
    ('./packages/atlantis', 'packages/atlantis'),
#    ('./packages/mb_tools', 'packages/mb_tools'),
    ('./utilsa', 'utilsa'),
    ('./vendor', 'vendor'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/PySide2', 'PySide2'),
#    ('c:/hostedtoolcache/windows/python/3.7.7/x64/lib/site-packages/shiboken2', 'shiboken2')
	('./venv/Lib/site-packages/PySide2', 'PySide2'),
	('./venv/Lib/site-packages/shiboken2', 'shiboken2'),
]
a = Analysis(['./packages/launcher/main.py'],
    pathex=[
    './',
    './core',
    './packages',
    './vendor/Qt.py',
    './vendor/lucidity/source',
    './vendor/watchdog/src'
#    'D:\\GitStuff\\mb-armada\\venv\\Lib\\site-packages'
#    'C:\\Users\\borbs\\Miniconda3\\envs\\mb-armada\\Lib\\site-packages',
    ],
    binaries=[],
    datas=added_files,
    hiddenimports=[
    'mb_utils.hooks.launchers.maya_hook',
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

###### include mydir in distribution #######
#def extra_datas(mydir):
#    def rec_glob(p, files):
#        import os
#        import glob
#        for d in glob.glob(p):
#            if os.path.isfile(d) and d.endswith('.pyc'):
#                files.append(d)
#            rec_glob("%s/*" % d, files)
#    files = []
#    rec_glob("%s/*" % mydir, files)
#    extra_datas = []
#    for f in files:
#        extra_datas.append((f, f, 'DATA'))
#
#    return extra_datas
#
## append the 'data' dir
#a.datas += extra_datas('source')
#a.datas += extra_datas('packages')
#a.datas += extra_datas('mb_utils')
############################################

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
          manifest=None,
#          uac_admin=True,
          icon='armada_logo.ico')
#          # For --onefile bundle
#          a.scripts,
#          a.binaries,
#          a.zipfiles,
#          a.datas,
#          [],
#          name='armada_pipeline',
#          debug=False,
#          bootloader_ignore_signals=False,
#          strip=False,
#          upx=True,
#          upx_exclude=[],
#          runtime_tmpdir=None,
#          console=True,
#          icon='armada_logo.ico')


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='armada_pipeline')