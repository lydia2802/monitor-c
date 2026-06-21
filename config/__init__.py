import os as _os
import shutil as _shutil

# Auto-create api_config.py from the example file on first run
# so the app works out-of-the-box without manual setup
_dir = _os.path.dirname(__file__)
_dst = _os.path.join(_dir, "api_config.py")
_src = _os.path.join(_dir, "api_config.example.py")

if not _os.path.exists(_dst) and _os.path.exists(_src):
    _shutil.copy2(_src, _dst)
