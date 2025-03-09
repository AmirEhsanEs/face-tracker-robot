
from PyQt5.QtWidgets import (QVBoxLayout,QFrame,QLabel,QScrollArea,QWidget,QHBoxLayout
                             )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent,QPixmap

from files.layouts.setting_layout import SettingLayout
from files.layouts.snapshot_layout import SnapshotLayout
from files.layouts.record_layout import RecordLayout


from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QScrollArea, QLabel, QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as Signal,pyqtSlot as Slot,Qt

class BottomRightLayout(QWidget):
    motor_enable_signal=Signal(int)
    accel_enable_signal=Signal(int)
    auto_track_signal=Signal(int)
    hand_detect_signal=Signal(int)
    mode_signal=Signal(int)
    move_increment_signal=Signal(float)
    horizontal_speed_signal=Signal(float)
    vertical_speed_signal=Signal(float)
    horizontal_accel_signal=Signal(float)
    vertical_accel_signal=Signal(float)
    
    def __init__(self,setting):
        super().__init__()
        self.setting=setting
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        scroll_vbox = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_vbox)

        setting_vbox = QVBoxLayout()
        self.create_setting_btn()
        self.setting_layout = SettingLayout(self.setting)
        self.setting_layout.motor_enable_signal.connect(self.motor_enable_signal)
        self.setting_layout.accel_enable_signal.connect(self.accel_enable_signal)
        self.setting_layout.auto_track_signal.connect(self.auto_track_signal)
        self.setting_layout.hand_detect_signal.connect(self.hand_detect_signal)
        self.setting_layout.mode_signal.connect(self.mode_signal)
        self.setting_layout.move_increment_signal.connect(self.move_increment_signal)
        self.setting_layout.horizontal_speed_signal.connect(self.horizontal_speed_signal)
        self.setting_layout.vertical_speed_signal.connect(self.vertical_speed_signal)
        self.setting_layout.horizontal_accel_signal.connect(self.horizontal_accel_signal)
        self.setting_layout.vertical_accel_signal.connect(self.vertical_accel_signal)
        setting_vbox.addWidget(self.setting_btn_widget)
        setting_vbox.addWidget(self.setting_layout)
        scroll_vbox.addLayout(setting_vbox)

        snapshots_vbox = QVBoxLayout()
        self.create_snapshots_btn()
        self.snapshot_layout = SnapshotLayout()
        snapshots_vbox.addWidget(self.snapshot_btn_widget)
        snapshots_vbox.addWidget(self.snapshot_layout)
        scroll_vbox.addLayout(snapshots_vbox)

        records_vbox = QVBoxLayout()
        self.create_records_btn()
        self.record_layout = RecordLayout()
        records_vbox.addWidget(self.records_btn_widget)
        records_vbox.addWidget(self.record_layout)
        scroll_vbox.addLayout(records_vbox)

        scroll_vbox.setAlignment(Qt.AlignTop)
        scroll_vbox.setContentsMargins(0, 0, 0, 0)
        scroll_vbox.setSpacing(2)
        scroll_content.setStyleSheet("border:None")

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("border:None;background-color:#050404")
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def create_setting_btn(self):
        self.setting_btn_widget=QWidget()
        self.setting_btn_widget.setFixedWidth(245)
        self.setting_btn_widget.setFixedHeight(40)
        self.setting_btn_widget.setStyleSheet('''background-color:#151c14; color:white;margin-left:1px;margin-top:1px;padding:0px;
                                           border:none;
                                           font-size:14px;
                                           font-weight:bold;
                                           border-radius:6px''')
        setting_btn_text = QLabel(f'Setting')
        setting_btn_text.setAlignment(Qt.AlignVCenter) 
        setting_btn_text.setStyleSheet('''padding-left:5px;
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 14px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')

        self.setting_logo=QLabel()
        pixmap=QPixmap('files/styles/down.png')
        self.setting_logo.setPixmap(pixmap)
        self.setting_logo.setStyleSheet('''border:none;''')
        self.setting_logo.setFixedWidth(30)
        self.setting_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.setting_hbox = QHBoxLayout()
        self.setting_hbox.setContentsMargins(0, 0, 10, 0)

        self.setting_hbox.addWidget(setting_btn_text)
        self.setting_hbox.addWidget(self.setting_logo)

        self.setting_btn_widget.setLayout(self.setting_hbox)

        self.setting_btn_widget.mousePressEvent = lambda event: self.clicked_btn_setting() if event.button() == Qt.LeftButton else None




    def create_snapshots_btn(self):        
        self.snapshot_btn_widget=QWidget()
        self.snapshot_btn_widget.setFixedWidth(245)
        self.snapshot_btn_widget.setFixedHeight(40)
        self.snapshot_btn_widget.setStyleSheet('''background-color:#151c14; color:white;margin-left:1px;margin-top:1px;padding:0px;
                                           border:none;
                                           font-size:14px;
                                           font-weight:bold;
                                           border-radius:6px''')
        
        snapshot_btn_text = QLabel(f'Snapshots')
        snapshot_btn_text.setAlignment(Qt.AlignVCenter) 
        snapshot_btn_text.setStyleSheet('''padding-left:5px;
                                           border:none;
                                           font-family: 'Roboto';
              
                                           font-size: 14px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')

        self.snapshot_logo=QLabel()
        pixmap=QPixmap('files/styles/down.png')
        self.snapshot_logo.setPixmap(pixmap)
        self.snapshot_logo.setStyleSheet('''border:none;''')
        self.snapshot_logo.setFixedWidth(30)
        self.snapshot_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.snapshot_hbox = QHBoxLayout()
        self.snapshot_hbox.setContentsMargins(0, 0, 10, 0)

        self.snapshot_hbox.addWidget(snapshot_btn_text)
        self.snapshot_hbox.addWidget(self.snapshot_logo)

        self.snapshot_btn_widget.setLayout(self.snapshot_hbox)

        self.snapshot_btn_widget.mousePressEvent = lambda event: self.clicked_btn_snapshots() if event.button() == Qt.LeftButton else None




    def create_records_btn(self):
        self.records_btn_widget=QWidget()
        self.records_btn_widget.setFixedWidth(245)
        self.records_btn_widget.setFixedHeight(40)
        self.records_btn_widget.setStyleSheet('''background-color:#151c14; color:white;margin-left:1px;margin-top:1px;padding:0px;
                                           border:none;
                                           font-size:14px;
                                           font-weight:bold;
                                           border-radius:6px''')
        records_btn_text = QLabel(f'Records')
        records_btn_text.setAlignment(Qt.AlignVCenter) 
        records_btn_text.setStyleSheet('''padding-left:5px;
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 14px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')

        self.records_logo=QLabel()
        pixmap=QPixmap('files/styles/down.png')
        self.records_logo.setPixmap(pixmap)
        self.records_logo.setStyleSheet('''border:none;''')
        self.records_logo.setFixedWidth(30)
        self.records_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.records_hbox = QHBoxLayout()
        self.records_hbox.setContentsMargins(0, 0, 10, 0)

        self.records_hbox.addWidget(records_btn_text)
        self.records_hbox.addWidget(self.records_logo)

        self.records_btn_widget.setLayout(self.records_hbox)

        self.records_btn_widget.mousePressEvent = lambda event: self.clicked_btn_records() if event.button() == Qt.LeftButton else None




    def clicked_btn_setting(self):
        if self.setting_layout.isVisible(): 
          self.setting_layout.setVisible(False)
          pixmap=QPixmap('files/styles/down.png')
          self.setting_logo.setPixmap(pixmap)
          self.updateGeometry()
        else:
          self.setting_layout.setVisible(True)
          pixmap=QPixmap('files/styles/up.png')
          self.setting_logo.setPixmap(pixmap)
          self.updateGeometry()

    def clicked_btn_snapshots(self):
        if self.snapshot_layout.isVisible(): 
          self.snapshot_layout.setVisible(False)
          pixmap=QPixmap('files/styles/down.png')
          self.snapshot_logo.setPixmap(pixmap)
          self.updateGeometry()
        else:
          self.snapshot_layout.setVisible(True)
          pixmap=QPixmap('files/styles/up.png')
          self.snapshot_logo.setPixmap(pixmap)
          self.updateGeometry()


    def clicked_btn_records(self):
        if self.record_layout.isVisible(): 
          self.record_layout.setVisible(False)
          pixmap=QPixmap('files/styles/down.png')
          self.records_logo.setPixmap(pixmap)
          self.updateGeometry()
        else:
          self.record_layout.setVisible(True)
          pixmap=QPixmap('files/styles/up.png')
          self.records_logo.setPixmap(pixmap)
          self.updateGeometry()

