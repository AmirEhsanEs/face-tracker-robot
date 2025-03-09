import sys
import os
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QWidget, QMenu, QAction, QPushButton, 
                             QHBoxLayout, QSizePolicy,QDialog)
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtGui import QPalette, QPixmap,QIcon
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from files.watchdog.list_handler import ListHandler
import re
from files.dialogs.error_dialog import ErrorDialog

def natural_key(string):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', string)]

class SnapshotLayout(QWidget):

    def __init__(self):
        super().__init__()
        main_vbox = QVBoxLayout()
        self.snapshots_directory = 'snapshots'
        self.record_vbox = QVBoxLayout()
        
        self.snapshots_files = []  
        self.current_index = 0  

        self.load_snapshots()
        self.setStyleSheet("color:white;")     
        main_vbox.addLayout(self.record_vbox)
        main_vbox.addStretch()

        self.setLayout(main_vbox)
        self.setVisible(False)

        main_vbox.setContentsMargins(4,2,4,0)
        main_vbox.setSpacing(4)
        self.setup_file_watcher()
        self.image_widget = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def load_snapshots(self):
        try:
            for i in reversed(range(self.record_vbox.count())):
                widget = self.record_vbox.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.snapshots_files = sorted(os.listdir(self.snapshots_directory), key=natural_key)
            for file_name in self.snapshots_files:
                file_path = os.path.join(self.snapshots_directory, file_name)
                if os.path.isfile(file_path):
                    self.add_snapshot(file_name)
        except FileNotFoundError:
            if not os.path.exists(self.snapshots_directory):
                os.makedirs(self.snapshots_directory)
            error_dialog=ErrorDialog(f'Directory {self.snapshots_directory} not found, it is created!!')
            error_dialog.exec_() 


    def add_snapshot(self, file_name):
        hbox = QHBoxLayout()
        label = QLabel(file_name)
        label.setStyleSheet('''
                            font-family: 'Roboto';
                            font-size: 11px;
                            color:#e0e0e0;
                            font-weight:normal;''')
        hbox.addWidget(label)
        btn = QPushButton("⋮")
        btn.setFixedSize(25, 25)
        btn.setStyleSheet('''background-color: transparent; 
                            border: none; 
                            font-family: 'Roboto';
                            font-size: 30px;
                            color:#e0e0e0;
                            font-weight:normal;''')
        btn.clicked.connect(lambda: self.show_context_menu(btn, file_name))
        hbox.addWidget(btn)

        snapshot_widget = QWidget()
        snapshot_widget.setStyleSheet('''background-color:#161616;
                                       border-radius:3px
                                      ''')
        snapshot_widget.setFixedHeight(30)
        hbox.setContentsMargins(10,0,0,0)
        snapshot_widget.setLayout(hbox)
        snapshot_widget.mouseDoubleClickEvent = lambda event: self.show_item(file_name)
        snapshot_widget.enterEvent = lambda event: self.on_hover(snapshot_widget)
        snapshot_widget.leaveEvent = lambda event: self.on_leave(snapshot_widget)
        self.record_vbox.addWidget(snapshot_widget)

    def on_hover(self, widget):
        widget.setStyleSheet('''background-color:#565656;
                                border-radius:3px;                              
                            ''')

    def on_leave(self, widget):
        widget.setStyleSheet('''background-color:#161616;
                                border-radius:3px;                              
                            ''')    

    def show_context_menu(self, button, file_name):
        context_menu = QMenu(self)
        show_action = QAction("Show")
        delete_action = QAction("Delete")

        show_action.triggered.connect(lambda: self.show_item(file_name))
        delete_action.triggered.connect(lambda: self.confirm_delete_item(file_name))

        context_menu.setStyleSheet("color:white;")
        context_menu.addAction(show_action)
        context_menu.addAction(delete_action)
        context_menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;  
                color: #e0e0e0; 
                border: 1px solid #5a5a5a;
                border-radius: 5px;  
            }
            QMenu::item {
                padding: 8px 20px;  
                background-color: transparent;
                border:none;  
            }
            QMenu::item:selected { 
                background-color: #2c592c;
                color: #e0e0e0; 
            }
            QMenu::separator {
                height: 1px;
                background: #5a5a5a;  
                margin: 5px 0.
            }
        """)

        context_menu.exec_(button.mapToGlobal(QPoint(0, button.height())))

    def confirm_delete_item(self, file_name):
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Delete")
        dialog.setFixedSize(400, 150)  
        dialog.setStyleSheet("""
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
                font-size: 14px;
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

        icon_label = QLabel(dialog)
        pixmap = QPixmap("files/styles/question.png")  
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(50, 54) 
        
        label = QLabel(f'Are you sure you want to delete "{file_name}"?', dialog)
        label.setWordWrap(True)
        label.adjustSize()

        yes_button = QPushButton("Yes", dialog)
        no_button = QPushButton("No", dialog)
        yes_button.setFixedSize(120, 30)
        no_button.setFixedSize(120, 30)
        yes_button.clicked.connect(lambda: (self.delete_item(file_name), dialog.accept()))
        no_button.clicked.connect(dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout = QVBoxLayout()
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0,5,0,0)
        icon_layout.addWidget(icon_label)
        icon_text_layout = QHBoxLayout()
        icon_text_layout.addLayout(icon_layout)
        icon_text_layout.addWidget(label)
        layout.addLayout(icon_text_layout)
        icon_text_layout.setContentsMargins(18,10,20,0)
                  
        layout.addStretch()
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def delete_item(self, file_name):
        file_path = os.path.join(self.snapshots_directory, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            if self.image_widget:
                self.image_widget.destroy()
            self.load_snapshots() 
        else:
            error_dialog=ErrorDialog(f'File "{file_name}" not found')
            error_dialog.exec_() 


    def show_item(self, file_name):
        file_path = os.path.join(self.snapshots_directory, file_name)
        if os.path.exists(file_path):
            self.current_index = self.snapshots_files.index(file_name)
            self.create_image_layout(file_path,file_name)
        else:
            error_dialog=ErrorDialog(f'File "{file_name}" not found')
            error_dialog.exec_() 

    def create_image_layout(self, file_path,filename):
        self.image_widget = QWidget()
        self.image_widget.setWindowTitle(filename)
        self.image_widget.setGeometry(350, 100, 580, 440)  

        p = self.image_widget.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.image_widget.setPalette(p)

        vboxLayout = QVBoxLayout()

        self.image_label = QLabel(self.image_widget)
        self.image_label.setFixedSize(580, 440)  
        self.pixmap = QPixmap(file_path)
        self.image_label.setPixmap(self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        vboxLayout.addWidget(self.image_label)
        vboxLayout.setContentsMargins(0, 0, 0, 0) 

        hbox = QHBoxLayout()

        prev_button = QPushButton()
        next_button = QPushButton()

        prev_button.setFixedWidth(60)
        next_button.setFixedWidth(60)

        prev_button.setIcon(QIcon("files/styles/prev.png"))
        next_button.setIcon(QIcon("files/styles/next.png"))

        prev_button.clicked.connect(self.show_previous_image)
        next_button.clicked.connect(self.show_next_image)

        button_style = """
            QPushButton {
                background-color: #1a171c;
                color: #e0e0e0;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #565656;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """
        prev_button.setStyleSheet(button_style)
        next_button.setStyleSheet(button_style)

        hbox.addWidget(prev_button)
        hbox.addWidget(next_button)

        hbox.setContentsMargins(0, 5, 0, 10)
        hbox.setSpacing(0)

        vboxLayout.addLayout(hbox)

        self.image_widget.setLayout(vboxLayout)
        self.image_widget.show()


    def update_image(self,filename):
      scaled_pixmap = self.pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
      self.image_label.setPixmap(scaled_pixmap)
      self.image_widget.setWindowTitle(filename)


    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            file_name = self.snapshots_files[self.current_index]
            file_path = os.path.join(self.snapshots_directory, file_name)
            self.pixmap = QPixmap(file_path)
            self.update_image(file_name)

    def show_next_image(self):
        if self.current_index < len(self.snapshots_files) - 1:
            self.current_index += 1
            file_name = self.snapshots_files[self.current_index]
            file_path = os.path.join(self.snapshots_directory, file_name)
            self.pixmap = QPixmap(file_path)
            self.update_image(file_name)

    def setup_file_watcher(self):
        self.event_handler = ListHandler(self.snapshots_directory)
        self.event_handler.update_signal.connect(self.load_snapshots)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.snapshots_directory, recursive=False)
        self.observer.start()
