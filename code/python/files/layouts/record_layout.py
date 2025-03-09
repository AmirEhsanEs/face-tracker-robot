from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QWidget, QMenu, QAction, QLineEdit,
                             QPushButton, QStyle, QSlider, QHBoxLayout, QSizePolicy,QDialog,QSpacerItem)
from PyQt5.QtCore import Qt, QUrl,QPoint
from PyQt5.QtGui import QPalette,QIcon,QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from files.watchdog.list_handler import ListHandler
from PyQt5.QtCore import QTimer,QSize

import os
import re

from files.dialogs.error_dialog import ErrorDialog

def natural_key(string):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', string)]


class RecordLayout(QFrame):
    def __init__(self):
        super().__init__()
        main_vbox = QVBoxLayout()

        self.record_directory = 'records'
        self.record_vbox = QVBoxLayout()  

        self.load_records()
        self.setStyleSheet('''color:white;
                             ''')
        main_vbox.addLayout(self.record_vbox)
        main_vbox.addStretch()

        self.setLayout(main_vbox)
        self.setVisible(False)

        main_vbox.setContentsMargins(4,2,4,0)
        main_vbox.setSpacing(3)
        self.setup_file_watcher()
        self.rename_editor = None
        self.rename_item_index = None
        self.rename_in_progress = False
        self.mediaPlayer = None
        self.current_file = None

    def load_records(self):
        try:
            for i in reversed(range(self.record_vbox.count())):
                widget = self.record_vbox.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            record_files = sorted(os.listdir(self.record_directory), key=natural_key)  
            for file_name in record_files:
                file_path = os.path.join(self.record_directory, file_name)
                if os.path.isfile(file_path):
                    self.add_record(file_name)

        except FileNotFoundError:
            if not os.path.exists(self.record_directory):
                os.makedirs(self.record_directory)
            error_dialog=ErrorDialog(f'Directory {self.record_directory} not found, it is created!!')
            error_dialog.exec_() 
    def add_record(self, file_name):
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
        
        record_widget = QWidget()
        record_widget.setStyleSheet('''background-color:#161616;
                                    border-radius:3px;                              
                                    ''')
        record_widget.setFixedHeight(34)
        hbox.setContentsMargins(10, 0, 0, 0)
        record_widget.setLayout(hbox)
        
        record_widget.mouseDoubleClickEvent = lambda event: self.show_item(file_name)
        record_widget.setContextMenuPolicy(Qt.CustomContextMenu)

        record_widget.enterEvent = lambda event: self.on_hover(record_widget)
        record_widget.leaveEvent = lambda event: self.on_leave(record_widget)

        self.record_vbox.addWidget(record_widget)

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
                margin: 5px 0;
            }
        """)

        context_menu.exec_(button.mapToGlobal(QPoint(0, button.height())))

    def confirm_delete_item(self, file_name):
        if self.current_file == file_name:
            self.stop_media_player()

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
            file_path = os.path.join(self.record_directory, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.load_records()
                except PermissionError as e:
                    error_dialog=ErrorDialog(f'Could not delete file: {e}')
                    error_dialog.exec_() 
            else:
                error_dialog=ErrorDialog(f'File "{file_path}" not found')
                error_dialog.exec_() 

    def show_item(self, file_name):
        file_path = os.path.join(self.record_directory, file_name)
        if os.path.exists(file_path):
            self.create_media_layout(file_name)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.playBtn.setEnabled(True)
            self.mediaPlayer.play()
            self.current_file = file_name
        else:
            error_dialog=ErrorDialog(f'File "{file_name}" not found')
            error_dialog.exec_() 

    def stop_media_player(self):
        if self.mediaPlayer:
            if self.mediaPlayer.state() != QMediaPlayer.StoppedState:
                self.mediaPlayer.stop()
            self.mediaPlayer.setMedia(QMediaContent())  # Release the file
            self.current_file = None

    def setup_file_watcher(self):
        self.event_handler = ListHandler(self.record_directory)
        self.event_handler.update_signal.connect(self.load_records)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.record_directory, recursive=False)
        self.observer.start()


    def create_media_layout(self,file_name):
        self.media_widget = QWidget()
        self.media_widget.setWindowTitle(file_name)
        self.media_widget.setGeometry(350, 100, 580, 400)

        p = self.media_widget.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.media_widget.setPalette(p)

        self.init_media_layout()
        self.media_widget.show()

        self.media_widget.destroyed.connect(self.on_media_widget_destroyed)

    def on_media_widget_destroyed(self):
        if self.mediaPlayer:
            self.mediaPlayer.stop()
            self.mediaPlayer.setMedia(QMediaContent())
            self.mediaPlayer.deleteLater()
            self.mediaPlayer = None

    def init_media_layout(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()
        videowidget.setFixedWidth(580)
        videowidget.setFixedHeight(440)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(QIcon('files/styles/play.png'))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.media_widget.setStyleSheet("""
                QWidget {
                    background-color: #050404;
                    color: #ffffff;
                }
                
                QVideoWidget {
                    background-color: #000000;
                }

                QPushButton {
                    background-color: #1a171c;
                    border: 1px solid black;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:enabled:hover {
                    background-color: #565656;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }

                QPushButton::icon {
                    color: white;
                }

                QSlider::groove:horizontal {
                    border: 1px solid #444;
                    height: 8px;
                    background: #2c592c;
                    border-radius: 4px;
                }

                QSlider::handle:horizontal {
                    background: #2c592c;
                    border: 1px solid #444;
                    width: 14px;
                    margin: -4px 0;
                    border-radius: 7px;
                }

                QSlider::sub-page:horizontal {
                    background: #2c592c;
                    border-radius: 4px;
                }

                QSlider::add-page:horizontal {
                    background: #555555;
                    border-radius: 4px;
                }
            """)


        hboxLayout = QHBoxLayout()
        btn_widget=QWidget()
        hboxLayout.setContentsMargins(10, 0, 6, 8)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        vboxLayout = QVBoxLayout()
        btn_widget.setFixedWidth(580)
        btn_widget.setLayout(hboxLayout)
        vboxLayout.addWidget(videowidget)
        vboxLayout.addWidget(btn_widget)
        vboxLayout.setContentsMargins(0,0,0,0)

         
        self.media_widget.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(QIcon('files/styles/stop.png'))
            self.playBtn.setIconSize(QSize(12, 12))

        else:
            self.playBtn.setIcon(QIcon('files/styles/play.png'))
            self.playBtn.setIconSize(QSize(12, 12))


    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def toggle_fullscreen(self):
        if self.media_widget.isFullScreen():
            self.media_widget.showNormal()
        else:
            self.media_widget.showFullScreen()
