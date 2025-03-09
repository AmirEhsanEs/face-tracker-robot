import os.path
import pickle

class Setting:
     def __init__(self,enable,step_mode
                      ,horizontal_max_speed,vertical_max_speed
                      ,accel_enable,horizontal_accel,vertical_accel
                      ,horizontal_hall_offset_degrees,verticall_hall_offset_degrees
                      ,automatic_track,detect_hand,move_invrement
                      ):
          self.enable=enable
          self.step_mode=step_mode
          self.horizontal_max_speed=horizontal_max_speed
          self.vertical_max_speed=vertical_max_speed
          self.accel_enable=accel_enable
          self.horizontal_accel=horizontal_accel
          self.vertical_accel=vertical_accel
          self.horizontal_hall_offset_degrees=horizontal_hall_offset_degrees
          self.verticall_hall_offset_degrees=verticall_hall_offset_degrees
          self.automatic_track=automatic_track
          self.detect_hand=detect_hand
          self.move_invrement=move_invrement


def get_saved_setting(): 
    if not(os.path.isfile('./setting.txt')):
         setting=Setting(1,16,
                            18.000,10.000,
                            0,4.000,1.000,
                            0,0,
                            1,1,1.000
                            )
         f=open('setting.txt','wb')
         pickle.dump(setting,f)
    f=open('setting.txt','rb')
    setting=pickle.load(f)
    return setting

def save_setting(setting):
        with open('setting.txt', 'wb') as f:
           pickle.dump(setting, f) 
              

