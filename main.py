"""
실행법

uv 설치 후
uv run main.py
"""

import os
import sys
import ctypes
import requests

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from version import Version
from file_duplicator.constants import (APP_ICON, APP_ID)
from file_duplicator.file_duplicator import FileDuplicator
import qdarktheme


print("현재 파이썬 실행 경로:", sys.executable)

#?: https://www.pythonguis.com/faq/always-the-default-icon/
# Set the app user model ID before creating QApplication (Windows only)
if sys.platform == "win32":
    myappid = APP_ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, os.path.normpath(relative_path))


def check_for_updates():
    response = requests.get(f"https://api.github.com/repos/d-dlzndi/file_duplicator/releases/latest")
    latest_version = response.json()["tag_name"].lstrip('v')
    print("latest :: ", latest_version)
    print("version :: ", Version.CURRENT)
    if Version.parse(latest_version) > Version.parse(Version.CURRENT):
        # 업데이트 알림 표시
        return response.json()
    return None

print("결과:", check_for_updates())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    print("아이콘 지정", resource_path(APP_ICON))
    # Set app-wide icon for taskbar clustering
    app.setWindowIcon(QIcon(resource_path(APP_ICON))) 
    
    window = FileDuplicator()
    window.set_icon(QIcon(resource_path(APP_ICON)))
    window.show()
    sys.exit(app.exec())
