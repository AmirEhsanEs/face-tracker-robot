import sys
from PyQt5.QtWidgets import (QFrame,QVBoxLayout ,QLabel,QHBoxLayout,QLineEdit,QPushButton,QSlider,QCheckBox,
                             QComboBox,QWidget)
from PyQt5.QtCore import pyqtSignal as Signal,pyqtSlot as Slot,Qt
from files.dialogs.error_dialog import ErrorDialog
class SettingLayout(QFrame):
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
        main_layout=QVBoxLayout()
        self.setVisible(False)
        enable_motor_hbox=QHBoxLayout()
        enable_accel_hbox=QHBoxLayout()
        automatic_track_hbox=QHBoxLayout()
        detect_hand_hbox=QHBoxLayout()
        mode_hbox=QHBoxLayout()
        move_increment_hbox=QHBoxLayout()
        speed_hbox=QHBoxLayout()
        accel_hbox=QHBoxLayout()
        speed_vbox=QVBoxLayout()
        accel_vbox=QVBoxLayout()

        enable_motor_widget=QWidget()
        enable_accel_widget=QWidget()
        automatic_track_widget=QWidget()
        detect_hand_widget=QWidget()

        enable_motor_widget.setFixedWidth(150)
        enable_accel_widget.setFixedWidth(150)
        automatic_track_widget.setFixedWidth(150)
        detect_hand_widget.setFixedWidth(150)



        enable_motor_label=QLabel("Enable Motors:")
        enable_accel_label=QLabel("Enable Accel:")
        automatic_track_label=QLabel("Automatic Track:")
        detect_hand_label=QLabel("Detect Hand:")
        mode_label=QLabel("Mode:")
        move_increment_label=QLabel("Move Increment:")
        speed_label=QLabel("Speed:")
        accel_label=QLabel("Accel:")

        self.enable_motor_checkbox=QCheckBox()
        self.enabel_accel_checkbox=QCheckBox()
        self.automatic_track_checkbox=QCheckBox()
        self.detect_hand_checkbox=QCheckBox()
        self.enable_motor_checkbox.setChecked(bool(self.setting.enable))
        self.enabel_accel_checkbox.setChecked(bool(self.setting.accel_enable))
        self.automatic_track_checkbox.setChecked(bool(self.setting.automatic_track))
        self.detect_hand_checkbox.setChecked(bool(self.setting.detect_hand)) 
        self.enable_motor_checkbox.stateChanged.connect(self.motor_enable_changed)
        self.enabel_accel_checkbox.stateChanged.connect(self.accel_enable_changed)
        self.automatic_track_checkbox.stateChanged.connect(self.auto_track_changed) 
        self.detect_hand_checkbox.stateChanged.connect(self.detect_hand_changed)


        self.mode_combo_box=QComboBox()
        self.mode_combo_box.addItems(["2","4","8","16"])
        self.mode_combo_box.setFixedWidth(50)
        self.mode_combo_box.setCurrentText(str(self.setting.step_mode))
        self.mode_combo_box.currentIndexChanged.connect(self.changeComboBox)

        self.move_increment_line_edit=QLineEdit()
        self.h_speed_line_edit=QLineEdit()
        self.v_speed_line_edit=QLineEdit()
        self.h_accel_line_edit=QLineEdit()
        self.v_accel_line_edit=QLineEdit()
        self.move_increment_line_edit.setFixedWidth(50)
        self.h_speed_line_edit.setFixedWidth(50)
        self.v_speed_line_edit.setFixedWidth(50)
        self.h_accel_line_edit.setFixedWidth(50)
        self.v_accel_line_edit.setFixedWidth(50)
        self.move_increment_line_edit.setText(str(self.setting.move_invrement))
        self.h_speed_line_edit.setText(str(self.setting.horizontal_max_speed))
        self.v_speed_line_edit.setText(str(self.setting.vertical_max_speed))
        self.h_accel_line_edit.setText(str(self.setting.horizontal_accel))
        self.v_accel_line_edit.setText(str(self.setting.vertical_accel))
        self.validate_move_increment()
        self.validate_h_speed()
        self.validate_v_speed()
        self.validate_h_accel()

        
        enable_motor_widget.setLayout(enable_motor_hbox)
        enable_accel_widget.setLayout(enable_accel_hbox)
        automatic_track_widget.setLayout(automatic_track_hbox)
        detect_hand_widget.setLayout(detect_hand_hbox)
        enable_motor_hbox.setSpacing(0) 
        enable_accel_hbox.setSpacing(0)
        automatic_track_hbox.setSpacing(0)
        detect_hand_hbox.setSpacing(0)
        enable_motor_hbox.setContentsMargins(0,0,0,0)
        enable_accel_hbox.setContentsMargins(0,0,0,0)
        automatic_track_hbox.setContentsMargins(0,0,0,0)
        detect_hand_hbox.setContentsMargins(0,0,0,0)

        self.validate_v_accel()
        enable_motor_hbox.addWidget(enable_motor_label)
        enable_motor_hbox.addWidget(self.enable_motor_checkbox)
        enable_accel_hbox.addWidget(enable_accel_label)
        enable_accel_hbox.addWidget(self.enabel_accel_checkbox)
        automatic_track_hbox.addWidget(automatic_track_label)
        automatic_track_hbox.addWidget(self.automatic_track_checkbox) 
        detect_hand_hbox.addWidget(detect_hand_label)
        detect_hand_hbox.addWidget(self.detect_hand_checkbox)
        mode_hbox.addWidget(mode_label)
        mode_hbox.addWidget(self.mode_combo_box)
        mode_hbox.setSpacing(0)
        move_increment_hbox.addWidget(move_increment_label)
        move_increment_hbox.addWidget(self.move_increment_line_edit)
        speed_hbox.addWidget(self.h_speed_line_edit)
        speed_hbox.addWidget(self.v_speed_line_edit)
        accel_hbox.addWidget(self.h_accel_line_edit)
        accel_hbox.addWidget(self.v_accel_line_edit)
        speed_hbox.setSpacing(0)
        accel_hbox.setSpacing(0)

        
        speed_vbox.addWidget(speed_label)
        speed_vbox.addLayout(speed_hbox)
        accel_vbox.addWidget(accel_label)
        accel_vbox.addLayout(accel_hbox)
        speed_vbox.setSpacing(0)
        accel_vbox.setSpacing(0)
        main_layout.addWidget(enable_motor_widget)
        main_layout.addWidget(enable_accel_widget)
        main_layout.addWidget(automatic_track_widget)
        main_layout.addWidget(detect_hand_widget)
        main_layout.addLayout(mode_hbox)
        main_layout.addLayout(move_increment_hbox)
        main_layout.addLayout(speed_vbox)
        main_layout.addLayout(accel_vbox)


        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0,0,0,20)
        self.setLayout(main_layout)

 
        enable_motor_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
        enable_accel_label.setStyleSheet('''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                                                               
                                                    }''')
        automatic_track_label.setStyleSheet('''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    
                                                    }''')
        detect_hand_label.setStyleSheet('''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    
                                                    }''')
        mode_label.setStyleSheet('''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    
                                                    }''')
               
        move_increment_label.setStyleSheet('''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    
                                                    }''')
        speed_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                    
                                                    }''') 
        accel_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''')
                                    
  
        self.mode_combo_box.setStyleSheet('''
                                            QComboBox {
                                                    background-color: #2b2b2b;
                                                    color: white;
                                                    border: 1px solid #2b2b2b;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                    margin-left: 0px;
                                                 }

                                                QComboBox::drop-down {
                                                    subcontrol-origin: padding;
                                                    subcontrol-position: top right;
                                                    width: 20px;
                                                    background-color: #2b2b2b;
                                                }

                                                QComboBox::down-arrow {
                                                    image: url(files/styles/down.png); 
                                                    width: 9px;
                                                    height: 9px;
                                                }

                                                QComboBox QAbstractItemView {
                                                    background-color: #2b2b2b;
                                                    color: white;
                                                    selection-background-color: #2c592c;
                                                    selection-color: white;
                                                    border-radius:5px;
                                                    border: 1px solid #5a5a5a;
                                                    outline: 0;  
                                                    padding:0;
                                                    margin:0;
                                                } 
                                            QComboBox QAbstractItemView::item {
                                                    outline: none; 
                                                    padding: 5px;
                                                    background-color: #6a0dad;
                                                    color: #6a0dad;
                                                }

                                            QComboBox QAbstractItemView::item:selected {
                                                     background-color: #6a0dad;
                                                     color: #6a0dad;
                                                }
                                          ''') 
        self.mode_combo_box.setFixedWidth(60)
        self.move_increment_line_edit.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2b2b2b;
                                                        color: #ffffff;
                                                        border-radius: 5px;
                                                        padding: 5px;
                                                        selection-background-color: #2b2b2b;
                                                        selection-color: #ffffff;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 1px solid #2c592c;
                                                        }   
                                                """)    
        self.move_increment_line_edit.setFixedWidth(65)    
        self.h_speed_line_edit.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2b2b2b;
                                                        color: #ffffff;
                                                        border-radius: 5px;
                                                        padding: 5px;
                                                        selection-background-color: #2b2b2b;
                                                        selection-color: #ffffff;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 1px solid #2c592c;
                                                        } 
                                                """) 
        self.h_speed_line_edit.setFixedWidth(65)   
        self.v_speed_line_edit.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2b2b2b;
                                                        color: #ffffff;
                                                        border-radius: 5px;
                                                        padding: 5px;
                                                        selection-background-color: #2b2b2b;
                                                        selection-color: #ffffff;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 1px solid #2c592c;
                                                        } 
                                                """)  
        self.v_speed_line_edit.setFixedWidth(65)   
        self.h_accel_line_edit.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2b2b2b;
                                                        color: #ffffff;
                                                        border-radius: 5px;
                                                        padding: 5px;
                                                        selection-background-color: #2b2b2b;
                                                        selection-color: #ffffff;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 1px solid #2c592c;
                                                        } 
                                                """)
        self.h_accel_line_edit.setFixedWidth(65)    
        self.v_accel_line_edit.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2b2b2b;
                                                        color: #ffffff;
                                                        border-radius: 5px;
                                                        padding: 5px;
                                                        selection-background-color: #2b2b2b;
                                                        selection-color: #ffffff;
                                                    }
                                             
                                                   QLineEdit:focus {
                                                        border: 1px solid #2c592c;
                                                        } 
                                                """)  
        self.v_accel_line_edit.setFixedWidth(65)   
        self.enabel_accel_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: white;
                                                    background-color: #2e2e2e;
                                                    border: 1px solid #5c5c5c;
                                                    padding: 0px;
                                                    border-radius: 2px
                                                }
                                                QCheckBox::indicator {
                                                    width: 12px;
                                                    height: 12px;
                                                 
                                                }
                                                QCheckBox::indicator::unchecked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2e2e2e;
                                                    border-radius: 2px

                                                }
                                                QCheckBox::indicator::checked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2c592c; 
                                                    image: url(files/styles/check.png);
                                                 
                                                }
                                            """)
        self.enabel_accel_checkbox.setFixedWidth(26)
        self.enable_motor_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: white;
                                                    background-color: #2e2e2e;
                                                    border: 1px solid #5c5c5c;
                                                    padding: 0px;
                                                    border-radius: 2px
                                                }
                                                QCheckBox::indicator {
                                                    width: 12px;
                                                    height: 12px;
                                                 
                                                }
                                                QCheckBox::indicator::unchecked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2e2e2e;
                                                    border-radius: 2px

                                                }
                                                QCheckBox::indicator::checked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2c592c; 
                                                    image: url(files/styles/check.png);
                                                 
                                                }
                                            """)
        self.enable_motor_checkbox.setFixedWidth(26)   
        
        self.automatic_track_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: white;
                                                    background-color: #2e2e2e;
                                                    border: 1px solid #5c5c5c;
                                                    padding: 0px;
                                                    border-radius: 2px
                                                }
                                                QCheckBox::indicator {
                                                    width: 12px;
                                                    height: 12px;
                                                 
                                                }
                                                QCheckBox::indicator::unchecked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2e2e2e;
                                                    border-radius: 2px

                                                }
                                                QCheckBox::indicator::checked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2c592c; 
                                                    image: url(files/styles/check.png);
                                                 
                                                }
                                            """)
        self.automatic_track_checkbox.setFixedWidth(26)   
        
        self.detect_hand_checkbox.setStyleSheet("""
                                                QCheckBox {
                                                    color: white;
                                                    background-color: #2e2e2e;
                                                    border: 1px solid #5c5c5c;
                                                    padding: 0px;
                                                    border-radius: 2px
                                                }
                                                QCheckBox::indicator {
                                                    width: 12px;
                                                    height: 12px;
                                                 
                                                }
                                                QCheckBox::indicator::unchecked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2e2e2e;
                                                    border-radius: 2px

                                                }
                                                QCheckBox::indicator::checked {
                                                    border: 1px solid #5c5c5c;
                                                    background-color: #2c592c; 
                                                    image: url(files/styles/check.png);
                                                 
                                                }
                                            """)
        self.detect_hand_checkbox.setFixedWidth(26)   
        self.move_increment_line_edit.editingFinished.connect(self.validate_move_increment)
        self.h_speed_line_edit.editingFinished.connect(self.validate_h_speed)
        self.v_speed_line_edit.editingFinished.connect(self.validate_v_speed)
        self.h_accel_line_edit.editingFinished.connect(self.validate_h_accel)
        self.v_accel_line_edit.editingFinished.connect(self.validate_v_accel)
        main_layout.addSpacing(10)
        self.setStyleSheet("margin:5px")
        


  def motor_enable_changed(self):
       if self.enable_motor_checkbox.isChecked():
            state=1
       else:
            state=0
       self.motor_enable_signal.emit(state)

  def  accel_enable_changed(self):
       if self.enabel_accel_checkbox.isChecked():
            state=1
       else:
            state=0
       self.accel_enable_signal.emit(state) 

  def  auto_track_changed(self):
       if self.automatic_track_checkbox.isChecked():
            state=1
       else:
            state=0
       self.auto_track_signal.emit(state)

  def  detect_hand_changed(self):
       if self.detect_hand_checkbox.isChecked():
            state=1
       else:
            state=0
       self.hand_detect_signal.emit(state)
   
  def validate_move_increment(self):
       mode=int(self.mode_combo_box.currentText())
       try:
              value=float(self.move_increment_line_edit.text())
              if mode==2:
                  value=int(round(value))
              elif mode==4:
                  value=round(value,1)
              elif mode==8:
                  value=round(value,2)        
              elif mode==16:
                  value=round(value,3)   

              self.move_increment_line_edit.setText(str(value))
              self.move_increment_signal.emit(value)
                  
       except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.move_increment_line_edit.setText(str(self.setting.move_invrement))
        

  def validate_h_speed(self):
        mode=int(self.mode_combo_box.currentText())
        try:
              value=float(self.h_speed_line_edit.text())
              if mode==2:
                  value=int(round(value))
              elif mode==4:
                  value=round(value,1)
              elif mode==8:
                  value=round(value,2)        
              elif mode==16:
                  value=round(value,3)   

              self.h_speed_line_edit.setText(str(value))
              self.horizontal_speed_signal.emit(value)

                  
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.h_speed_line_edit.setText(str(self.setting.horizontal_max_speed))
              
  def validate_v_speed(self):
        mode=int(self.mode_combo_box.currentText())
        try:
            value=float(self.v_speed_line_edit.text())
            if mode==2:
                value=int(round(value))
            elif mode==4:
                value=round(value,1)
            elif mode==8:
                value=round(value,2)        
            elif mode==16:
                value=round(value,3)   
            self.v_speed_line_edit.setText(str(value))
            self.vertical_speed_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.v_speed_line_edit.setText(str(self.setting.vertical_max_speed))

  def validate_h_accel(self):
        mode=int(self.mode_combo_box.currentText())
        try:
            value=float(self.h_accel_line_edit.text())
            if mode==2:
                value=int(round(value))
            elif mode==4:
                value=round(value,1)
            elif mode==8:
                value=round(value,2)        
            elif mode==16:
                value=round(value,3)   
            self.h_accel_line_edit.setText(str(value))
            self.horizontal_accel_signal.emit(value)

                
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.h_accel_line_edit.setText(str(self.setting.horizontal_accel))


  def validate_v_accel(self):
        mode=int(self.mode_combo_box.currentText())
        try:
            value=float(self.v_accel_line_edit.text())
            if mode==2:
                value=int(round(value))
            elif mode==4:
                value=round(value,1)
            elif mode==8:
                value=round(value,2)        
            elif mode==16:
                value=round(value,3)   
            self.v_accel_line_edit.setText(str(value))
            self.vertical_accel_signal.emit(value)
                
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.v_accel_line_edit.setText(str(self.setting.vertical_accel))    

  def changeComboBox(self):
      self.mode_signal.emit(int(self.mode_combo_box.currentText()))
      self.validate_move_increment()
      self.validate_h_speed()
      self.validate_v_speed()
      self.validate_h_accel()
      self.validate_v_accel() 
