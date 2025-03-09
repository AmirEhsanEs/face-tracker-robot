from PyQt5.QtWidgets import (QHBoxLayout,QFrame)
from files.layouts.bottom_left_layout import BottomLeftLayout
from files.layouts.bottom_center_layout import BottomCenterLayout
from files.layouts.bottom_right_layout import BottomRightLayout
from PyQt5.QtCore import pyqtSignal as Signal


class BottomLayout(QFrame):
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
     
     add_h_deg_signal=Signal(float)
     add_v_deg_signal=Signal(float)
     add_h_speed_signal=Signal(float)
     add_v_speed_signal=Signal(float)
     add_h_accel_signal=Signal(float)
     add_v_accel_signal=Signal(float)
     add_accel_enable_signal=Signal(int)
     add_delay_signal=Signal(int)
     create_keyframe_signal=Signal()

     edit_index_signal=Signal(int)
     edit_keyframe_accel_enable_signal=Signal(int)
     edit_keyframe_delay_signal=Signal(int)
     edit_keyframe_h_deg_signal=Signal(float)
     edit_keyframe_v_deg_signal=Signal(float)
     edit_keyframe_h_speed_signal=Signal(float)
     edit_keyframe_v_speed_signal=Signal(float)
     edit_keyframe_h_accel_signal=Signal(float)
     edit_keyframe_v_accel_signal=Signal(float)
     delete_keyframe_signal=Signal(int)

     
     def __init__(self,setting):
           super().__init__()
           self.setting=setting
           layout=QHBoxLayout()
           self.create_bottom_left_layout=BottomLeftLayout()
           self.create_bottom_center_layout=BottomCenterLayout()
           self.create_bottom_right_layout=BottomRightLayout(setting)
           layout.addWidget(self.create_bottom_left_layout)
           layout.addWidget(self.create_bottom_center_layout)
           layout.addWidget(self.create_bottom_right_layout)
           layout.setStretch(0,1)
           layout.setStretch(1,3)
           layout.setStretch(2,1)
           layout.setContentsMargins(0,0,0,0)
           layout.setSpacing(0)   
           self.setLayout(layout)
          
           self.create_bottom_center_layout.btn_zomm_in_signal.connect(self.btn_zomm_in_signal)
           self.create_bottom_center_layout.btn_zoom_out_signal.connect(self.btn_zoom_out_signal)
           self.create_bottom_center_layout.btn_take_photo_signal.connect(self.btn_take_photo_signal)
           self.create_bottom_center_layout.btn_record_signal.connect(self.btn_record_signal)
           self.create_bottom_center_layout.btn_up_left_signal.connect(self.btn_up_left_signal)
           self.create_bottom_center_layout.btn_up_signal.connect(self.btn_up_signal)
           self.create_bottom_center_layout.btn_up_right_signal.connect(self.btn_up_right_signal)
           self.create_bottom_center_layout.btn_left_signal.connect(self.btn_left_signal)
           self.create_bottom_center_layout.btn_home_signal.connect(self.btn_home_signal)
           self.create_bottom_center_layout.btn_right_signal.connect(self.btn_right_signal)
           self.create_bottom_center_layout.btn_down_left_signal.connect(self.btn_down_left_signal)
           self.create_bottom_center_layout.btn_down_signal.connect(self.btn_down_signal)
           self.create_bottom_center_layout.btn_down_right.connect(self.btn_down_right)
           self.create_bottom_center_layout.btn_move_signal.connect(self.btn_move_signal)
           self.create_bottom_center_layout.btn_track_signal.connect(self.btn_track_signal)
           self.create_bottom_center_layout.btn_auto_home_signal.connect(self.btn_auto_home_signal)
           self.create_bottom_center_layout.btn_set_home_signal.connect(self.btn_set_home_signal)


           self.create_bottom_right_layout.motor_enable_signal.connect(self.motor_enable_signal)
           self.create_bottom_right_layout.accel_enable_signal.connect(self.accel_enable_signal)
           self.create_bottom_right_layout.auto_track_signal.connect(self.auto_track_signal)
           self.create_bottom_right_layout.hand_detect_signal.connect(self.hand_detect_signal)
           self.create_bottom_right_layout.mode_signal.connect(self.getStepMode)
           self.create_bottom_right_layout.move_increment_signal.connect(self.move_increment_signal)
           self.create_bottom_right_layout.horizontal_speed_signal.connect(self.horizontal_speed_signal)
           self.create_bottom_right_layout.vertical_speed_signal.connect(self.vertical_speed_signal)
           self.create_bottom_right_layout.horizontal_accel_signal.connect(self.horizontal_accel_signal)
           self.create_bottom_right_layout.vertical_accel_signal.connect(self.vertical_accel_signal)
           self.create_bottom_left_layout.mode_signal.emit(self.setting.step_mode)


           self.create_bottom_left_layout.move_type_signal.connect(self.move_type_signal)
           self.create_bottom_left_layout.h_move_signal.connect(self.h_move_signal)
           self.create_bottom_left_layout.v_move_signal.connect(self.v_move_signal)
           self.create_bottom_left_layout.send_start_keyframe_signal.connect(self.send_start_keyframe_signal)
           self.create_bottom_left_layout.execute_steps_signal.connect(self.execute_steps_signal)
           self.create_bottom_left_layout.pic_count_signal.connect(self.pic_count_signal)
           self.create_bottom_left_layout.deg_per_pic_signal.connect(self.deg_per_pic_signal)
           self.create_bottom_left_layout.delay_between_pic_signal.connect(self.delay_between_pic_signal)
           self.create_bottom_left_layout.btn_add_keyframe_signal.connect(self.btn_add_keyframe_signal)
           self.recieve_start_keyframe_signal.connect(self.create_bottom_left_layout.recieve_start_keyframe_signal)
           self.keyframe_count_signal.connect(self.create_bottom_left_layout.keyframe_count_signal)



           self.add_h_deg_signal.connect(self.create_bottom_left_layout.get_h_deg_keyframe)
           self.add_v_deg_signal.connect(self.create_bottom_left_layout.get_v_deg_keyframe)
           self.add_h_speed_signal.connect(self.create_bottom_left_layout.get_h_speed_keyframe)
           self.add_v_speed_signal.connect(self.create_bottom_left_layout.get_v_speed_keyframe)
           self.add_h_accel_signal.connect(self.create_bottom_left_layout.get_h_accel_keyframe)
           self.add_v_accel_signal.connect(self.create_bottom_left_layout.get_v_accel_keyframe)
           self.add_accel_enable_signal.connect(self.create_bottom_left_layout.get_add_accel_enable)
           self.add_delay_signal.connect(self.create_bottom_left_layout.get_add_delay)
           self.create_keyframe_signal.connect(self.create_bottom_left_layout.create_keyframe)



           self.create_bottom_left_layout.edit_index_signal.connect(self.edit_index_signal)
           self.create_bottom_left_layout.edit_keyframe_accel_enable_signal.connect(self.edit_keyframe_accel_enable_signal)
           self.create_bottom_left_layout.edit_keyframe_delay_signal.connect(self.edit_keyframe_delay_signal)
           self.create_bottom_left_layout.edit_keyframe_h_deg_signal.connect(self.edit_keyframe_h_deg_signal)
           self.create_bottom_left_layout.edit_keyframe_v_deg_signal.connect(self.edit_keyframe_v_deg_signal)
           self.create_bottom_left_layout.edit_keyframe_h_speed_signal.connect(self.edit_keyframe_h_speed_signal)
           self.create_bottom_left_layout.edit_keyframe_v_speed_signal.connect(self.edit_keyframe_v_speed_signal)
           self.create_bottom_left_layout.edit_keyframe_h_accel_signal.connect(self.edit_keyframe_h_accel_signal)
           self.create_bottom_left_layout.edit_keyframe_v_accel_signal.connect(self.edit_keyframe_v_accel_signal)
           self.create_bottom_left_layout.delete_keyframe_signal.connect(self.delete_keyframe_signal)
           
     def getStepMode(self,mode):
         self.mode_signal.emit(mode)
         self.create_bottom_left_layout.mode_signal.emit(mode)


           
                  
           



