from PyQt5.QtWidgets import (QVBoxLayout,QHBoxLayout,
                             QPushButton,QLabel,
                             QDialog,QLineEdit,QFormLayout,QGridLayout)
from PyQt5.QtCore import Qt
class CameraConnectDialog(QDialog):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
          self.setFixedSize(280, 120)
          self.setWindowTitle("Camera Connection")
          
          vbox_layout = QVBoxLayout(self)
          vbox_layout.setAlignment(Qt.AlignCenter)
          self.inputs = []
          
          form = QFormLayout()
          
          label_1 = QLabel("IP:")
          line_edit1 = QLineEdit(self)
          form.addRow(label_1, line_edit1)
          
          label_2 = QLabel("Port:")
          line_edit2 = QLineEdit(self)
          form.addRow(label_2, line_edit2)
          line_edit2.setFixedWidth(50)
          
          self.inputs.append(line_edit1)
          self.inputs.append(line_edit2)
          
          vbox_layout.addLayout(form)
          vbox_layout.setStretch(0, 5)
          vbox_layout.setStretch(1, 2)
          
          button_layout = QHBoxLayout()
          btn_connect = QPushButton("Connect", self)
          btn_cancel = QPushButton("Cancel", self)
          button_layout.addWidget(btn_connect)
          button_layout.addWidget(btn_cancel)
          
          vbox_layout.addLayout(button_layout)

          btn_connect.clicked.connect(self.click_connect)
          btn_cancel.clicked.connect(self.reject)

          self.setStyleSheet("""
              QDialog {
                  background-color: #121212;
                  border-radius: 10px;
              }
              QLabel {
                  color: #e0e0e0;
                  font-family: 'Roboto';
                  font-size: 12px;
                  font-weight: 300;
              }
              QLineEdit {
                  background-color: #2b2b2b;
                  color: white;
                  border-radius: 5px;
                  padding: 5px;
              }
              QLineEdit:focus {
                  border: 1px solid #2c592c;
              }
              QPushButton {
                  color: #e0e0e0;
                  background-color: #2c592c;
                  border: 1px solid #2c592c;
                  border-radius: 5px;
                  padding: 5px 10px;
                  font-size: 11px;
              }
              QPushButton:hover {
                  background-color: #2c592c;
              }
              QPushButton:pressed {
                  background-color: #2c592c;
                  color: black;
              }
          """)
    
     def click_connect(self):
         self.ip = self.inputs[0].text()
         self.port = self.inputs[1].text()
         self.url = 'http://' + self.ip + ':' + self.port
         self.done(QDialog.Accepted)
                 

class  CameraConnectionInfo(QDialog):
    def __init__(self, ip, port, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setFixedSize(280, 120)
        self.setWindowTitle("Device Connection")
        
        vbox_layout = QVBoxLayout(self)
        vbox_layout.setAlignment(Qt.AlignCenter)
        
        grid_layout = QGridLayout()
        
        label_1 = QLabel("IP:")
        label_1.setStyleSheet("padding-left:6px; padding-top:7px")

        label_1.setAlignment(Qt.AlignLeft)
        label_1_info = QLabel(self.ip)
        label_1_info.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_1, 0, 0)
        grid_layout.addWidget(label_1_info, 0, 1)
        
        label_2 = QLabel("Port:")
        label_2.setStyleSheet("padding-left:6px; padding-top:6px")

        label_2.setAlignment(Qt.AlignLeft)
        label_2_info = QLabel(self.port)
        label_2_info.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_2, 1, 0)
        grid_layout.addWidget(label_2_info, 1, 1)
        
        vbox_layout.addLayout(grid_layout)
        vbox_layout.setStretch(0, 2)
        vbox_layout.setStretch(1, 1)
        vbox_layout.setContentsMargins(0, 15, 0, 15)
        
        button_layout = QHBoxLayout()
        btn_connect = QPushButton("Disconnect", self)
        btn_cancel = QPushButton("Cancel", self)
        btn_connect.setFixedWidth(80)
        btn_cancel.setFixedWidth(80)
        
        button_layout.addWidget(btn_connect)
        button_layout.addWidget(btn_cancel)
        
        vbox_layout.addLayout(button_layout)
        
        btn_connect.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                border-radius: 10px;
            }
            QLabel {
                  color: #e0e0e0;
                  font-family: 'Roboto';
                  font-size: 12px;
                  font-weight: 300;
            }
            QPushButton {
                color: white;
                background-color: #2c592c;
                border: 1px solid #2c592c;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2c592c;
            }
            QPushButton:pressed {
                background-color: #2c592c;
                color: black;
            }
        """)

