
from PyQt5.QtWidgets import (QVBoxLayout,QHBoxLayout,
                             QWidget,QPushButton,QFrame,QLabel,QGridLayout
                             )
from PyQt5.QtCore import QSize,Qt,pyqtSignal as Signal
from PyQt5.QtGui import QIcon

class BottomCenterLayout(QFrame):
     btn_zomm_in_signal=Signal()
     btn_zoom_out_signal=Signal()
     btn_take_photo_signal=Signal()
     btn_record_signal=Signal()

     btn_up_left_signal=Signal()
     btn_up_signal=Signal()
     btn_up_right_signal=Signal()
     btn_left_signal=Signal()
     btn_home_signal=Signal()
     btn_right_signal=Signal()
     btn_down_left_signal=Signal()
     btn_down_signal=Signal()
     btn_down_right=Signal() 
     
     btn_move_signal=Signal() 
     btn_track_signal=Signal()
     btn_auto_home_signal=Signal()
     btn_set_home_signal=Signal()

     def create_bottom_center_webcam_part(self):
          webcam_frame=QFrame()
          webcam_frame_vbox=QVBoxLayout()
          self.video=QLabel(self)
          self.device_h=''
          self.device_v=''
          self.face_center_x=''
          self.face_center_y=''
          self.cam_position=QLabel(f'H:{self.device_h}                           V:{self.device_v}')
          self.face_position=QLabel(f'X:{self.face_center_x}                           Y:{self.face_center_y}')
          self.video.setFixedSize(QSize(580,440))
          self.video.setStyleSheet('''background-color:#151c14;;
                                      border: 1px solid #2c592c;
                                      border-radius:15px; 
                                      ''')
          self.cam_position.setStyleSheet('''
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 12px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')
          self.face_position.setStyleSheet('''
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 12px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')

          webcam_frame_vbox.addWidget(self.video,alignment=Qt.AlignCenter)
          webcam_frame_vbox.addWidget(self.cam_position,alignment=Qt.AlignCenter)
          webcam_frame_vbox.addWidget(self.face_position,alignment=Qt.AlignCenter)

          webcam_frame.setLayout(webcam_frame_vbox)
          return webcam_frame
     
     def set_device_pos(self):
          self.cam_position.setText(f'H:{self.device_h}                           V:{self.device_v}')

     def set_face_pos(self):
          self.face_position.setText(f'X:{self.face_center_x}                           Y:{self.face_center_y}')
    
     def create_move_keys(self):
           move_key_grid=QGridLayout()
           move_key_widget=QWidget()
           move_key_btn_size=(35,35)
           btn_up_left=QPushButton()
           btn_up=QPushButton()
           btn_up_right=QPushButton()
           btn_left=QPushButton()
           btn_home=QPushButton()
           btn_right=QPushButton()
           btn_down_left=QPushButton()
           btn_down=QPushButton()
           btn_down_right=QPushButton()

           btn_up_left.setFixedSize(*move_key_btn_size)
           btn_up.setFixedSize(*move_key_btn_size)
           btn_up_right.setFixedSize(*move_key_btn_size)
           btn_left.setFixedSize(*move_key_btn_size)
           btn_home.setFixedSize(*move_key_btn_size)
           btn_right.setFixedSize(*move_key_btn_size)
           btn_down_left.setFixedSize(*move_key_btn_size)
           btn_down.setFixedSize(*move_key_btn_size)
           btn_down_right.setFixedSize(*move_key_btn_size)
           btn_home.setIcon(QIcon("files/styles/home.png"))
           btn_down_left.setIcon(QIcon("files/styles/down-left.png"))
           btn_down.setIcon(QIcon("files/styles/down_d.png"))
           btn_home.setIconSize(QSize(23,23))
           btn_up.setIconSize(QSize(23,23))
           btn_right.setIconSize(QSize(23,23))
           btn_left.setIconSize(QSize(23,23))
           btn_down.setIconSize(QSize(23,23))
           btn_down_right.setIcon(QIcon("files/styles/down-right.png"))
           btn_right.setIcon(QIcon("files/styles/right.png"))
           btn_left.setIcon(QIcon("files/styles/left.png"))
           btn_up.setIcon(QIcon("files/styles/top.png"))
           btn_up_left.setIcon(QIcon("files/styles/top-left.png"))
           btn_up_right.setIcon(QIcon("files/styles/top-right.png"))

           move_key_grid.addWidget(btn_up_left,0,0)
           move_key_grid.addWidget(btn_up,0,1)
           move_key_grid.addWidget(btn_up_right,0,2)
           move_key_grid.addWidget(btn_left,1,0)
           move_key_grid.addWidget(btn_home,1,1)
           move_key_grid.addWidget(btn_right,1,2)
           move_key_grid.addWidget(btn_down_left,2,0)
           move_key_grid.addWidget(btn_down,2,1)
           move_key_grid.addWidget(btn_down_right,2,2)

           btn_up_left.clicked.connect(self.up_left_btn_clicked)
           btn_up.clicked.connect(self.up_btn_clicked)
           btn_up_right.clicked.connect(self.up_right_btn_clicked)
           btn_left.clicked.connect(self.left_btn_clicked)
           btn_home.clicked.connect(self.home_btn_clicked)
           btn_right.clicked.connect(self.right_btn_clicked)
           btn_down_left.clicked.connect(self.down_left_btn_clicked)
           btn_down.clicked.connect(self.down_btn_clicked)
           btn_down_right.clicked.connect(self.down_right_btn_clicked)



           move_key_widget.setStyleSheet("""
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

           move_key_grid.setSpacing(5)
           move_key_grid.setSpacing(5)
           move_key_widget.setContentsMargins(0,0,0,0)  
           move_key_widget.setLayout(move_key_grid)
           return move_key_widget

     def create_buttom_photography(self):
         photography_hbox=QHBoxLayout()
         pohotography_widget=QWidget()
         photography_btn_size=(80,30)
         btn_zoom_in=QPushButton('Zoom in')
         btn_zoom_out=QPushButton('Zoom out')
         btn_take_photo=QPushButton('Take photo')
         self.btn_record=QPushButton('Record')
         btn_zoom_in.setFixedSize(*photography_btn_size)
         btn_zoom_out.setFixedSize(*photography_btn_size)
         btn_take_photo.setFixedSize(*photography_btn_size)
         self.btn_record.setFixedSize(*photography_btn_size)
         photography_hbox.addWidget(btn_zoom_in)
         photography_hbox.addWidget(btn_zoom_out)
         photography_hbox.addWidget(self.btn_record)
         photography_hbox.addWidget(btn_take_photo)
         btn_zoom_in.clicked.connect(self.zoom_in_btn_clicked)
         btn_zoom_out.clicked.connect(self.zoom_out_btn_clicked)
         btn_take_photo.clicked.connect(self.take_photo_btn_clicked)
         self.btn_record.clicked.connect(self.record_btn_clicked)
         pohotography_widget.setStyleSheet("""
                                                   QPushButton {
                                                        color: #e0e0e0;
                                                        background-color: #151c14;
                                                        border: 1px solid #2c592c;
                                                        border-radius: 5px;
                                                        padding: 5px 10px;
                                                        font-size: 12px;
                                                        font-family: 'Roboto';
                                                        font-weight:bold;
                                                        color:#e0e0e0;
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #2c592c;
                                                    }
                                                    QPushButton:pressed {
                                                        background-color: #2c592c;
                                                        color: black;
                                                    }
                                        """)
         pohotography_widget.setLayout(photography_hbox) 
         

         return pohotography_widget
    
     def create_type_move_key(self):
         type_move_hbox=QHBoxLayout()
         type_move_widget=QWidget()
         type_move_btn_size=(80,30)
         btn_move=QPushButton("Move")
         self.btn_track=QPushButton("Track face")
         btn_set_home=QPushButton("Set home")
         btn_auto_home=QPushButton("AutoHome")
         btn_move.setFixedSize(*type_move_btn_size)
         btn_auto_home.setFixedSize(*type_move_btn_size)
         self.btn_track.setFixedSize(*type_move_btn_size)
         btn_set_home.setFixedSize(*type_move_btn_size)
         type_move_hbox.addWidget(btn_move)
         type_move_hbox.addWidget(self.btn_track)
         type_move_hbox.addWidget(btn_auto_home)
         type_move_hbox.addWidget(btn_set_home)
         
         btn_move.clicked.connect(self.move_btn_clicked)
         self.btn_track.clicked.connect(self.track_btn_clicked)
         btn_auto_home.clicked.connect(self.auto_home_btn_clicked)
         btn_set_home.clicked.connect(self.set_home_btn_clicked)
         
         type_move_widget.setStyleSheet("""
                                                   QPushButton {
                                                        color: #e0e0e0;
                                                        background-color: #151c14;
                                                        border: 1px solid #2c592c;
                                                        border-radius: 5px;
                                                        padding: 5px 10px;
                                                        font-size: 12px;
                                                        font-family: 'Roboto';
                                                        font-weight:bold;
                                                        color:#e0e0e0;
                                                
                                        
                                                    }
                                                    QPushButton:hover {
                                                        background-color: #2c592c;
                                                    }
                                                    QPushButton:pressed {
                                                        background-color: #2c592c;
                                                        color: black;
                                                    }
                                        """)
         
         type_move_widget.setLayout(type_move_hbox)
         return type_move_widget
     
     def create_bottom_center_control_part(self):
          control_part_frame=QFrame()
          control_part_hbox=QHBoxLayout()
          control_part_hbox.addWidget(self.create_buttom_photography())
          control_part_hbox.addWidget(self.create_move_keys())
          control_part_hbox.addWidget(self.create_type_move_key())

          control_part_frame.setLayout(control_part_hbox)
          return control_part_frame     
          
     def __init__(self):
          super().__init__()
          layout=QVBoxLayout() 
          layout.addWidget(self.create_bottom_center_webcam_part())
          layout.addWidget(self.create_bottom_center_control_part())
          layout.setStretch(0,30)
          layout.setStretch(1,1)
          layout.setContentsMargins(0,0,0,0)
          layout.setSpacing(0)
          self.setLayout(layout)
          self.setStyleSheet("background-color:#161616;")


     def zoom_in_btn_clicked(self):
         self.btn_zomm_in_signal.emit()
     def zoom_out_btn_clicked(self):
         self.btn_zoom_out_signal.emit()
     def take_photo_btn_clicked(self):
         self.btn_take_photo_signal.emit()
     def record_btn_clicked(self):
         self.btn_record_signal.emit()        

     def up_left_btn_clicked(self):
         self.btn_up_left_signal.emit()
     def up_btn_clicked(self):
         self.btn_up_signal.emit()
     def up_right_btn_clicked(self):
         self.btn_up_right_signal.emit()
     def left_btn_clicked(self):
         self.btn_left_signal.emit()
     def home_btn_clicked(self):
          self.btn_home_signal.emit()
     def right_btn_clicked(self):
         self.btn_right_signal.emit()
     def down_left_btn_clicked(self):
         self.btn_down_left_signal.emit()
     def down_btn_clicked(self):
         self.btn_down_signal.emit()
     def down_right_btn_clicked(self):
         self.btn_down_right.emit()

     def move_btn_clicked(self):
        self.btn_move_signal.emit()
     def track_btn_clicked(self):
        self.btn_track_signal.emit()
     def auto_home_btn_clicked(self):
        self.btn_auto_home_signal.emit() 
     def set_home_btn_clicked(self):
          self.btn_set_home_signal.emit()
          


     



