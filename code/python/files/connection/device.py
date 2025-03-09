from PyQt5.QtCore import QObject,pyqtSignal as Signal,QThread
import struct
import files.connection.device as device
import serial.tools.list_ports
import serial
import os.path
import pickle
import time



class SerialConnection(QThread):
     disconected_signal=Signal()
     response_signal=Signal(str)
     def __init__(self):
          super().__init__()
          self.port=None
          self.baudrate=None
          self.serial_port=None
          self.running=False

     def start_device(self,port,baudrate,setting):
         try:
             self.baudrate=int(baudrate)
             self.port='COM'+port
             self.setting=setting
             self.serial_port=serial.Serial(self.port,9600)
             self.running=True
             self.start()
         except:
             self.running=False
             
                    
     def run(self):
          self.initial_device()
          while self.running:
               if self.serial_port and self.serial_port.isOpen():
                  try:  
                      data=self.serial_port.readline().decode('utf-8').strip()
                      self.response_signal.emit(data)
                  except serial.SerialException:
                       self.running=False
                       self.disconected_signal.emit()
               else:
                       self.running=False
                       self.disconected_signal.emit()
                     
     def stop_device(self):
           self.running=False
           if self.serial_port:
                self.serial_port.close()
     
     def send_byte_to_serial(self,byte):
           if self.serial_port and self.serial_port.isOpen():
             try:
                time.sleep(1/1000)
                self.serial_port.write(bytes([byte]))
             except serial.SerialException:
                self.disconected_signal.emit()


     def send_char_to_serial(self,char):
           if self.serial_port and self.serial_port.isOpen():
            try: 
              time.sleep(1/1000)
              encoded_char = struct.pack('c', char.encode())
              self.serial_port.write(encoded_char)
            except serial.SerialException:
                self.disconected_signal.emit()


     def send_short_int_to_serial(self,num):
           if self.serial_port and self.serial_port.isOpen():
              try:
                time.sleep(1/1000)
                encode=struct.pack('h',num)
                self.serial_port.write(encode)
              except serial.SerialException:
                self.disconected_signal.emit()

     def send_float_to_serial(self,num):
           if self.serial_port and self.serial_port.isOpen():
              try:
                 time.sleep(1/1000)
                 encode=struct.pack('f',num)
                 self.serial_port.write(encode)      
              except serial.SerialException:
                self.disconected_signal.emit()

     def send_Int8_to_serial(self,num):
           if self.serial_port and self.serial_port.isOpen():
              try:
                 time.sleep(1/1000)
                 encode=struct.pack('b',num)
                 self.serial_port.write(encode)
              except serial.SerialException:
                self.disconected_signal.emit()
   

     def send_unsigned_int_to_serial(self,num):
           if self.serial_port and self.serial_port.isOpen():
              try:
                time.sleep(1/1000)
                encode=struct.pack('H',num)
                self.serial_port.write(encode)
              except serial.SerialException:
                self.disconected_signal.emit()
     
     def initial_device(self):
         time.sleep(3)
         while self.serial_port.in_waiting>0:
             self.serial_port.readline().decode('utf-8').strip() 
         self.send_byte_to_serial(self.setting.enable)
         self.send_byte_to_serial(self.setting.step_mode)
         self.send_float_to_serial(self.setting.horizontal_max_speed)
         self.send_float_to_serial(self.setting.vertical_max_speed)
         self.send_byte_to_serial(self.setting.accel_enable)
         self.send_float_to_serial(self.setting.horizontal_accel)
         self.send_float_to_serial(self.setting.vertical_accel)
         self.send_float_to_serial(self.setting.horizontal_hall_offset_degrees)
         self.send_float_to_serial(self.setting.verticall_hall_offset_degrees)
         self.send_byte_to_serial(self.setting.automatic_track)
         self.send_float_to_serial(self.setting.move_invrement)
         
         

   

