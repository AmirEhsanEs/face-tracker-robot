import sys
from PyQt5.QtWidgets import QFrame,QVBoxLayout ,QLabel

class SpeedLayout(QFrame):

     def __init__(self):
        super().__init__()
        main_vbox=QVBoxLayout()
        content_label=QLabel("speed layout")
        content_label.setStyleSheet("color:white;")
        main_vbox.addWidget(content_label)
        self.setLayout(main_vbox)
        self.setVisible(False)
