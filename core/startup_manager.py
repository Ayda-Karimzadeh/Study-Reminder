from __future__ import annotations

import sys
from typing import Optional

_APP_NAME = "StudyReminder"
_RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_supported() -> bool:
    """Auto-start only makes sense for a packaged executable, not a dev script."""
    return sys.platform == "win32" and _get_executable_path() is not None


def is_startup_enabled() -> bool:
    if not is_supported():
        return False
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, _APP_NAME)
        return True
    except OSError:
        return False


def enable_startup() -> None:
    if not is_supported():
        return
    exe_path = _get_executable_path()
    if exe_path is None:
        return
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, _RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, _APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
    except OSError:
        pass


def disable_startup() -> None:
    if not is_supported():
        return
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, _RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, _APP_NAME)
    except OSError:
        pass


def _get_executable_path() -> Optional[str]:
    if getattr(sys, "frozen", False):
        return sys.executable
    return None
