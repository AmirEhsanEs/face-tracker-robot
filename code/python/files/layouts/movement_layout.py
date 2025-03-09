import sys
from PyQt5.QtWidgets import QFrame,QVBoxLayout ,QLabel,QHBoxLayout,QComboBox,QLineEdit,QPushButton
from PyQt5.QtCore import pyqtSignal as Signal


from files.dialogs.error_dialog import ErrorDialog
class MovementLayout(QFrame):
     mode_signal=Signal(int)
     move_type_signal=Signal(int)
     h_move_signal=Signal(float)
     v_move_signal=Signal(float)
     start_keyframe_signal=Signal(int)
     execute_steps_signal=Signal(int)
     pic_count_signal=Signal(int)
     deg_per_pic_signal=Signal(float)
     delay_between_pic_signal=Signal(int)
     btn_add_keyframe_signal=Signal()
     def __init__(self):
         super().__init__()
         main_vbox=QVBoxLayout()
         move_to_vbox=QVBoxLayout()
         movement_type_hbox=QHBoxLayout()
         move_to_hbox=QHBoxLayout() 
         start_keyframe_hbox=QHBoxLayout()
         execute_steps_hbox=QHBoxLayout()
         pic_count_hbox =QHBoxLayout()
         deg_per_pic_hbox=QHBoxLayout()
         delay_between_pic_hbox=QHBoxLayout()
         add_keyframe_hbox=QHBoxLayout()

         movemrnt_type_label=QLabel("Movement Type:")
         move_to_label=QLabel("Move To:")
         start_keyframe_label=QLabel("Start Keyframe:")
         execute_steps_label=QLabel("Execute Steps:")
         pic_count_label=QLabel("Pic Count:")
         deg_per_pic_label=QLabel("Deg/pic:")
         delay_between_pic_label=QLabel("Pic Delay:")


         self.h_move_line_edit=QLineEdit()
         self.v_move_line_edit=QLineEdit()
         self.start_keyframe_line_edit=QLineEdit()
         self.execute_steps_line_edit=QLineEdit()
         self.pic_count_line_edit=QLineEdit()
         self.deg_per_pic_line_edit=QLineEdit()
         self.delay_between_pic_line_edit=QLineEdit()


         self.movement_combo_box=QComboBox()   
         self.movement_combo_box.addItems(["Move to","Keyframe move","Keyframe deg/pic","Keyframe pic count","Keyframe record"])
   
         self.add_keyframe_btn=QPushButton("Add keyframe")

         movement_type_hbox.addWidget(movemrnt_type_label)
         movement_type_hbox.addWidget(self.movement_combo_box)
         move_to_hbox.addWidget(self.h_move_line_edit)
         move_to_hbox.addWidget(self.v_move_line_edit)
         start_keyframe_hbox.addWidget(start_keyframe_label)
         start_keyframe_hbox.addWidget(self.start_keyframe_line_edit)
         execute_steps_hbox.addWidget(execute_steps_label)
         execute_steps_hbox.addWidget(self.execute_steps_line_edit)
         pic_count_hbox.addWidget(pic_count_label)
         pic_count_hbox.addWidget(self.pic_count_line_edit)
         deg_per_pic_hbox.addWidget(deg_per_pic_label)
         deg_per_pic_hbox.addWidget(self.deg_per_pic_line_edit)
         delay_between_pic_hbox.addWidget(delay_between_pic_label)
         delay_between_pic_hbox.addWidget(self.delay_between_pic_line_edit) 
         add_keyframe_hbox.addWidget(self.add_keyframe_btn)

         main_vbox.addLayout(movement_type_hbox)
         main_vbox.addWidget(move_to_label)
         main_vbox.addLayout(move_to_hbox)
         main_vbox.addLayout(start_keyframe_hbox)
         main_vbox.addLayout(execute_steps_hbox)
         main_vbox.addLayout(pic_count_hbox)
         main_vbox.addLayout(deg_per_pic_hbox)
         main_vbox.addLayout(delay_between_pic_hbox)
         main_vbox.addLayout(add_keyframe_hbox)
         self.setLayout(main_vbox)
         self.setVisible(False)

         movemrnt_type_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         move_to_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         start_keyframe_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         execute_steps_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         pic_count_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         deg_per_pic_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')
         delay_between_pic_label.setStyleSheet( '''QLabel {
                                                    font-family: 'Roboto';
                                                    font-size: 12px;
                                                    color:#e0e0e0;
                                                    font-weight:bold;
                                                    }''')

         self.h_move_line_edit.setStyleSheet("""
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
         self.h_move_line_edit.setFixedWidth(55)  
         self.v_move_line_edit.setStyleSheet("""
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
         self.v_move_line_edit.setFixedWidth(55)  
         self.start_keyframe_line_edit.setStyleSheet("""
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
         self.start_keyframe_line_edit.setFixedWidth(35)  
         self.execute_steps_line_edit.setStyleSheet("""
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
         self.execute_steps_line_edit.setFixedWidth(35)  
         self.pic_count_line_edit.setStyleSheet("""
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
         self.pic_count_line_edit.setFixedWidth(55)  
         self.deg_per_pic_line_edit.setStyleSheet("""
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
         self.deg_per_pic_line_edit.setFixedWidth(55)  
         self.delay_between_pic_line_edit.setStyleSheet("""
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
         self.delay_between_pic_line_edit.setFixedWidth(55)  
         self.movement_combo_box.setStyleSheet('''
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
         self.movement_combo_box.setFixedWidth(100)
         self.add_keyframe_btn.setStyleSheet(''' 
                                        QPushButton {
                                                        color: #e0e0e0;
                                                        background-color: #2c592c;
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
                                            ''')
         self.add_keyframe_btn.setFixedSize(120,30)
         start_keyframe_hbox.setSpacing(0)
         execute_steps_hbox.setSpacing(0)
         pic_count_hbox.setSpacing(0)
         deg_per_pic_hbox.setSpacing(0)
         delay_between_pic_hbox.setSpacing(0)
         main_vbox.setSpacing(20)
         move_to_hbox.setSpacing(0)
         
         self.mode_signal.connect(self.changed_mode)
         self.movement_combo_box.currentIndexChanged.connect(self.change_move_type_combo_box)      
         self.h_move_line_edit.editingFinished.connect(self.validate_h_move)
         self.v_move_line_edit.editingFinished.connect(self.validate_v_move)
         self.start_keyframe_line_edit.editingFinished.connect(self.validate_start_keyframe)
         self.execute_steps_line_edit.editingFinished.connect(self.validate_execute_steps)
         self.pic_count_line_edit.editingFinished.connect(self.validate_pic_count)
         self.deg_per_pic_line_edit.editingFinished.connect(self.validate_deg_per_pic)
         self.delay_between_pic_line_edit.editingFinished.connect(self.validate_delay_between_pic)
         self.add_keyframe_btn.clicked.connect(self.clicked_btn_add_keyframe)

         self.h_move_text=""
         self.v_move_text=""
         self.start_keyframe_text=""
         self.execute_steps_text=""
         self.pic_count_text=""
         self.deg_per_pic_text="" 
         self.delay_between_pic_text=""
         self.keyframe_count=0


    
     def changed_mode(self,mode):
          self.mode=mode
          if self.h_move_text!="": 
            self.validate_h_move()
          if self.v_move_text!="":  
            self.validate_v_move()
          if self.deg_per_pic_text!="":  
            self.validate_deg_per_pic()

     def get_keyframe_start(self,start):
         if start==-1:
            self.start_keyframe_line_edit.setText("")
            self.start_keyframe_text=""
         else:
           self.start_keyframe_line_edit.setText(str(start))
           self.start_keyframe_text=str(start)

     def get_keyframe_count(self,count):
         if count==2 and self.keyframe_count==1:
             self.execute_steps_line_edit.setText("1")
             self.execute_steps_text="1"
             self.execute_steps_signal.emit(1)
    
         elif count==1 and self.keyframe_count==2 :
                 val=int(self.execute_steps_text)
                 self.execute_steps_line_edit.setText("")
                 self.execute_steps_text=""
         self.keyframe_count=count           
                 
             
     def validate_h_move(self):
        try:
              value=float(self.h_move_line_edit.text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   

              self.h_move_line_edit.setText(str(value))
              self.h_move_text=str(value)
              self.h_move_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.h_move_line_edit.setText(self.h_move_text)
         
     def validate_v_move(self):
        try:
              value=float(self.v_move_line_edit.text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   

              self.v_move_line_edit.setText(str(value))
              self.v_move_text=str(value)
              self.v_move_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.v_move_line_edit.setText(self.v_move_text)
         
     def validate_start_keyframe(self):
        try:
              value=int(self.start_keyframe_line_edit.text())
              if value<0:
                 error_dialog=ErrorDialog("Start index cant be negative!!")
                 error_dialog.exec_() 
                 self.start_keyframe_line_edit.setText(self.start_keyframe_text) 
              elif value>=self.keyframe_count:        
                 error_dialog=ErrorDialog("Start index not valid!!")
                 error_dialog.exec_() 
                 self.start_keyframe_line_edit.setText(self.start_keyframe_text)
              else :    
                 self.start_keyframe_line_edit.setText(str(value))
                 self.start_keyframe_text=str(value)
                 self.start_keyframe_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter Integer value!! ")
              error_dialog.exec_() 
              self.start_keyframe_line_edit.setText(self.start_keyframe_text)
         
     def validate_execute_steps(self):
        try:
              value=int(self.execute_steps_line_edit.text())
              if self.keyframe_count<2:        
                 error_dialog=ErrorDialog("Need at least 2 keyframe!!")
                 error_dialog.exec_() 
                 self.execute_steps_line_edit.setText("")
              elif value>30 or value <-30:
                 error_dialog=ErrorDialog("Maximum 30 step can go to forward or backward!!")
                 error_dialog.exec_() 
                 self.execute_steps_line_edit.setText(self.execute_steps_text)    
              else :    
                 self.execute_steps_line_edit.setText(str(value))
                 self.execute_steps_text=str(value)
                 self.execute_steps_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter Integer value!! ")
              error_dialog.exec_() 
              self.execute_steps_line_edit.setText(self.execute_steps_text)
         
     def validate_pic_count(self):
         try:
              value=int(self.pic_count_line_edit.text())
              if value>1000 or value <1:
                 error_dialog=ErrorDialog("Pic count at list 1 and max 1000!!")
                 error_dialog.exec_() 
                 self.pic_count_line_edit.setText(self.pic_count_text)                     
              else :    
                 self.pic_count_line_edit.setText(str(value))
                 self.pic_count_text=str(value)
                 self.pic_count_signal.emit(value)

         except ValueError:
              error_dialog=ErrorDialog("Please enter Integer value!! ")
              error_dialog.exec_() 
              self.pic_count_line_edit.setText(self.pic_count_text)
        
     def validate_deg_per_pic(self):   
        try:
              value=float(self.deg_per_pic_line_edit.text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   

              self.deg_per_pic_line_edit.setText(str(value))
              self.deg_per_pic_text=str(value)
              self.deg_per_pic_signal.emit(value)

        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.deg_per_pic_line_edit.setText(self.deg_per_pic_text)
         

     def validate_delay_between_pic(self):
         try:
              value=int(self.delay_between_pic_line_edit.text())
              if value>65535 or value <200:
                 error_dialog=ErrorDialog("Pic count at list 200 and max 65535 milisec!!")
                 error_dialog.exec_() 
                 self.delay_between_pic_line_edit.setText(self.delay_between_pic_text)                     
              else :    
                 self.delay_between_pic_line_edit.setText(str(value))
                 self.delay_between_pic_text=str(value)
                 self.delay_between_pic_signal.emit(value)

         except ValueError:
              error_dialog=ErrorDialog("Please enter Integer value!! ")
              error_dialog.exec_() 
              self.delay_between_pic_line_edit.setText(self.delay_between_pic_text)
   
     def change_move_type_combo_box(self):
         val=int(self.movement_combo_box.currentIndex())
         self.move_type_signal.emit(val)
     def clicked_btn_add_keyframe(self):
         self.btn_add_keyframe_signal.emit()
   
