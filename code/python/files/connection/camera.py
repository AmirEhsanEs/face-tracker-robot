import cv2,imutils
from PyQt5.QtCore import QThread,pyqtSignal as Signal
from PyQt5.QtGui import QImage
import time
import numpy as np
import os.path
import mediapipe as mp
import requests

from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRect

class CameraThread(QThread):
      #signals
      frame_signal=Signal(QImage)
      disconnect_signal=Signal()
      x_output_signal=Signal(float)
      y_output_signal=Signal(float)
      face_x_signal=Signal(int)
      face_y_signal=Signal(int)

      #initial function
      def __init__(self):
           super().__init__()
           self.cap=None
           self.running = False
           self.video_url=''
           self.url=''
           self.tracking=False
           self.mp_facedetect=mp.solutions.face_detection
           self.face_detector=self.mp_facedetect.FaceDetection(model_selection=1,min_detection_confidence=0.7)

           self.x_kp,self.x_ki,self.x_kd=0.062,0.0,0.0
           self.y_kp,self.y_ki,self.y_kd=0.062,0.0,0.0
           self.take_snapshot_requested=False
           self.recording=False
           self.video_writer=None
      def set_url(self,url):
            self.video_url=url +'/video' 
            self.url=url
      #photo graphy function
      def take_snapshot(self):
          self.take_snapshot_requested=True

      def save_photo(self,frame):
          if not os.path.exists('snapshots'):
              os.makedirs('snapshots')
          timestamp=time.strftime("%Y%m%d_%H%M%S")
          filename=f'snapshots/snapshot_{timestamp}.png'
          cv2.imwrite(filename,frame)

      def start_recording(self):
          if not self.recording:
              if not os.path.exists('records'):
                  os.makedirs('records')
              fourcc=cv2.VideoWriter_fourcc(*'mp4v') 
              timestamp=time.strftime("%Y%m%d_%H%M%S")
              fps=self.cap.get(cv2.CAP_PROP_FPS)
              if fps==0:
                fps=20  
              frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
              frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
              self.video_writer=cv2.VideoWriter(f'records/video_{timestamp}.mp4',fourcc,fps,(frame_width,frame_height))
              self.recording=True

      def stop_recording(self):
          if self.recording:
              self.recording=False
              self.video_writer.release()
              self.video_writer=None

      def zoom_in(self):
        zoom_url=self.url+'/cam/1/zoomin'
        response=requests.get(zoom_url)
        if response.status_code==200:
            print('request send successfully')
        else :
            print('request send unsuccessfully')



      def zoom_out(self):
        zoom_url=self.url+'/cam/1/zoomout'
        response=requests.get(zoom_url)
        if response.status_code==200:
            print('request send successfully')
        else:
            print('request send unsuccessfully')
    
               
      #face tracking function          
      def enable_tracking(self):
         self.tracking=True
         self.x_integral,self.y_integral=0.0,0.0
         self.x_prev_error,self.y_prev_error=0.0,0.0
         self.x_prev_time=time.time()
         self.y_prev_time=time.time() 

      def disable_tracking(self):
          self.tracking=False

      def set_pid_controller(self,Kp, Ki, Kd, curr_error, prev_error, prev_time, integral):
        curr_time = time.time()
        delta_time = curr_time - prev_time    
        if delta_time == 0:
            delta_time = 1e-6
        proportional = curr_error
        integral = integral + (curr_error * delta_time)
        derivative = (curr_error - prev_error) / delta_time
        output = (Kp * proportional) + (Ki * integral) + (Kd * derivative)
        return output, integral, curr_time
      
      def send_image(self, frame, radius=15):
            frame = imutils.resize(frame,width=580)
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame=QImage(frame,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(frame)
            size = pixmap.size()
            
            rounded = QPixmap(size)
            rounded.fill(Qt.transparent)  
            
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.setBrush(QBrush(pixmap))
            painter.setPen(Qt.NoPen)
            
            rect = QRect(0, 0, size.width(), size.height())
            painter.drawRoundedRect(rect, radius, radius)
            painter.end()
            
            self.frame_signal.emit(rounded.toImage())

      def track_face(self, frame):
            frame_height,frame_width,c=frame.shape
            set_point=frame_width//40
            frame=cv2.flip(frame,1)
            frame.flags.writeable=False
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result=self.face_detector.process(frame)
            frame.flags.writeable=True
            frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            if result.detections:
                for detection in result.detections:
                    box_cordinate=detection.location_data.relative_bounding_box
                    keypoints=detection.location_data.relative_keypoints
                    start_x=int(box_cordinate.xmin*frame_width)
                    start_y=int(box_cordinate.ymin*frame_height)
                    end_x=int((box_cordinate.xmin+box_cordinate.width)*frame_width)
                    end_y=int((box_cordinate.ymin+box_cordinate.height)*frame_height)
                    face_center_x=(start_x+end_x)//2
                    face_center_y=(start_y+end_y)//2
                    self.face_x_signal.emit(face_center_x)
                    self.face_y_signal.emit(face_center_y)
                    x_curr_error=face_center_x-frame_width//2
                    y_curr_error=face_center_y-frame_height//2
                    cv2.rectangle(frame,(frame_width//2 -set_point,frame_height//2-set_point),(frame_width//2+set_point,frame_height//2+set_point),(0,255,0),1)
                    cv2.circle(frame,(face_center_x,face_center_y),50,(0,255,255),5)
                    cv2.line(frame,(0,face_center_y),(frame_width,face_center_y),(0,255,255),1)
                    cv2.line(frame,(face_center_x,0),(face_center_x,frame_height),(0,255,255),1)
                    if abs(x_curr_error)>set_point:
                        x_output,self.x_integral,self.x_prev_time=self.set_pid_controller(self.x_kp,self.x_ki,self.x_kd,x_curr_error,self.x_prev_error,self.x_prev_time,self.x_integral)
                        self.x_output_signal.emit(x_output)
                        cv2.putText(frame,f'Xout:{x_output}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2)            
                    if abs(y_curr_error)>set_point:
                        y_output,self.y_integral,self.y_prev_time=self.set_pid_controller(self.y_kp,self.y_ki,self.y_kd,y_curr_error,self.y_prev_error,self.y_prev_time,self.y_integral)
                        self.y_output_signal.emit(-y_output)
                        cv2.putText(frame,f'Yout:{y_output}',(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2)            
                    
            return frame


      def run(self):    
            while self.running:
              if self.cap is not None:
                ret,image=self.cap.read()
                if ret:
                    if self.recording and self.video_writer is not None:
                        try:
                            self.video_writer.write(image)
                        except cv2.error as e:
                            print(f"Error while writing frame: {e}")

                    if self.take_snapshot_requested:
                        self.save_photo(image)
                        self.take_snapshot_requested=False 

                    if self.tracking:  
                        image=self.track_face(image)

                    self.send_image(image)  
                   
                else:
                    self.stop_webcam()   
                    self.disconnect_signal.emit() 


                                 
  
      def start_webcam(self):
           self.cap=cv2.VideoCapture(self.video_url)
           if not self.cap.isOpened():
                 self.running=False
                 return
           time.sleep(0.1)
           self.running=True
           self.fps_prev_time=0.0
           self.fps_curr_time=0.0
           self.fps=0

           self.start()
              
      def stop_webcam(self):
           self.running=False
           time.sleep(0.1)
           if self.cap is not None:
                self.cap.release()
                self.cap=None





    


           