from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog
from gui.chat_interface3 import ChatInterface
from analysis.llm_interpreter2 import analyze_program
from analysis.radare2_analyzer import analyze_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Program Analyzer")
        self.setFixedSize(500, 700)
        self.layout = QVBoxLayout()
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file to analyze")
        if file_path:
            self.file_label.setText(f"Selected file: {file_path}")
            # For demonstration purposes, we simulate program analysis
            radare_result = analyze_file(file_path)
            analysis_result = analyze_program(radare_result)
            self.open_chat_interface(analysis_result)

    def open_chat_interface(self, analysis_result):
        self.chat_interface = ChatInterface(analysis_result, self)
        self.chat_interface.show()
