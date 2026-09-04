"""
실행법

uv 설치 후
uv run main.py
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
)
from file_duplicator import FileDuplicator
import qdarktheme

print("현재 파이썬 실행 경로:", sys.executable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    window = FileDuplicator()
    window.show()
    sys.exit(app.exec())
