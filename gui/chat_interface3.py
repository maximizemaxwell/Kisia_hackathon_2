from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QHBoxLayout, QScrollArea
from analysis.llm_interpreter2 import ask_llm


class ChatInterface(QDialog):
    def __init__(self, analysis_result, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Chat Interface")
        self.setFixedSize(1000, 1200)
        self.layout = QVBoxLayout()

        self.chat_history_layout = QVBoxLayout()
        self.chat_widget = QWidget()
        self.chat_widget.setLayout(self.chat_history_layout)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setWidget(self.chat_widget)
        self.layout.addWidget(self.chat_scroll)

        self.analysis_label = QLabel("Analysis Result:")
        self.analysis_label.setStyleSheet("font-weight: bold; color: #555555;")
        self.layout.addWidget(self.analysis_label)

        # 첫 번째 분석 결과를 추가
        self.chat_history = [f"Analysis: {analysis_result}"]  # 초기 분석 결과를 대화 내역에 추가
        self.add_message(self.chat_history[-1], "assistant")

        self.question_entry = QLineEdit()
        self.question_entry.setPlaceholderText("Ask a question about the analysis...")
        self.question_entry.setStyleSheet("padding: 16px; font-size: 24px;")
        self.layout.addWidget(self.question_entry)

        self.ask_button = QPushButton("Send")
        self.ask_button.setStyleSheet("""
            background-color: #007BFF; color: white; padding: 15px;
            border-radius: 10px; font-size: 18px; font-weight: bold;
        """)
        self.ask_button.clicked.connect(self.ask_gpt)
        self.layout.addWidget(self.ask_button)

        self.setLayout(self.layout)

    def add_message(self, message, sender):
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            background-color: #E0E0E0; padding: 10px; border-radius: 10px;
            font-size: 18px;
        """)

        message_layout = QHBoxLayout()

        if sender == "user":
            message_label.setStyleSheet("""
                background-color: #007BFF; color: white; padding: 10px; border-radius: 10px;
                font-size: 18px;
            """)
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_label.setStyleSheet("""
                background-color: #E0E0E0; padding: 10px; border-radius: 10px;
                font-size: 18px;
            """)
            message_layout.addWidget(message_label)
            message_layout.addStretch()

        self.chat_history_layout.addLayout(message_layout)
        self.chat_scroll.verticalScrollBar().setValue(self.chat_scroll.verticalScrollBar().maximum())

    def ask_gpt(self):
        question = self.question_entry.text()
        if question:
            self.add_message(f"User: {question}", "user")
            self.chat_history.append(f"User: {question}")

            # 이전 대화 내역을 포함하여 질문을 전달
            answer = ask_llm(self.chat_history)
            self.chat_history.append(f"Assistant: {answer}")
            self.add_message(f"Assistant: {answer}", "assistant")
            self.question_entry.clear()


