"""
실행법

uv 설치 후
uv run main.py
"""

import os
import sys
import ctypes

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

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
