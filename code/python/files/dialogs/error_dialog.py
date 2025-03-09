from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ErrorDialog(QDialog):
    def __init__(self, error_message):
        super().__init__()
        self.setWindowTitle("Error")
        self.setFixedSize(350, 130)
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #e0e0e0;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                color: #e0e0e0;
                background-color: #121212;   
                font-family: 'Roboto';
                font-size: 12px;
                font-weight: 500;
                padding-bottom: 5px;
            }
            QPushButton {
                background-color: #2c592c;
                color: #e0e0e0;
                font-family: 'Roboto';
                border: 1px solid #252525;
                border-radius: 6px;
                padding: 8px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2c592c;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #2c592c;
            }
            QPushButton:disabled {
                background-color: #444;
                color: #777;
                border: 1px solid #555;
            }
        """)

        icon_label = QLabel(self)
        pixmap = QPixmap("files/styles/error.png") 
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(50, 54)

        label = QLabel(error_message, self)
        label.setWordWrap(True)
        label.adjustSize()

        ok_button = QPushButton("OK", self)
        ok_button.setFixedSize(120, 30)
        ok_button.clicked.connect(self.accept)  

        layout = QVBoxLayout()
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0, 5, 0, 0)
        icon_layout.addWidget(icon_label)

        icon_text_layout = QHBoxLayout()
        icon_text_layout.addLayout(icon_layout)
        icon_text_layout.addWidget(label)
        icon_text_layout.setStretch(0,5)
        icon_text_layout.setStretch(1,0)
        icon_text_layout.setSpacing(21)

        icon_text_layout.setContentsMargins(10, 10, 0, 0)  

        icon_text_container = QVBoxLayout()
        icon_text_container.addLayout(icon_text_layout)
        icon_text_container.setAlignment(icon_text_layout, Qt.AlignHCenter)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addStretch()

        layout.addLayout(icon_text_container)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)
