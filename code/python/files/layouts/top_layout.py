from PyQt5.QtWidgets import (QHBoxLayout,QPushButton,QFrame,QLabel )
from PyQt5.QtCore import QSize,pyqtSignal as Signal
from PyQt5.QtGui import QPixmap,QIcon

class TopLayout(QFrame):
     btn_camera_connect_signal=Signal()
     btn_device_connect_signal=Signal()
     btn_restart_signal=Signal()
     def __init__(self):
        super().__init__()
        navbar_hbox=QHBoxLayout()
        logo_label=QLabel()
        self.camera_connection_btn=QPushButton()
        self.device_connection_btn=QPushButton()
        self.restart_connection_btn=QPushButton()
        self.camera_connection_btn.setFixedSize(40,30)
        self.device_connection_btn.setFixedSize(40,30)
        self.restart_connection_btn.setFixedSize(40,30)
        self.camera_connection_btn.setIcon(QIcon('files/styles/camera.png'))
        self.camera_connection_btn.setIconSize(QSize(40,30))
                                        
        self.device_connection_btn.setIcon(QIcon('files/styles/micro.png'))
        self.device_connection_btn.setIconSize(QSize(40,30))

        self.restart_connection_btn.setIcon(QIcon('files/styles/restart.png'))
        self.restart_connection_btn.setIconSize(QSize(40,30))
        self.setStyleSheet("border: 1px solid black; background-color:#161616")
        logo_label.setStyleSheet("border:none")
        self.camera_connection_btn.setStyleSheet("""QPushButton {
                                                background-color: #2b2b2b;
                                                border: 1px solid black; 
                                                font-size: 20px;
                                                font-weight: bold;
                                                border-radius:10px
                                            }
                                            QPushButton:hover {
                                                border: 1px solid black; 
                                                background-color: #2c592c;
                                            }
                                        """)
        self.device_connection_btn.setStyleSheet("""QPushButton {
                                                background-color: #2b2b2b;
                                                border: 1px solid black; 
                                                font-size: 20px;
                                                font-weight: bold;
                                                border-radius:10px
                                            }
                                            QPushButton:hover {
                                                border: 1px solid black; 
                                                background-color: #2c592c;
                                            }
                                        """)
        self.restart_connection_btn.setStyleSheet("""QPushButton {
                                                background-color: #2b2b2b;
                                                border: 1px solid black; 
                                                font-size: 20px;
                                                font-weight: bold;
                                                border-radius:10px
                                            }
                                            QPushButton:hover {
                                                border: 1px solid black; 
                                                background-color: #2c592c;
                                            }
                                        """)

        pixmap=QPixmap('files/styles/etracker.png')
        logo_label.setPixmap(pixmap)
        navbar_hbox.addWidget(logo_label)
        self.setLayout(navbar_hbox)
        navbar_hbox.addWidget(self.camera_connection_btn)
        navbar_hbox.addWidget(self.device_connection_btn)
        navbar_hbox.addWidget(self.restart_connection_btn)
        self.camera_connection_btn.clicked.connect(self.click_camera_connection_button)
        self.device_connection_btn.clicked.connect(self.click_device_connection_button)
        self.restart_connection_btn.clicked.connect(self.click_restart_button)

     def click_camera_connection_button(self):
         self.btn_camera_connect_signal.emit()

     def click_device_connection_button(self):
         self.btn_device_connect_signal.emit()

     def click_restart_button(self):
         self.btn_restart_signal.emit()         

