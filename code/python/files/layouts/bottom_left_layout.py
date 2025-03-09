
from PyQt5.QtWidgets import (QVBoxLayout,QFrame,QLabel,QScrollArea,QWidget,QHBoxLayout,QCheckBox,QLineEdit
                             ,QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent,QPixmap
from PyQt5.QtCore import pyqtSignal as Signal

from files.layouts.movement_layout import MovementLayout
from files.dialogs.error_dialog import ErrorDialog

class BottomLeftLayout(QWidget):
    mode_signal=Signal(int)
    move_type_signal=Signal(int)
    h_move_signal=Signal(float)
    v_move_signal=Signal(float)
    send_start_keyframe_signal=Signal(int)
    recieve_start_keyframe_signal=Signal(int)
    execute_steps_signal=Signal(int)
    pic_count_signal=Signal(int)
    deg_per_pic_signal=Signal(float)
    delay_between_pic_signal=Signal(int)
    btn_add_keyframe_signal=Signal()
    keyframe_count_signal=Signal(int)
    delete_keyframe_signal=Signal(int)
    edit_index_signal=Signal(int)
    edit_keyframe_accel_enable_signal=Signal(int)
    edit_keyframe_delay_signal=Signal(int)
    edit_keyframe_h_deg_signal=Signal(float)
    edit_keyframe_v_deg_signal=Signal(float)
    edit_keyframe_h_speed_signal=Signal(float)
    edit_keyframe_v_speed_signal=Signal(float)
    edit_keyframe_h_accel_signal=Signal(float)
    edit_keyframe_v_accel_signal=Signal(float)



    def __init__(self):
        super().__init__()
        self.keyframe_count=0
        self.keyframe_layouts=[] 
        self.keyframe_btns=[]
        self.keyframe_accel_enable_check_boxs=[]
        self.keyframe_delay_line_edits=[]
        self.keyframe_h_deg_line_edits=[]
        self.keyframe_v_deg_line_edits=[]        
        self.keyframe_h_speed_line_edits=[]
        self.keyframe_v_speed_line_edits=[]
        self.keyframe_h_accel_line_edits=[]
        self.keyframe_v_accel_line_edits=[]
        self.keyframe_del_btns=[]

        self.keyframe_delay_texts=[]
        self.keyframe_h_deg_texts=[]
        self.keyframe_v_deg_texts=[]        
        self.keyframe_h_speed_texts=[]
        self.keyframe_v_speed_texts=[]
        self.keyframe_h_accel_texts=[]
        self.keyframe_v_accel_texts=[]

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        scroll_vbox = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_vbox)

        movement_vbox = QVBoxLayout()
        self.create_movement_btn()
        self.movement_layout = MovementLayout()

        movement_vbox.addWidget(self.movement_btn_widget)
        movement_vbox.addWidget(self.movement_layout)
        scroll_vbox.addLayout(movement_vbox)
        
        self.keyframes_vbox=QVBoxLayout()
        scroll_vbox.addLayout(self.keyframes_vbox)


        scroll_vbox.setAlignment(Qt.AlignTop)
        scroll_vbox.setContentsMargins(0, 0, 0, 0)
        scroll_vbox.setSpacing(2)
        scroll_content.setStyleSheet("border:None")


        self.movement_layout.move_type_signal.connect(self.move_type_signal)
        self.movement_layout.h_move_signal.connect(self.h_move_signal)
        self.movement_layout.v_move_signal.connect(self.v_move_signal)
        self.movement_layout.start_keyframe_signal.connect(self.send_start_keyframe_signal)
        self.movement_layout.execute_steps_signal.connect(self.execute_steps_signal)
        self.movement_layout.pic_count_signal.connect(self.pic_count_signal)
        self.movement_layout.deg_per_pic_signal.connect(self.deg_per_pic_signal)
        self.movement_layout.delay_between_pic_signal.connect(self.delay_between_pic_signal)
        self.movement_layout.btn_add_keyframe_signal.connect(self.btn_add_keyframe_signal)
        self.mode_signal.connect(self.changedMode)
        self.recieve_start_keyframe_signal.connect(self.movement_layout.get_keyframe_start)
        self.keyframe_count_signal.connect(self.movement_layout.get_keyframe_count)

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("border:None;background-color:#050404")
        self.keyframes_vbox.setSpacing(2)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        layout.setSpacing(2)
        layout.setContentsMargins(0,0,0,0)   
        self.setLayout(layout)


    def create_movement_btn(self):
        self.movement_btn_widget=QWidget()
        self.movement_btn_widget.setFixedWidth(245)
        self.movement_btn_widget.setFixedHeight(40)

        self.movement_btn_widget.setStyleSheet('''background-color:#151c14; color:white;margin-left:1px;margin-top:1px;padding:0px;
                                           border:none;
                                           font-size:14px;
                                           font-weight:bold;
                                           border-radius:6px''')
        movement_btn_text = QLabel(f'Movement')
        movement_btn_text.setAlignment(Qt.AlignVCenter) 
        movement_btn_text.setStyleSheet('''padding-left:5px;
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 14px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')

        self.movement_logo=QLabel()
        pixmap=QPixmap('files/styles/down.png')
        self.movement_logo.setPixmap(pixmap)
        self.movement_logo.setStyleSheet('''border:none;''')
        self.movement_logo.setFixedWidth(30)
        self.movement_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.movement_hbox = QHBoxLayout()
        self.movement_hbox.setContentsMargins(0, 0, 10, 0)

        self.movement_hbox.addWidget(movement_btn_text)
        self.movement_hbox.addWidget(self.movement_logo)

        self.movement_btn_widget.setLayout(self.movement_hbox)

        self.movement_btn_widget.mousePressEvent = lambda event: self.clicked_btn_movement() if event.button() == Qt.LeftButton else None



    def clicked_btn_movement(self):
        if self.movement_layout.isVisible(): 
          self.movement_layout.setVisible(False)
          pixmap=QPixmap('files/styles/down.png')
          self.movement_logo.setPixmap(pixmap)
          self.updateGeometry()
        else:
          self.movement_layout.setVisible(True)
          pixmap=QPixmap('files/styles/up.png')
          self.movement_logo.setPixmap(pixmap)
          self.updateGeometry()

    def create_keyframe(self):
        index=self.keyframe_count
        keyframe_layout=QVBoxLayout()

        self.keyframe_btn_widget=QWidget()
        self.keyframe_btn_widget.setFixedWidth(245)
        self.keyframe_btn_widget.setFixedHeight(40)
        self.keyframe_btn_widget.setStyleSheet('''background-color:#151c14; color:white;margin-left:0px;margin-top:1px;padding:0px;
                                           border:none;
                                           font-size:14px;
                                           font-weight:bold;
                                           border-radius:6px''')
        
        self.keyframe_btn_text = QLabel(f'Keyframe{index}')
        self.keyframe_btn_text.setAlignment(Qt.AlignVCenter) 
        self.keyframe_btn_text.setStyleSheet('''padding-left:0px;
                                           border:none;
                                           font-family: 'Roboto';
                                           font-size: 14px;
                                           color:#e0e0e0;
                                           font-weight:bold;
                                        ''')
        
        self.keyframe_logo=QLabel()
        pixmap=QPixmap('files/styles/down.png')
        self.keyframe_logo.setPixmap(pixmap)
        self.keyframe_logo.setStyleSheet('''border:none;''')
        self.keyframe_logo.setFixedWidth(30)
        self.keyframe_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        keyframe_btn_hbox = QHBoxLayout()
        keyframe_btn_hbox.addWidget(self.keyframe_btn_text)
        keyframe_btn_hbox.addWidget(self.keyframe_logo)

        self.keyframe_btn_widget.setLayout(keyframe_btn_hbox)
        keyframe_layout.addWidget(self.keyframe_btn_widget)
        self.keyframe_btn_widget.mousePressEvent = lambda event,idx=index: self.clicked_btn_keyframe(idx) if event.button() == Qt.LeftButton else None


        self.keyframe_content_widget=QWidget()
        keyframe_content_vbox=QVBoxLayout()

        keyframe_accel_enable_hbox=QHBoxLayout()
        keyframe_accel_enable_label=QLabel('Accel Enable:')
        keyframe_accel_enable_check_box=QCheckBox()
        keyframe_accel_enable_hbox.addWidget(keyframe_accel_enable_label)
        keyframe_accel_enable_hbox.addWidget(keyframe_accel_enable_check_box)
        keyframe_accel_enable_check_box.setChecked(bool(self.add_accel_enable))
        keyframe_accel_enable_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''') 
        keyframe_accel_enable_check_box.setStyleSheet("""
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
        keyframe_accel_enable_check_box.setFixedWidth(16)
        keyframe_content_vbox.addLayout(keyframe_accel_enable_hbox)
        keyframe_accel_enable_check_box.stateChanged.connect(lambda:self.changedAccelEnableCheckBox(index))

        
        
        keyframe_delay_hbox=QHBoxLayout()
        keyframe_delay_label=QLabel("Delay:")
        keyframe_delay_line_edit=QLineEdit()
        keyframe_delay_hbox.addWidget(keyframe_delay_label)
        keyframe_delay_hbox.addWidget(keyframe_delay_line_edit)
        keyframe_delay_line_edit.setText(str(self.add_delay))
        keyframe_delay_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''') 
        keyframe_delay_line_edit.setStyleSheet("""
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
        keyframe_delay_line_edit.setFixedWidth(55)   
        keyframe_content_vbox.addLayout(keyframe_delay_hbox)
        keyframe_delay_line_edit.editingFinished.connect(lambda:self.changedDelayLineEdit(index))
        
        position_vbox=QVBoxLayout()
        position_hbox=QHBoxLayout()
        position_label=QLabel("Degrre:")
        self.h_position_line_edit=QLineEdit()
        self.v_position_line_edit=QLineEdit()
        position_hbox.addWidget(self.h_position_line_edit)
        position_hbox.addWidget(self.v_position_line_edit)
        position_vbox.addWidget(position_label)
        position_vbox.addLayout(position_hbox)
        self.h_position_line_edit.setText(str(self.add_h_deg))
        self.v_position_line_edit.setText(str(self.add_v_deg))
        self.h_position_line_edit.setStyleSheet("""
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
        self.h_position_line_edit.setFixedWidth(55)   
        self.v_position_line_edit.setStyleSheet("""
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
        self.v_position_line_edit.setFixedWidth(55)   
        position_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''') 
        keyframe_content_vbox.addLayout(position_vbox)
        self.h_position_line_edit.editingFinished.connect(lambda:self.changedHDegLineEdit(index))
        self.v_position_line_edit.editingFinished.connect(lambda:self.changedVDegLineEdit(index))


        speed_vbox=QVBoxLayout()
        speed_hbox=QHBoxLayout()
        speed_label=QLabel("Speed:")
        self.h_speed_line_edit=QLineEdit()
        self.v_speed_line_edit=QLineEdit()
        speed_hbox.addWidget(self.h_speed_line_edit)
        speed_hbox.addWidget(self.v_speed_line_edit)
        speed_vbox.addWidget(speed_label)
        speed_vbox.addLayout(speed_hbox)
        self.h_speed_line_edit.setText(str(self.add_h_speed))
        self.v_speed_line_edit.setText(str(self.add_v_speed))
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
        self.h_speed_line_edit.setFixedWidth(55)   
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
        self.v_speed_line_edit.setFixedWidth(55)   
        speed_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''') 
        keyframe_content_vbox.addLayout(speed_vbox)
        self.h_speed_line_edit.editingFinished.connect(lambda:self.changedHSpeedLineEdit(index))
        self.v_speed_line_edit.editingFinished.connect(lambda:self.changedVSpeedLineEdit(index))

        accel_vbox=QVBoxLayout()
        accel_hbox=QHBoxLayout()
        accel_label=QLabel("Accel:")
        self.h_accel_line_edit=QLineEdit()
        self.v_accel_line_edit=QLineEdit()
        accel_hbox.addWidget(self.h_accel_line_edit)
        accel_hbox.addWidget(self.v_accel_line_edit)
        accel_vbox.addWidget(accel_label)
        accel_vbox.addLayout(accel_hbox)
        self.h_accel_line_edit.setText(str(self.add_h_accel))
        self.v_accel_line_edit.setText(str(self.add_v_accel))
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
        self.h_accel_line_edit.setFixedWidth(55)   
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
        self.v_accel_line_edit.setFixedWidth(55)   
        accel_label.setStyleSheet('''QLabel {
                                                font-family: 'Roboto';
                                                font-size: 12px;
                                                color:#e0e0e0;
                                                font-weight:bold;
                                                
                                                    }''') 
        keyframe_content_vbox.addLayout(accel_vbox)
        self.h_accel_line_edit.editingFinished.connect(lambda:self.changedHAccelLineEdit(index))
        self.v_accel_line_edit.editingFinished.connect(lambda:self.changedVAccelLineEdit(index))
        
        del_keyframe_hbox=QHBoxLayout()
        keyframe_content_vbox.addSpacing(12)
        self.del_keyframe_btn=QPushButton("Delete")
        del_keyframe_hbox.addWidget(self.del_keyframe_btn)
        del_keyframe_hbox.setAlignment(self.del_keyframe_btn,Qt.AlignCenter)
        keyframe_content_vbox.addLayout(del_keyframe_hbox)
        self.del_keyframe_btn.setFixedSize(120,30)
        self.del_keyframe_btn.setStyleSheet(''' 
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
        self.del_keyframe_btn.clicked.connect(lambda: self.clicked_btn_del(index))

        keyframe_content_vbox.setSpacing(16) 
        self.keyframe_content_widget.setLayout(keyframe_content_vbox)
        self.keyframe_content_widget.setVisible(False)


        keyframe_layout.addWidget(self.keyframe_content_widget) 

        self.keyframes_vbox.addLayout(keyframe_layout)
        self.keyframe_layouts.append(keyframe_layout)
        self.keyframe_btns.append(self.keyframe_btn_widget)
        self.keyframe_accel_enable_check_boxs.append(keyframe_accel_enable_check_box)
        self.keyframe_delay_line_edits.append(keyframe_delay_line_edit)
        self.keyframe_h_deg_line_edits.append(self.h_position_line_edit)
        self.keyframe_v_deg_line_edits.append(self.v_position_line_edit)        
        self.keyframe_h_speed_line_edits.append(self.h_speed_line_edit)
        self.keyframe_v_speed_line_edits.append(self.v_speed_line_edit)
        self.keyframe_h_accel_line_edits.append(self.h_accel_line_edit)
        self.keyframe_v_accel_line_edits.append(self.v_accel_line_edit)
        self.keyframe_del_btns.append(self.del_keyframe_btn)

        self.keyframe_delay_texts.append(self.add_delay)
        self.keyframe_h_deg_texts.append(self.add_h_deg)
        self.keyframe_v_deg_texts.append(self.add_v_deg)  
        self.keyframe_h_speed_texts.append(self.add_h_speed)
        self.keyframe_v_speed_texts.append(self.add_v_speed)
        self.keyframe_h_accel_texts.append(self.add_h_accel)
        self.keyframe_v_accel_texts.append(self.add_v_accel)

        self.keyframe_count+=1

    def clicked_btn_keyframe(self,index):
        for i,layout in enumerate(self.keyframe_layouts):
            if i==index:
                if layout.itemAt(1).widget().isVisible(): 
                   layout.itemAt(1).widget().setVisible(False)
                   pixmap=QPixmap('files/styles/down.png')
                   self.keyframe_btns[index].layout().itemAt(1).widget().setPixmap(pixmap)
                else:
                   layout.itemAt(1).widget().setVisible(True)
                   pixmap=QPixmap('files/styles/up.png')
                   self.keyframe_btns[index].layout().itemAt(1).widget().setPixmap(pixmap)

        



    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item=layout.takeAt(0)
                widget=item.widget()
                if widget is not None:
                    widget.deleteLater()
                else :
                    self.clear_layout(item.layout())
                    
    def clicked_btn_del(self,index):
        layout=self.keyframe_layouts[index]
        self.clear_layout(layout)   
        self.keyframes_vbox.removeItem(layout)
        self.keyframe_layouts.pop(index)
        self.keyframe_btns.pop(index)
        self.keyframe_accel_enable_check_boxs.pop(index)
        self.keyframe_delay_line_edits.pop(index)
        self.keyframe_h_deg_line_edits.pop(index)
        self.keyframe_v_deg_line_edits.pop(index)
        self.keyframe_h_speed_line_edits.pop(index)
        self.keyframe_v_speed_line_edits.pop(index)
        self.keyframe_h_accel_line_edits.pop(index)
        self.keyframe_v_accel_line_edits.pop(index)
        self.keyframe_del_btns.pop(index)

        self.keyframe_delay_texts.pop(index)
        self.keyframe_h_deg_texts.pop(index)
        self.keyframe_v_deg_texts.pop(index)
        self.keyframe_h_speed_texts.pop(index)
        self.keyframe_v_speed_texts.pop(index)
        self.keyframe_h_accel_texts.pop(index)
        self.keyframe_v_accel_texts.pop(index)


        for i in range(index, len(self.keyframe_layouts)):
          self.keyframe_accel_enable_check_boxs[i].stateChanged.disconnect()
          self.keyframe_delay_line_edits[i].editingFinished.disconnect()
          self.keyframe_h_deg_line_edits[i].editingFinished.disconnect()
          self.keyframe_v_deg_line_edits[i].editingFinished.disconnect()
          self.keyframe_h_speed_line_edits[i].editingFinished.disconnect()
          self.keyframe_v_speed_line_edits[i].editingFinished.disconnect()
          self.keyframe_h_accel_line_edits[i].editingFinished.disconnect()
          self.keyframe_v_accel_line_edits[i].editingFinished.disconnect()
          self.keyframe_del_btns[i].clicked.disconnect()

          self.keyframe_btns[i].mousePressEvent = lambda event, i=i: self.clicked_btn_keyframe(i) if event.button() == Qt.LeftButton else None
          self.keyframe_accel_enable_check_boxs[i].stateChanged.connect(lambda _, i=i: self.changedAccelEnableCheckBox(i))
          self.keyframe_delay_line_edits[i].editingFinished.connect(lambda i=i: self.changedDelayLineEdit(i))
          self.keyframe_h_deg_line_edits[i].editingFinished.connect(lambda i=i: self.changedHDegLineEdit(i))
          self.keyframe_v_deg_line_edits[i].editingFinished.connect(lambda i=i: self.changedVDegLineEdit(i))
          self.keyframe_h_speed_line_edits[i].editingFinished.connect(lambda i=i: self.changedHSpeedLineEdit(i))
          self.keyframe_v_speed_line_edits[i].editingFinished.connect(lambda i=i: self.changedVSpeedLineEdit(i))
          self.keyframe_h_accel_line_edits[i].editingFinished.connect(lambda i=i: self.changedHAccelLineEdit(i))
          self.keyframe_v_accel_line_edits[i].editingFinished.connect(lambda i=i: self.changedVAccelLineEdit(i))
          self.keyframe_del_btns[i].clicked.connect(lambda _, i=i: self.clicked_btn_del(i))
          self.keyframe_btns[i].layout().itemAt(0).widget().setText(f'keyframe{i}')

        self.keyframe_count-=1
        self.delete_keyframe_signal.emit(index)

    def changedAccelEnableCheckBox(self,index):
        if self.keyframe_accel_enable_check_boxs[index].isChecked():
            state=1
        else:
            state=0
        self.edit_index_signal.emit(index)
        self.edit_keyframe_accel_enable_signal.emit(state)
    def changedDelayLineEdit(self,index):
         try:
              value=int(self.keyframe_delay_line_edits[index].text())
              if value>65535 or value <0:
                 error_dialog=ErrorDialog("Delay at leat 0 and maximum 65535!!")
                 error_dialog.exec_() 
                 self.keyframe_delay_line_edits[index].setText(str(self.keyframe_delay_texts[index]))                     
              else :    
                 self.keyframe_delay_line_edits[index].setText(str(value))
                 self.keyframe_delay_texts[index]=value
                 self.edit_index_signal.emit(index)
                 self.edit_keyframe_delay_signal.emit(value)

         except ValueError:
              error_dialog=ErrorDialog("Please enter Integer value!! ")
              error_dialog.exec_() 
              self.keyframe_delay_line_edits[index].setText(str(self.keyframe_delay_texts[index]))                     
    def changedHDegLineEdit(self,index):
        try:
              value=float(self.keyframe_h_deg_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_h_deg_line_edits[index].setText(str(value))
              self.keyframe_h_deg_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_h_deg_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_h_deg_line_edits[index].setText(str(self.keyframe_h_deg_texts[index]))      
    def changedVDegLineEdit(self,index):
        try:
              value=float(self.keyframe_v_deg_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_v_deg_line_edits[index].setText(str(value))
              self.keyframe_v_deg_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_v_deg_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_v_deg_line_edits[index].setText(str(self.keyframe_v_deg_texts[index]))            
    def changedHSpeedLineEdit(self,index):
        try:
              value=float(self.keyframe_h_speed_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_h_speed_line_edits[index].setText(str(value))
              self.keyframe_h_speed_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_h_speed_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_h_speed_line_edits[index].setText(str(self.keyframe_h_speed_texts[index]))       
    def changedVSpeedLineEdit(self,index):
        try:
              value=float(self.keyframe_v_speed_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_v_speed_line_edits[index].setText(str(value))
              self.keyframe_v_speed_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_v_speed_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_v_speed_line_edits[index].setText(str(self.keyframe_v_speed_texts[index]))
    def changedHAccelLineEdit(self,index):
        try:
              value=float(self.keyframe_h_accel_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_h_accel_line_edits[index].setText(str(value))
              self.keyframe_h_accel_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_h_accel_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_h_accel_line_edits[index].setText(str(self.keyframe_h_accel_texts[index]))
    def changedVAccelLineEdit(self,index):
        try:
              value=float(self.keyframe_v_accel_line_edits[index].text())
              if self.mode==2:
                  value=int(round(value))
              elif self.mode==4:
                  value=round(value,1)
              elif self.mode==8:
                  value=round(value,2)        
              elif self.mode==16:
                  value=round(value,3)   
              self.keyframe_v_accel_line_edits[index].setText(str(value))
              self.keyframe_v_accel_texts[index]=value
              self.edit_index_signal.emit(index)
              self.edit_keyframe_v_accel_signal.emit(value)
        except ValueError:
              error_dialog=ErrorDialog("Please enter numeric value!! ")
              error_dialog.exec_() 
              self.keyframe_v_accel_line_edits[index].setText(str(self.keyframe_v_accel_texts[index]))

    def get_h_deg_keyframe(self,deg):
        self.add_h_deg=deg
    def get_v_deg_keyframe(self,deg):
        self.add_v_deg=deg
    def get_h_speed_keyframe(self,speed):
        self.add_h_speed=speed
    def get_v_speed_keyframe(self,speed):
        self.add_v_speed=speed    
    def get_h_accel_keyframe(self,accel):
        self.add_h_accel=accel
    def get_v_accel_keyframe(self,accel):
        self.add_v_accel=accel    
    def get_add_accel_enable(self,enable):
        self.add_accel_enable=enable
    def get_add_delay(self,delay):
        self.add_delay=delay
    def changedMode(self,mode):
        self.mode=mode
        self.movement_layout.mode_signal.emit(mode)
        for i in range(len(self.keyframe_layouts)):
           self.changedHDegLineEdit(i)
           self.changedVDegLineEdit(i)
           self.changedHSpeedLineEdit(i)
           self.changedVSpeedLineEdit(i)
           self.changedHAccelLineEdit(i)
           self.changedVAccelLineEdit(i)
    
            





        




 