# pyinstaller --noconfirm pyinst_windows.spec
# pyinstaller --noconfirm pyinst_macos.spec

import os
import shutil

root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
dir_name = os.path.join(root_path, 'dist', 'armada_pipeline').replace('\\', '/')

shutil.make_archive('armada_pipeline', 'zip', dir_name)
