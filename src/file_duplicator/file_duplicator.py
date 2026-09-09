import shutil
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QProgressDialog,
)
from PySide6.QtGui import (
    QAction, 
    QKeySequence, 
    QDesktopServices, 
    QTextOption,
)

from .constants import (
    HELP_TEXT, HELP_URL
)
from ._version import __version__

# import subprocess

def version():
    return "v" + __version__


class FileDuplicator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Duplicator")
        self.resize(720, 280)
        
        self.setAcceptDrops(True)
        
        self.create_menu_bar()
        self.create_status_bar()
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.init_ui()
        
    
    def set_icon(self, icon):
        self.setWindowIcon(icon)
    
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # 1) '파일(File)' 메뉴 추가
        file_menu = menu_bar.addMenu("파일(&F)") # &F는 Alt+F 단축키 활성화
        
        restart_action = QAction("초기화(&N)", self)
        restart_action.setShortcut(QKeySequence.New)
        restart_action.setStatusTip("애플리케이션을 재시작합니다.")
        restart_action.triggered.connect(self.restart_window) 
        
        exit_action = QAction("종료(&X)", self)
        exit_action.setShortcut(QKeySequence.Quit) # Ctrl+Q 등의 표준 종료 단축키 자동 지정
        exit_action.setStatusTip("애플리케이션을 종료합니다")
        exit_action.triggered.connect(self.close) # 창 닫기 기능 연결
        
        file_menu.addAction(restart_action)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("도움말(&H)")
        
        # 정보 액션 생성
        about_action = QAction("프로그램 정보(&A)", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_action.setStatusTip("정보 확인하기 - " + version())
        
        help_menu.addAction(about_action)
        
        # 정보 액션 생성
        repo_action = QAction("소스 코드 보기", self)
        repo_action.triggered.connect(lambda _=False: self.open_website(HELP_URL))
        repo_action.setStatusTip(HELP_URL)
        
        help_menu.addAction(repo_action)
    
    
    def create_status_bar(self):
        status_bar = self.statusBar()
        
        status_bar.showMessage(version())
    
        
    def restart_window(self):
        # 1. 새 창 인스턴스 생성 (전역 참조 유지 필요)
        self.new_window = FileDuplicator()
        self.new_window.show()
        
        # 2. 현재 창 닫기 및 메모리 해제
        self.close()
        self.deleteLater() 
        
    def show_about_dialog(self):
        """도움말 -> 정보 클릭 시 띄울 팝업 메시지 박스"""
        QMessageBox.about(
            self, 
            "프로그램 정보", 
            HELP_TEXT + version()
        )
    
    
    def init_ui(self):
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("복제할 파일을 드래그 앤 드랍하거나 선택하세요.")
        self.file_path.setReadOnly(True)

        browse_button = QPushButton("파일 선택")
        browse_button.clicked.connect(self.select_file)

        browse_reset_button = QPushButton("초기화")
        browse_reset_button.clicked.connect(self.reset_file)

        file_row = QHBoxLayout()
        file_row.addWidget(self.file_path)
        file_row.addWidget(browse_button)
        file_row.addWidget(browse_reset_button)

        self.prefix = QLineEdit("")
        self.prefix.setPlaceholderText("이름 앞 글자")

        self.new_name = QLineEdit("")
        self.new_name.setPlaceholderText("새로운 이름(공란 시 원본 이름)")

        self.suffix = QLineEdit(".")
        self.suffix.setPlaceholderText("이름 뒷 글자")

        name_row = QHBoxLayout()
        name_row.addWidget(self.prefix)
        name_row.addWidget(self.new_name)
        name_row.addWidget(self.suffix)

        self.start_count = QSpinBox()
        self.start_count.setRange(1, 999999)
        self.start_count.setValue(1)

        self.end_count = QSpinBox()
        self.end_count.setRange(1, 999999)
        self.end_count.setValue(50)

        self.zero_index = QSpinBox()
        self.zero_index.setRange(1, 10)
        self.zero_index.setValue(4)

        count_row = QHBoxLayout()
        count_row.addWidget(self.start_count)
        count_row.addWidget(self.end_count)
        count_row.addWidget(self.zero_index)

        self.dup_folder_path = QLineEdit()
        self.dup_folder_path.setPlaceholderText("공란일 시 원본 폴더에 복제. 폴더 드래그 앤 드랍 가능")
        self.dup_folder_path.setReadOnly(True)

        dup_browse_button = QPushButton("폴더 선택")
        dup_browse_button.clicked.connect(self.select_folder)

        dup_reset_button = QPushButton("초기화")
        dup_reset_button.clicked.connect(self.reset_folder)

        dup_file_row = QHBoxLayout()
        dup_file_row.addWidget(self.dup_folder_path)
        dup_file_row.addWidget(dup_browse_button)
        dup_file_row.addWidget(dup_reset_button)
        
        self.preview = QPlainTextEdit()
        self.preview.setPlaceholderText("-")
        self.preview.setReadOnly(True)
        self.preview.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        form = QFormLayout()
        form.addRow("복제할 파일:", file_row)
        form.addRow("이름:", name_row)
        form.addRow("번호 시작 / 종료 / 자릿수:", count_row)
        form.addRow("복제할 파일 위치:", dup_file_row)
        form.addRow("복제 파일명 미리보기:", self.preview)

        duplicate_button = QPushButton("복제 시작")
        duplicate_button.setMinimumHeight(36)
        duplicate_button.clicked.connect(self.duplicate_files)

        layout = QVBoxLayout(self.central_widget)
        layout.addLayout(form)
        layout.addWidget(self.preview)
        layout.addWidget(duplicate_button)
        
        
        self.file_path.textChanged.connect(self.update_preview)
        self.prefix.textChanged.connect(self.update_preview)
        self.new_name.textChanged.connect(self.update_preview)
        self.suffix.textChanged.connect(self.update_preview)
        self.start_count.valueChanged.connect(self.update_preview)
        self.end_count.valueChanged.connect(self.update_preview)
        self.zero_index.valueChanged.connect(self.update_preview)
        self.dup_folder_path.textChanged.connect(self.update_preview)

    def dragEnterEvent(self, event):
        # 드래그한 데이터가 URL(파일/폴더)을 포함하고 있는지 확인
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 드롭된 파일 경로 가져오기
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            path = Path(file_path)
            if path.is_file():
                # 파일일 때
                print(f"File Path: {file_path}")
                self.file_path.setText(file_path)
            elif path.is_dir():
                # 폴더일 때
                print(f"Folder Path: {file_path}")
                self.dup_folder_path.setText(file_path)
            else:
                print("경로가 존재하지 않음.")

    def reset_file(self):
        self.file_path.setText("")
        
    
    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "복제할 파일 선택",
            "",
            "All Files (*.*)",
        )
        if path:
            self.file_path.setText(path)

    def reset_folder(self):
        self.dup_folder_path.setText("")

    def select_folder(self):
        orig_path = self.file_path.text().strip()
        base_path = "" if orig_path == "" else Path(self.file_path.text().strip()).parent
        path = QFileDialog.getExistingDirectory(
            self,
            "복제할 파일이 위치할 경로 선택",
            base_path,
        )
        if path:
            self.dup_folder_path.setText(path)

    def make_name(self, source: Path, index: int) -> str:
        filename = source.stem if self.new_name.text() == "" else self.new_name.text()
        indexname = f"{index:0{self.zero_index.value()}d}"
        return f"{self.prefix.text()}{filename}{self.suffix.text()}{indexname}{source.suffix}"

    def update_preview(self):
        raw_path = self.file_path.text().strip()
        if not raw_path:
            self.preview.setPlainText("")
            return

        source = Path(raw_path)
        if not source.exists():
            self.preview.setPlainText("")
            return

        first_idx = self.start_count.value()
        last_idx = self.end_count.value()
        text = ""
        for i in range(first_idx, last_idx+1):
            text += f"{self.make_name(source, i)}"
            if not i == last_idx:
                text += "\n"
        self.preview.setPlainText(text)

    def duplicate_files(self):
        raw_path = self.file_path.text().strip()
        if not raw_path:
            QMessageBox.warning(self, "파일 미선택", "복제할 파일을 먼저 선택하세요.")
            return

        source = Path(raw_path)
        if not source.is_file():
            QMessageBox.warning(self, "파일 오류", "선택한 파일을 찾을 수 없습니다.")
            return

        start_count = self.start_count.value()
        end_count = self.end_count.value()
        count = end_count+1 - start_count
        
        if count < 1 :
            QMessageBox.about(
                self,
                "오류",
                "입력 값에 오류가 있습니다."
            )
            return

        # 복제 파일은 원본과 같은 폴더에 생성됩니다.
        destination_dir = source.parent
        if self.dup_folder_path.text() != "":
            try:
                raw_dup_path = self.dup_folder_path.text().strip()
                dup_path = Path(raw_dup_path)
                if dup_path.is_dir():
                    destination_dir = dup_path
                else:
                    destination_dir = dup_path.parent
            except:
                pass
        
        result = QMessageBox.question(
            self,
            "복제 확인",
            f"정말로 이 파일을 아래 경로에 {count}번 복제할까요?\n\n{source.name}\n\n{destination_dir}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if result != QMessageBox.Yes:
            return

        self.duplicate_file_with_dialog(
            start_count, 
            end_count, 
            destination_dir, 
            source
            )
        
        
    def duplicate_file_with_dialog(self, start_count, end_count, destination_dir, source):
        total_steps = end_count+1 - start_count

        # 2. Initialize the Progress Dialog
        progress = QProgressDialog("복제중...", "Cancel", 0, total_steps, self)
        progress.setWindowTitle("Task Progress")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        
        # Force the dialog to appear immediately (removes default 4-second delay)
        progress.setMinimumDuration(0)
        created = 0
        skipped = 0

        try:
            for i in range(start_count, end_count + 1):
                progress.setValue(i - start_count + 1)
                # Check if the user clicked the 'Cancel' button
                if progress.wasCanceled():
                    print("Task canceled by user.")
                    break
                
                filename = self.make_name(source, i)
                destination = destination_dir / filename
                
                progress.setLabelText(filename)

                # 기존 파일을 덮어쓰지 않고 건너뜁니다.
                if destination.exists():
                    skipped += 1
                    continue

                shutil.copy2(source, destination)
                created += 1
                
                # Crucial: Process UI events so the dialog stays responsive and updates
                QApplication.processEvents()
            # The dialog closes automatically when it hits 'maximum' value or gets canceled

        except Exception as exc:
            QMessageBox.critical(
                self,
                "복제 오류",
                f"복제 중 오류가 발생했습니다.\n\n"
                f"생성: {created}개\n"
                f"건너뜀: {skipped}개\n\n"
                f"{exc}",
            )
            return

        result_text = "완료"
        if progress.wasCanceled():
            result_text = "취소"
        
        QMessageBox.information(
            self,
            f"복제 {result_text}",
            f"복제가 {result_text}되었습니다.\n\n"
            f"생성: {created}개\n"
            f"이미 존재하여 건너뜀: {skipped}개",
        )
        
    def open_website(self, url):
        # Pass a QUrl object to QDesktopServices
        QDesktopServices.openUrl(QUrl(url))

