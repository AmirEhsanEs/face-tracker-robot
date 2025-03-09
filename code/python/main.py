import sys
import cv2,imutils
from PyQt5.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,
                             QWidget,QDialog,QMessageBox)
from PyQt5.QtCore import pyqtSignal as Signal,pyqtSlot as Slot,Qt
from PyQt5.QtGui import QImage,QPixmap
import requests
import numpy as np
import time
import struct
from files.layouts.top_layout import TopLayout
from files.layouts.bottom_layout import BottomLayout

from files.dialogs.camera_connection_dialog import CameraConnectDialog,CameraConnectionInfo
from files.dialogs.device_connection_dialog import DeviceConnectionDialog,DeviceConnectionInfo
from files.dialogs.error_dialog import ErrorDialog

from files.connection.device import SerialConnection
from files.connection.camera import CameraThread

from files.storage.storage import get_saved_setting 
from files.storage.storage import save_setting 

import mediapipe as mp



class MainWindow(QMainWindow):
    keyframe_count_signal=Signal(int)
    recieve_start_keyframe_signal=Signal(int)
    add_h_deg_signal=Signal(float)
    add_v_deg_signal=Signal(float)
    add_h_speed_signal=Signal(float)
    add_v_speed_signal=Signal(float)
    add_h_accel_signal=Signal(float)
    add_v_accel_signal=Signal(float)
    add_accel_enable_signal=Signal(int)
    add_delay_signal=Signal(int)
    create_keyframe_signal=Signal() 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ETracker")
        self.camera_connected=False        
        self.device_connected=False
        self.face_tracking=False
        self.start_record=False
        self.setting=get_saved_setting()
        self.camera_thread=CameraThread()
        self.device_connection=SerialConnection()
        self.top_layout=TopLayout()
        self.bottom_layout=BottomLayout(self.setting)

        if not(self.setting.automatic_track):
           if not self.setting.accel_enable:
               self.camera_thread.x_kp=0.042
               self.camera_thread.y_kp=0.042
           else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062
        else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062       
                      


        self.mod=0
        self.camera_thread.disconnect_signal.connect(self.getCameraDisconnectMessage)
        self.camera_thread.frame_signal.connect(self.setImage)
        self.camera_thread.x_output_signal.connect(self.getXout)
        self.camera_thread.y_output_signal.connect(self.getYout)
        self.camera_thread.face_x_signal.connect(self.getFaceCenterX)
        self.camera_thread.face_y_signal.connect(self.getFaceCenterY)
        self.device_connection.disconected_signal.connect(self.getDeviceDisconnectMessage)
        self.device_connection.response_signal.connect(self.getDeviceResponse)
        self.top_layout.btn_camera_connect_signal.connect(self.click_btn_connect_camera)
        self.top_layout.btn_device_connect_signal.connect(self.click_btn_connect_device)
        self.top_layout.btn_restart_signal.connect(self.click_btn_restart)  


        self.bottom_layout.btn_zomm_in_signal.connect(self.click_btn_zoom_in)
        self.bottom_layout.btn_zoom_out_signal.connect(self.click_btn_zoom_out)
        self.bottom_layout.btn_take_photo_signal.connect(self.click_btn_take_photo)
        self.bottom_layout.btn_record_signal.connect(self.click_btn_record)
        self.bottom_layout.btn_up_left_signal.connect(self.click_btn_up_left)
        self.bottom_layout.btn_up_signal.connect(self.click_btn_up)
        self.bottom_layout.btn_up_right_signal.connect(self.click_btn_up_right)
        self.bottom_layout.btn_left_signal.connect(self.click_btn_left)
        self.bottom_layout.btn_home_signal.connect(self.click_btn_home)
        self.bottom_layout.btn_right_signal.connect(self.click_btn_right)
        self.bottom_layout.btn_down_left_signal.connect(self.click_btn_down_left)
        self.bottom_layout.btn_down_signal.connect(self.click_btn_down)
        self.bottom_layout.btn_down_right.connect(self.click_btn_down_right)
        self.bottom_layout.btn_move_signal.connect(self.click_btn_move)
        self.bottom_layout.btn_track_signal.connect(self.click_btn_track)
        self.bottom_layout.btn_auto_home_signal.connect(self.click_btn_auto_home)
        self.bottom_layout.btn_set_home_signal.connect(self.click_btn_set_home)



        self.bottom_layout.motor_enable_signal.connect(self.getMotorEnable)
        self.bottom_layout.accel_enable_signal.connect(self.getAccelEnable)
        self.bottom_layout.auto_track_signal.connect(self.getAutoTrack)
        self.bottom_layout.hand_detect_signal.connect(self.getHandDetect)
        self.bottom_layout.mode_signal.connect(self.getStepMode)
        self.bottom_layout.move_increment_signal.connect(self.getMoveIncrement)
        self.bottom_layout.horizontal_speed_signal.connect(self.getHorizontalSpeed)
        self.bottom_layout.vertical_speed_signal.connect(self.getVerticalSpeed)
        self.bottom_layout.horizontal_accel_signal.connect(self.getHorizontalAccel)
        self.bottom_layout.vertical_accel_signal.connect(self.getVerticalAccel)

        
        self.bottom_layout.move_type_signal.connect(self.getMoveType)
        self.bottom_layout.h_move_signal.connect(self.getHMove)
        self.bottom_layout.v_move_signal.connect(self.getVMove)
        self.bottom_layout.send_start_keyframe_signal.connect(self.getStartKeyFrame)
        self.bottom_layout.execute_steps_signal.connect(self.getExecuteSteps)
        self.bottom_layout.pic_count_signal.connect(self.getPicCount)
        self.bottom_layout.deg_per_pic_signal.connect(self.getDegPerPic)
        self.bottom_layout.delay_between_pic_signal.connect(self.getDelayBetweenPic)
        self.bottom_layout.btn_add_keyframe_signal.connect(self.getClickedAddKeyframe)

        self.recieve_start_keyframe_signal.connect(self.bottom_layout.recieve_start_keyframe_signal)
        self.keyframe_count_signal.connect(self.bottom_layout.keyframe_count_signal)


        self.add_h_deg_signal.connect(self.bottom_layout.add_h_deg_signal)
        self.add_v_deg_signal.connect(self.bottom_layout.add_v_deg_signal)
        self.add_h_speed_signal.connect(self.bottom_layout.add_h_speed_signal)
        self.add_v_speed_signal.connect(self.bottom_layout.add_v_speed_signal)
        self.add_h_accel_signal.connect(self.bottom_layout.add_h_accel_signal)
        self.add_v_accel_signal.connect(self.bottom_layout.add_v_accel_signal)
        self.add_accel_enable_signal.connect(self.bottom_layout.add_accel_enable_signal)
        self.add_delay_signal.connect(self.bottom_layout.add_delay_signal)
        self.create_keyframe_signal.connect(self.bottom_layout.create_keyframe_signal)

        self.bottom_layout.edit_index_signal.connect(self.getEditIndex)
        self.bottom_layout.edit_keyframe_accel_enable_signal.connect(self.getEditAccelEnable)
        self.bottom_layout.edit_keyframe_delay_signal.connect(self.getEditDelay)
        self.bottom_layout.edit_keyframe_h_deg_signal.connect(self.getEditHDeg)
        self.bottom_layout.edit_keyframe_v_deg_signal.connect(self.getEditVDeg)
        self.bottom_layout.edit_keyframe_h_speed_signal.connect(self.getEditHSpeed)
        self.bottom_layout.edit_keyframe_v_speed_signal.connect(self.getEditVSpeed)
        self.bottom_layout.edit_keyframe_h_accel_signal.connect(self.getEditHAccel)
        self.bottom_layout.edit_keyframe_v_accel_signal.connect(self.getEditVAccel)
        self.bottom_layout.delete_keyframe_signal.connect(self.getDeleteKeyframe)


        self.main_content_layout()
        self.showMaximized()
        self.move_type=0
        self.h_move=None
        self.v_move=None
        self.start_keyframe=None
        self.execute_steps=None
        self.pic_count=None
        self.deg_per_pic=None
        self.delay_between_pic=None
        self.keyframe_count=0

    
    def main_content_layout(self):
        main_widget=QWidget()
        main_layout=QVBoxLayout()
        main_layout.addWidget(self.top_layout)
        main_layout.addWidget(self.bottom_layout)
        main_layout.setStretch(0,1)
        main_layout.setStretch(1,15)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def start_camera_connection(self):
        while True:    
            self.camera_connect_dialog=CameraConnectDialog()
            result=self.camera_connect_dialog.exec_()
            if result==QDialog.Accepted:
                self.camera_thread.set_url(self.camera_connect_dialog.url)
                self.camera_thread.start_webcam()
                if self.camera_thread.running:
                    self.camera_connected=True
                    self.top_layout.camera_connection_btn.setStyleSheet("""QPushButton {
                                        border: 1px solid black; 
                                        background-color: #2c592c;                                                                        
                                        font-size: 20px;
                                        font-weight: bold;
                                        border-radius:10px;
                                    }

                                """)
                    break
                else:
                    error_dialog=ErrorDialog("Cannot connect to this ip:port ")
                    error_dialog.exec_()
            else :
                break
    
    def stop_camera_connection(self):
        self.camera_thread.stop_webcam()
        self.camera_connected=False  
        self.bottom_layout.create_bottom_center_layout.video.clear()
        self.top_layout.camera_connection_btn.setStyleSheet("""QPushButton {
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
        self.bottom_layout.create_bottom_center_layout.face_center_x=''   
        self.bottom_layout.create_bottom_center_layout.face_center_y=''
        self.bottom_layout.create_bottom_center_layout.set_face_pos() 

    def start_device_connection(self):
            while True:    
                self.device_connect_dialog=DeviceConnectionDialog()
                result=self.device_connect_dialog.exec_()
                if result==QDialog.Accepted:
                        self.device_connection.start_device(self.device_connect_dialog.com,self.device_connect_dialog.baudrate,self.setting)
                        if self.device_connection.running:
                            self.device_connected=True
                            self.top_layout.device_connection_btn.setStyleSheet("""QPushButton {
                                            border: 1px solid black; 
                                            background-color: #2c592c;
                                            font-size: 20px;
                                            font-weight: bold;
                                            border-radius:10px;
                                        }
            
                                    """)
                            break
                        else:
                         error_dialog=ErrorDialog("Cannot connect to this com with this baudrate ")
                         error_dialog.exec_()
                else :
                    break
        
    def stop_device_connection(self):
            
            self.device_connection.stop_device()
            self.device_connected=False  
            self.top_layout.device_connection_btn.setStyleSheet("""QPushButton {
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
            self.bottom_layout.create_bottom_center_layout.device_h=''
            self.bottom_layout.create_bottom_center_layout.device_v=''
            self.bottom_layout.create_bottom_center_layout.set_device_pos()  
            self.mod=0

    def getXout(self,x_out):
        self.device_connection.send_char_to_serial('h')
        self.device_connection.send_float_to_serial(x_out)
    def getYout(self,y_out):
        self.device_connection.send_char_to_serial('v')
        self.device_connection.send_float_to_serial(y_out)
    def getFaceCenterX(self,center_x):
        self.bottom_layout.create_bottom_center_layout.face_center_x=str(center_x)
        self.bottom_layout.create_bottom_center_layout.set_face_pos() 
    
    def getFaceCenterY(self,center_y):
        self.bottom_layout.create_bottom_center_layout.face_center_y=str(center_y)
        self.bottom_layout.create_bottom_center_layout.set_face_pos() 
    
    def getMotorEnable(self,motor_enable):
        self.device_connection.send_char_to_serial('e')
        self.setting.enable=motor_enable

    def getAccelEnable(self,accel):
        self.device_connection.send_char_to_serial('c')
        self.setting.accel_enable=accel
        if not(self.setting.automatic_track):
           if not self.setting.accel_enable:
               self.camera_thread.x_kp=0.042
               self.camera_thread.y_kp=0.042
           else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062
        else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062       


    def getAutoTrack(self,auto_track):
        self.device_connection.send_char_to_serial('l')
        self.setting.automatic_track=auto_track
        if not(self.setting.automatic_track):
           if not self.setting.accel_enable:
               self.camera_thread.x_kp=0.042
               self.camera_thread.y_kp=0.042
           else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062
        else:
               self.camera_thread.x_kp=0.062
               self.camera_thread.y_kp=0.062       

                      


    def getHandDetect(self,hand_track):
        self.setting.detect_hand=hand_track
    def getStepMode(self,step_mode):
        self.device_connection.send_char_to_serial('m')
        self.device_connection.send_byte_to_serial(step_mode)
        self.setting.step_mode=step_mode
        if self.device_connected:
            value1=float(self.bottom_layout.create_bottom_center_layout.device_h)
            value2=float(self.bottom_layout.create_bottom_center_layout.device_v)
            if step_mode == 2:
                value1 = int(round(value1))
                value2 = int(round(value2))
                value1_str = f"{value1:.0f}"  
                value2_str = f"{value2:.0f}"  
            elif step_mode == 4:
                value1 = round(value1, 1)
                value2 = round(value2, 1)
                value1_str = f"{value1:.1f}"  
                value2_str = f"{value2:.1f}" 
            elif step_mode == 8:
                value1 = round(value1, 2)
                value2 = round(value2, 2)
                value1_str = f"{value1:.2f}" 
                value2_str = f"{value2:.2f}"  
            elif step_mode == 16:
                value1 = round(value1, 3)
                value2 = round(value2, 3)
                value1_str = f"{value1:.3f}"  
                value2_str = f"{value2:.3f}"  

            self.device_connection.send_char_to_serial('Z')              
            self.device_connection.send_float_to_serial(value1)
            self.device_connection.send_float_to_serial(value2)
            self.bottom_layout.create_bottom_center_layout.device_h=value1_str
            self.bottom_layout.create_bottom_center_layout.device_v=value2_str
            self.bottom_layout.create_bottom_center_layout.set_device_pos()  

    def getMoveIncrement(self,increment):
        self.device_connection.send_char_to_serial('x')
        self.device_connection.send_float_to_serial(increment)
        self.setting.move_invrement=increment

    def getHorizontalSpeed(self,speed):
        self.device_connection.send_char_to_serial('s')
        self.device_connection.send_float_to_serial(speed)
        self.setting.horizontal_max_speed=speed

    def getVerticalSpeed(self,speed):
        self.device_connection.send_char_to_serial('S')
        self.device_connection.send_float_to_serial(speed)
        self.setting.vertical_max_speed=speed

    def getHorizontalAccel(self,accel):
        self.device_connection.send_char_to_serial('a')
        self.device_connection.send_float_to_serial(accel)
        self.setting.horizontal_accel=accel

    def getVerticalAccel(self,accel):
        self.device_connection.send_char_to_serial('A')
        self.device_connection.send_float_to_serial(accel)
        self.setting.vertical_accel=accel

    def getMoveType(self,move_type):
        self.move_type=move_type
    
    def getHMove(self,h_deg):
        self.h_move=h_deg
    
    def getVMove(self,v_deg):
        self.v_move=v_deg

    def getStartKeyFrame(self,start_index):
        self.start_keyframe=start_index
        self.device_connection.send_char_to_serial('i')
        self.device_connection.send_Int8_to_serial(start_index)
    
    def getExecuteSteps(self,count):
        self.execute_steps=count
        self.device_connection.send_char_to_serial('I')
        self.device_connection.send_Int8_to_serial(count)
        
    def  getPicCount(self,count):
         self.pic_count=count
         self.device_connection.send_char_to_serial('n')
         self.device_connection.send_unsigned_int_to_serial(count)
         
    def getDegPerPic(self,deg_per_pic):
         self.deg_per_pic=deg_per_pic
         self.device_connection.send_char_to_serial('b')
         self.device_connection.send_float_to_serial(deg_per_pic)

    def getDelayBetweenPic(self,delay):
        self.delay_between_pic=delay
        self.device_connection.send_char_to_serial('B')
        self.device_connection.send_unsigned_int_to_serial(delay)

    def getClickedAddKeyframe(self):
        self.device_connection.send_char_to_serial('p')        

    def getEditIndex(self,index):
        self.edit_index=index

    def getEditAccelEnable(self,state):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(0)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_byte_to_serial(state)
 
    def getEditDelay(self,delay):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(1)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_short_int_to_serial(delay)


    def getEditHDeg(self,deg):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(2)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(deg)

    def getEditVDeg(self,deg):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(3)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(deg)

    def getEditHSpeed(self,speed):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(4)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(speed)


    def getEditVSpeed(self,speed):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(5)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(speed)

    def getEditHAccel(self,accel):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(6)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(accel)


    def getEditVAccel(self,accel):
        self.device_connection.send_char_to_serial('L')
        self.device_connection.send_byte_to_serial(7)
        self.device_connection.send_byte_to_serial(self.edit_index)
        self.device_connection.send_float_to_serial(accel)

    
    def getDeleteKeyframe(self,index):
        self.device_connection.send_char_to_serial('d')
        self.device_connection.send_byte_to_serial(index)


    @Slot()
    def getCameraDisconnectMessage(self):
        self.camera_connected=False  
        self.bottom_layout.create_bottom_center_layout.video.clear()
        self.top_layout.camera_connection_btn.setStyleSheet("""QPushButton {
                                        background-color: #212121;
                                        border: 1px solid black; 
                                        font-size: 20px;
                                        font-weight: bold;
                                        border-radius:10px
                                    }
                                    QPushButton:hover {
                                        border: 1px solid black; 
                                        background-color: #ECDFCC;
                                    }
                                """) 

        error_dialog=ErrorDialog("Camera is disconnected!")
        error_dialog.exec_() 

    @Slot(QImage)
    def setImage(self,image):
         if self.camera_thread.running:
           self.bottom_layout.create_bottom_center_layout.video.setPixmap(QPixmap.fromImage(image)) 


    @Slot()
    def getDeviceDisconnectMessage(self):
         self.stop_device_connection()            
         error_dialog=ErrorDialog("Device is disconnected!!")
         error_dialog.exec_()

  
    @Slot(str)
    def getDeviceResponse(self,response):
      if self.device_connection.running:  
        spilited_response=self.spilit(response)
        if spilited_response[0]=='e':
            self.mod=0
        elif self.mod==0:
            if spilited_response[0]=='t':
                self.mod=1
            elif spilited_response[0]=='h':
                 self.mod=2
            elif spilited_response[0]=='v':
                self.mod=3
            elif spilited_response[0]=='m':
                 self.mod=4   
            elif spilited_response[0]=='x':
                 self.keyframe_count-=1
                 self.keyframe_count_signal.emit(self.keyframe_count)
                 self.recieve_start_keyframe_signal.emit(int(spilited_response[1]))
            elif spilited_response[0]=='p':
                 self.add_h_deg_signal.emit(float(spilited_response[1]))
                 self.add_v_deg_signal.emit(float(spilited_response[2]))
                 self.add_h_speed_signal.emit(self.setting.horizontal_max_speed)
                 self.add_v_speed_signal.emit(self.setting.vertical_max_speed)
                 self.add_h_accel_signal.emit(self.setting.horizontal_accel)
                 self.add_v_accel_signal.emit(self.setting.vertical_accel)
                 self.add_accel_enable_signal.emit(self.setting.accel_enable)
                 self.add_delay_signal.emit(0)
                 self.create_keyframe_signal.emit()
                 self.keyframe_count_signal.emit(int(spilited_response[3]))
                 if self.keyframe_count==0 and int(spilited_response[3])==1:
                     self.recieve_start_keyframe_signal.emit(0) 
                 self.keyframe_count=int(spilited_response[3])
  
            elif spilited_response[0]=='o':
                 self.setting.horizontal_hall_offset_degrees=float(spilited_response[1])
                 self.setting.verticall_hall_offset_degrees=float(spilited_response[2])

            else :
                print(f'response:{spilited_response[0]}')     
                      
     
        elif self.mod==1:
             self.bottom_layout.create_bottom_center_layout.device_h=spilited_response[0]
             self.bottom_layout.create_bottom_center_layout.device_v=spilited_response[1]
             self.bottom_layout.create_bottom_center_layout.set_device_pos()  
        elif self.mod==2:
             self.bottom_layout.create_bottom_center_layout.device_h=spilited_response[0]
             self.bottom_layout.create_bottom_center_layout.set_device_pos()    
        elif self.mod==3:
             self.bottom_layout.create_bottom_center_layout.device_v=spilited_response[0]
             self.bottom_layout.create_bottom_center_layout.set_device_pos()  
        elif self.mod==4:
            if len(spilited_response)==1:
                 if spilited_response[0]=='f':
                      self.camera_thread.take_snapshot() 
                 elif spilited_response[0]=='w':
                      self.camera_thread.start_recording()
                      self.start_record=True
                      self.bottom_layout.create_bottom_center_layout.btn_record.setText('Stop')        
                 elif spilited_response[0]=='W':
                      self.camera_thread.stop_recording()
                      self.start_record=False
                      self.bottom_layout.create_bottom_center_layout.btn_record.setText('Record')
                 else: 
                    self.start_keyframe=int(spilited_response[0])   
                    self.recieve_start_keyframe_signal.emit(int(spilited_response[0]))   
            else :
                self.bottom_layout.create_bottom_center_layout.device_h=spilited_response[0]
                self.bottom_layout.create_bottom_center_layout.device_v=spilited_response[1]
                self.bottom_layout.create_bottom_center_layout.set_device_pos()  

        
    #click button actions
    def click_btn_connect_camera(self):
         if self.camera_connected==False:    
            self.start_camera_connection()
         else:
            camera_connect__info_dialog=CameraConnectionInfo(self.camera_connect_dialog.ip,self.camera_connect_dialog.port)
            if camera_connect__info_dialog.exec_()==QDialog.Accepted:
               if self.mod==0:
                  self.stop_camera_connection()      
  

    def click_btn_connect_device(self):
         if self.device_connected==False:
            self.start_device_connection() 
         else:
            device_connect_info_dialog=DeviceConnectionInfo(self.device_connect_dialog.com,self.device_connect_dialog.baudrate)
            if device_connect_info_dialog.exec_()==QDialog.Accepted:
                if self.mod==0:
                     self.stop_device_connection() 


    def click_btn_restart(self):
             print('c')
   
    def click_btn_zoom_in(self):
       if self.camera_connected:   
           self.camera_thread.zoom_in()
       else:                  
         error_dialog=ErrorDialog("Camera is not connected!")
         error_dialog.exec_()

    def click_btn_zoom_out(self):
       if self.camera_connected:   
           self.camera_thread.zoom_out()
       else:
         error_dialog=ErrorDialog("Camera is not connected!")
         error_dialog.exec_()
       
    def click_btn_take_photo(self):
      if self.mod!=4:  
         if self.camera_connected:  
             self.camera_thread.take_snapshot()
         else:
            error_dialog=ErrorDialog("Camera is not connected!")
            error_dialog.exec_()
        
      else :
           error_dialog=ErrorDialog("Device in photography mode!!")
           error_dialog.exec_()

    def click_btn_record(self): 
       if self.mod!=4: 
          if self.camera_connected:       
              if self.start_record:
                self.camera_thread.stop_recording()
                self.start_record=False
                self.bottom_layout.create_bottom_center_layout.btn_record.setText('Record')
              else: 
                self.camera_thread.start_recording()
                self.start_record=True
                self.bottom_layout.create_bottom_center_layout.btn_record.setText('Stop')
          else:
           error_dialog=ErrorDialog("Camera is not connected!")
           error_dialog.exec_()
       else :
           error_dialog=ErrorDialog("Device in photography mode!!")
           error_dialog.exec_()
                        
    def click_btn_up_left(self):
      if self.mod==0:  
         if self.device_connected:
             self.device_connection.send_char_to_serial('g')
         else :
            error_dialog=ErrorDialog("Device is not connected!")
            error_dialog.exec_()
      else:
           error_dialog=ErrorDialog("The Device in Movement status!!")
           error_dialog.exec_()
    def click_btn_up(self):
     if self.mod==0:   
        if self.device_connected:    
            self.device_connection.send_char_to_serial('j')
        else :
            error_dialog=ErrorDialog("Device is not connected!")
            error_dialog.exec_()
     else:
            error_dialog=ErrorDialog("The Device in Movement status!!")
            error_dialog.exec_() 
             
    def click_btn_up_right(self):
      if self.mod==0:
         if self.device_connected:    
             self.device_connection.send_char_to_serial('w')
         else :
            error_dialog=ErrorDialog("Device is not connected!")
            error_dialog.exec_()
      else:
            error_dialog=ErrorDialog("The Device in Movement status!!")
            error_dialog.exec_()  

    def click_btn_left(self):
     if self.mod==0: 
        if self.device_connected:   
            self.device_connection.send_char_to_serial('k')
        else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_()  
     else:
             error_dialog=ErrorDialog("The Device in Movement status!!")
             error_dialog.exec_()  

    def click_btn_home(self):
      if self.mod==0:  
         if self.device_connected:
            self.device_connection.send_char_to_serial('F')
         else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_()  
      else:
             error_dialog=ErrorDialog("The Device in Movement status!!")
             error_dialog.exec_()  
    def click_btn_right(self):
       if self.mod==0: 
         if self.device_connected:
            self.device_connection.send_char_to_serial('K')
         else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_()  
       else:
             error_dialog=ErrorDialog("The Device in Movement status!!")
             error_dialog.exec_()  
           
    def click_btn_down_left(self):
       if self.mod==0: 
            if self.device_connected:    
                self.device_connection.send_char_to_serial('G')
            else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_()  
       else:
             error_dialog=ErrorDialog("The Device in Movement status!!")
             error_dialog.exec_()  
    def click_btn_down(self):
      if self.mod==0: 
         if self.device_connected:    
            self.device_connection.send_char_to_serial('J')
         else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_()  
      else:
             error_dialog=ErrorDialog("The Device in Movement status!!")
             error_dialog.exec_()         
    def click_btn_down_right(self):
        if self.mod==0:
           if self.device_connected:
              self.device_connection.send_char_to_serial('W')
           else :
              error_dialog=ErrorDialog("Device is not connected!")
              error_dialog.exec_()  
        else:
              error_dialog=ErrorDialog("The Device in Movement status!!")
              error_dialog.exec_()    
    def click_btn_move(self):
       if self.mod==0:      
          if self.device_connected:
              if self.move_type==0:
                  if self.h_move is None:
                        error_dialog=ErrorDialog("Please enter Hdeg!!")
                        error_dialog.exec_()  
                  elif self.v_move is None:
                        error_dialog=ErrorDialog("Please enter Vdeg!!")
                        error_dialog.exec_()  
                  else:
                        self.device_connection.send_char_to_serial('r')
                        self.device_connection.send_float_to_serial(self.h_move)
                        self.device_connection.send_float_to_serial(self.v_move)

              else:
                  if self.keyframe_count<2:
                        error_dialog=ErrorDialog("Need at least 2 keyframe!!!")
                        error_dialog.exec_()  
                  else:
                      if self.move_type==1:
                          self.device_connection.send_char_to_serial('M')
                          self.device_connection.send_byte_to_serial(0)
                      elif self.move_type==2:
                          if self.camera_connected:
                                if self.deg_per_pic is None :
                                    error_dialog=ErrorDialog("Please enter deg/pic!!!")
                                    error_dialog.exec_()  
                                elif self.delay_between_pic is None:
                                    error_dialog=ErrorDialog("Please enter delay btween pictures!!!")
                                    error_dialog.exec_()  
                                else:                                       
                                    self.device_connection.send_char_to_serial('M')
                                    self.device_connection.send_byte_to_serial(2)
                          else:
                              error_dialog=ErrorDialog("Camera is not connected")
                              error_dialog.exec_()                        
                      elif self.move_type==3:   
                          if self.camera_connected:               
                                if self.pic_count is None :
                                    error_dialog=ErrorDialog("Please enter pic count!!!")
                                    error_dialog.exec_()  
                                elif self.delay_between_pic is None:
                                    error_dialog=ErrorDialog("Please enter delay btween pictures!!!")
                                    error_dialog.exec_()                                    
                                else:                                       
                                    self.device_connection.send_char_to_serial('M')
                                    self.device_connection.send_byte_to_serial(1)
                          else :
                             error_dialog=ErrorDialog("Camera is not connected")
                             error_dialog.exec_() 
                      elif self.move_type==4:
                         if self.camera_connected:
                            if self.start_record:
                                error_dialog=ErrorDialog("Please stop recording!!!")
                                error_dialog.exec_() 
                            else:    
                                self.device_connection.send_char_to_serial('M')
                                self.device_connection.send_byte_to_serial(3)
                         else:
                           error_dialog=ErrorDialog("Camera is not connected")
                           error_dialog.exec_() 
          
          else :
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_() 

       else:
            error_dialog=ErrorDialog("The Device in Movement status!!")
            error_dialog.exec_() 
           
    def click_btn_track(self):
       if self.mod==0 or self.face_tracking: 
          if self.device_connected and self.camera_connected:
             self.camera_thread.disable_tracking()
             if self.face_tracking:
                    self.device_connection.send_char_to_serial('q')
                    self.face_tracking=False
                    self.bottom_layout.create_bottom_center_layout.btn_track.setText('Track face')
                    
             else: 
                    self.camera_thread.enable_tracking()
                    self.device_connection.send_char_to_serial('z')
                    self.face_tracking=True
                    self.bottom_layout.create_bottom_center_layout.btn_track.setText('Stop')
        
          else:
              if not(self.device_connected) and not(self.camera_connected):
                  error_dialog=ErrorDialog("Device and camera is not connected!")
                  error_dialog.exec_() 
              elif not(self.device_connected):
                    error_dialog=ErrorDialog("Device is not connected!")
                    error_dialog.exec_()   
              elif not(self.camera_connected):
                  error_dialog=ErrorDialog("Camera is not connected!")
                  error_dialog.exec_()  
                    
       else:
           error_dialog=ErrorDialog("he Device in Movement status!!")
           error_dialog.exec_()  
    def click_btn_auto_home(self):
      if self.mod==0:  
         if self.device_connected:
             self.device_connection.send_char_to_serial('U')
             self.setting.horizontal_hall_offset_degrees=0
             self.setting.verticall_hall_offset_degrees=0
     
         else:
             error_dialog=ErrorDialog("Device is not connected!")
             error_dialog.exec_() 
      else:
           error_dialog=ErrorDialog("The Device in Movement status!!")
           error_dialog.exec_() 

    def click_btn_set_home(self):
        if self.mod==0:    
            if self.device_connected:
              self.device_connection.send_char_to_serial('f')
            else:
                error_dialog=ErrorDialog("Device is not connected!")
                error_dialog.exec_() 
        else:
           error_dialog=ErrorDialog("The Device in Movement status!!")
           error_dialog.exec_() 

    #events
    def closeEvent(self,event):
        if self.mod==0:
            if self.camera_connected:
                self.stop_camera_connection()
            if self.device_connected:
                self.stop_device_connection()   
            save_setting(self.setting)
            self.bottom_layout.create_bottom_right_layout.record_layout.observer.stop()
            self.bottom_layout.create_bottom_right_layout.record_layout.observer.join()
            event.accept()
        else :
            event.ignore()    


    #spilit      
    def spilit(self,string):
        str_array=[]
        item=''
        for i in range(len(string)):
            if(string[i]!=' '):
                item=item+string[i]
            elif i<len(string)-1: 
                if string[i+1]!=' ' :
                  str_array.append(item)
                  item=''     
        str_array.append(item) 
        return str_array  


   
       
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())