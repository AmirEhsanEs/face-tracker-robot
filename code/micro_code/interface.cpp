#include <stdint.h>
#include "Arduino.h"
#include "HardwareSerial.h"
#include "interface.h"
#include <AccelStepper.h>
#include <MultiStepper.h>
#include <EEPROM.h>
/***************************************************************************************************************************************************************/
//Global parameters
AccelStepper horizontal_stepper=AccelStepper(1,PIN_HORIZONTAL_STEPPER_STEP,PIN_HORIZONTAL_STEPPER_DIR);
AccelStepper vertical_stepper=AccelStepper(1,PIN_VERTICAL_STEPPER_STEP,PIN_VERTICAL_STEPPER_DIR);
MultiStepper multi_stepper;

bool steppers_enable; //steppers enable
byte steppers_step_mode; //steppers mode
float horizontal_speed; //stepper speed degrees/second
float vertical_speed; //stepper speed degrees/second
bool accel_enable;//accel enable 
float horizontal_accel; //stepper accel degrees/second^2
float vertical_accel;//stepper accel degrees/second^2
float horizontal_stepper_steps_per_degree; //stepper requirement step for move 1 degree
float vertical_stepper_steps_per_degree; //stepper requirement step for move 1 degree
float move_increment;
float currentHDeg;
float currentVDeg;
int decimal_point;
/*hall effect sensors defines*/
float horizontal_offset_degrees;
float vertical_offset_degrees;

long target_position[2];  //target_position[0]:for horizontal & target_position[1]:for vertical

/*KeyFrame*/
KeyFrameElements keyframe[KEYFRAME_ARRAY_LENGTH+1];
byte keyframe_elements=0;
int8_t keyframe_start_index=-1;
int8_t keyframe_execute_count=1;

/*photography defines*/
float degrees_per_picture;
unsigned int delay_ms_between_pictures;
unsigned int number_of_pictures;
/*face tracking*/
bool auto_track_enable;

long startTime;
/****************************************************************************************************************************************************************/
//serial communication function 

void serialFlush(){
    while(Serial.available())
      char c=Serial.read();
}
char readCharFromSerial(){
     while (Serial.available() < 1) {
        }
     return char(Serial.read());   
}
byte readByteFromSerial(){
      while (Serial.available() < 1) {
        }
      return Serial.read();
}
bool readBoolFromSerial(){
      while (Serial.available() < 1) {
        }
      return bool(Serial.read());
}
int8_t readInt8FromSerial(){
    while (Serial.available() < 1) {
        }
    return int8_t(Serial.read());
}
int readIntFromSerial(){
      byte byteArray[2];
      while (Serial.available() < 2) {
        }
      byteArray[0]=Serial.read();
      byteArray[1]=Serial.read();
      return *((int*)byteArray);
}
unsigned int readUnsignedIntFromSerial(){
       byte byteArray[2];
      while (Serial.available() < 2) {
        }
      byteArray[0]=Serial.read();
      byteArray[1]=Serial.read();
      return *((unsigned int*)byteArray);
}
float readFloatFromSerial(){
        byte byteArray[4];
        while (Serial.available() < 4) {
        }
        byteArray[0]=Serial.read();
        byteArray[1]=Serial.read();
        byteArray[2]=Serial.read();
        byteArray[3]=Serial.read();
        return *((float*)byteArray);

}
void sendSuccessMessage(){
     Serial.println(1);
}
void sendErrorMessage(){
     Serial.println(0);
}
/****************************************************************************************************************************************************************************************/
//Get saved parameter from python app
void getSavedSetting(void){
      steppers_enable=readBoolFromSerial();
      steppers_step_mode=readByteFromSerial();
      horizontal_speed=readFloatFromSerial();
      vertical_speed=readFloatFromSerial();
      accel_enable=readBoolFromSerial();
      horizontal_accel=readFloatFromSerial();
      vertical_accel=readFloatFromSerial();
      horizontal_offset_degrees=readFloatFromSerial();
      vertical_offset_degrees=readFloatFromSerial();
      auto_track_enable=readBoolFromSerial();
      move_increment=readFloatFromSerial();
      steppers_enable=!steppers_enable;
}
/****************************************************************************************************************************************************************************************/
//stepper motor setting function
//set functions
void setToggleSteppersEnable(){
     if(steppers_enable==true){
        digitalWrite(PIN_STEPPER_EN,HIGH);
        steppers_enable=false;
     }
     else{
        digitalWrite(PIN_STEPPER_EN,LOW);
        steppers_enable=true;
     } 
}
void setStepperStepMode(byte steppersNewStepMode){
  float stepRatio= (float)steppersNewStepMode/ (float)steppers_step_mode;
  if(steppersNewStepMode==HALF_STEP){
    digitalWrite(PIN_STEPPER_MS1,HIGH);
    digitalWrite(PIN_STEPPER_MS2,LOW);
    decimal_point=0;
  }
  else if (steppersNewStepMode==QUARTER_STEP) {
    digitalWrite(PIN_STEPPER_MS1,LOW);
    digitalWrite(PIN_STEPPER_MS2,HIGH);
    decimal_point=1;
  }
  else if(steppersNewStepMode==EIGHTH_STEP){
    digitalWrite(PIN_STEPPER_MS1,LOW);
    digitalWrite(PIN_STEPPER_MS2,LOW);
    decimal_point=2;
  }
  else if(steppersNewStepMode==SIXTEENTH_STEP){
    digitalWrite(PIN_STEPPER_MS1,HIGH);
    digitalWrite(PIN_STEPPER_MS2,HIGH);
    decimal_point=3;
  }
  horizontal_stepper.setCurrentPosition(round(horizontal_stepper.currentPosition()*stepRatio));
  vertical_stepper.setCurrentPosition(round(vertical_stepper.currentPosition()*stepRatio));
  target_position[0]=round(target_position[0]*stepRatio);
  target_position[1]=round(target_position[1]*stepRatio);
  horizontal_stepper_steps_per_degree=(200.0 * (float)steppersNewStepMode*HORIZONTALL_GEAR_RATIO)/360.0;
  vertical_stepper_steps_per_degree=(200.0* (float) steppersNewStepMode*VERTICAL_GEAR_RATIO)/360.0;
  setHorizontalSpeed();
  setVerticalSpeed();
  setHorizontalAccel();
  setVerticalAccel();
  steppers_step_mode=steppersNewStepMode;
}
void setAntiClockWiseToPositiveDirection(){
     horizontal_stepper.setPinsInverted(true,false,false);
     vertical_stepper.setPinsInverted(false,false,false);
}
void setHorizontalSpeed(){
    horizontal_stepper.setMaxSpeed(horizontalDegreeToStep(horizontal_speed));
}
void setVerticalSpeed(){
    vertical_stepper.setMaxSpeed(verticalDegreeToStep(vertical_speed));
}
void setToggleAccel(){
     if(accel_enable==true)
        accel_enable=false;
     else
        accel_enable=true;
}
void setHorizontalAccel(){
     horizontal_stepper.setAcceleration(horizontalDegreeToStep(horizontal_accel));
}
void setVerticalAccel(){
     vertical_stepper.setAcceleration(verticalDegreeToStep(vertical_accel));
}

/******************************************************************************************************************************************************************************************/
//requirement function for stepper motor function
float horizontalDegreeToStep(float degree){
     return horizontal_stepper_steps_per_degree*degree;
}
float verticalDegreeToStep(float degree){
     return vertical_stepper_steps_per_degree*degree;
}
float horizontalStepsToDegrees(long steps){
     return steps/horizontal_stepper_steps_per_degree;
}
float horizontalStepsToDegrees(float steps){
     return steps/horizontal_stepper_steps_per_degree;
}
float verticalStepsToDegree(long steps){
     return steps/vertical_stepper_steps_per_degree;
}
float verticalStepsToDegree(float steps){
     return steps/vertical_stepper_steps_per_degree;

}
/********************************************************************************************************************************************************************************/
//position functions
void twoAxisMoveDegree(float hDegree,float vDegree){
     long prevTime;
     long currentTime;
     float horizontalDeg;
     float verticalDeg;
     target_position[0]=horizontalDegreeToStep(hDegree);
     target_position[1]=verticalDegreeToStep(vDegree); 
     Serial.print(currentHDeg,decimal_point);
     Serial.print(" ");
     Serial.println(currentVDeg,decimal_point);
     if(accel_enable==0){
        multi_stepper.moveTo(target_position);  
        prevTime=millis();
        while(target_position[0]!= horizontal_stepper.currentPosition()|| target_position[1]!= vertical_stepper.currentPosition()){
            multi_stepper.run();
            currentTime=millis();
            if(currentTime-prevTime>50){
                horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                Serial.print(horizontalDeg,decimal_point);
                Serial.print(" ");
                Serial.println(verticalDeg,decimal_point);
                prevTime=currentTime;
            } 
        }
      }
      else{
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
          horizontal_stepper.moveTo(target_position[0]);
          vertical_stepper.moveTo(target_position[1]);
          prevTime=millis();
          while(target_position[0]!= horizontal_stepper.currentPosition() || target_position[1]!= vertical_stepper.currentPosition()){
              horizontal_stepper.run();
              vertical_stepper.run();
              currentTime=millis();
              if(currentTime-prevTime>50){
                horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                Serial.print(horizontalDeg,decimal_point);
                Serial.print(" ");
                Serial.println(verticalDeg,decimal_point);
                prevTime=currentTime;
              } 
          } 
      }
      currentHDeg=hDegree;
      currentVDeg=vDegree;  
      Serial.print(currentHDeg,decimal_point);
      Serial.print(" ");
      Serial.println(currentVDeg,decimal_point);
}
void horizontalMoveDegree(float degree){
     long prevTime;
     long currentTime;
     float horizontalDeg;
     target_position[0]=horizontalDegreeToStep(degree);
     target_position[1]=vertical_stepper.currentPosition();
     Serial.println(currentHDeg,decimal_point);
     if(accel_enable==0){
       multi_stepper.moveTo(target_position);  
       prevTime=millis();
       while(target_position[0]!= horizontal_stepper.currentPosition()){
          multi_stepper.run();
          currentTime=millis();
          if(currentTime-prevTime>50){
            horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
            Serial.println(horizontalDeg,decimal_point);
            prevTime=currentTime;
          } 
       }
     }
     else{
        horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
        horizontal_stepper.moveTo(target_position[0]);
        prevTime=millis();
        while(target_position[0]!= horizontal_stepper.currentPosition()){
            horizontal_stepper.run();
            currentTime=millis();
            if(currentTime-prevTime>50){
              horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
              Serial.println(horizontalDeg,decimal_point);
              prevTime=currentTime;
            } 
        }
     }
      currentHDeg=degree;
      Serial.println(currentHDeg,decimal_point);
}
void verticalMoveDegree(float degree){
     long prevTime;
     long currentTime;
     float verticalDeg;
     target_position[0]=horizontal_stepper.currentPosition();
     target_position[1]=verticalDegreeToStep(degree); 
     Serial.println(currentVDeg,decimal_point);
     if(accel_enable==0){
        multi_stepper.moveTo(target_position);   
        prevTime=millis();
        while(target_position[1]!= vertical_stepper.currentPosition()){
            multi_stepper.run();
            currentTime=millis();
            if(currentTime-prevTime>50){
               verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition()); 
               Serial.println(verticalDeg,decimal_point);
               prevTime=currentTime;
            } 
        }
      }
        else{
            vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
            vertical_stepper.moveTo(target_position[1]);
            prevTime=millis();
          while(target_position[1]!= vertical_stepper.currentPosition()){
            vertical_stepper.run();
            currentTime=millis();
            if(currentTime-prevTime>50){
               verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition()); 
               Serial.println(verticalDeg,decimal_point);
               prevTime=currentTime;
            } 
        }
      }  
        currentVDeg=degree;
        Serial.println(currentVDeg,decimal_point);
}

void autoHome(){
     long prevTime;
     long currentTime;
     float horizontalDeg;
     float verticalDeg;
     target_position[0]=horizontalDegreeToStep(360);
     target_position[1]=verticalDegreeToStep(-200); 
     if(accel_enable==0){
        multi_stepper.moveTo(target_position);  
        prevTime=millis();
        while(target_position[0]!= horizontal_stepper.currentPosition()|| target_position[1]!= vertical_stepper.currentPosition()){
            multi_stepper.run();
            currentTime=millis();
            if(currentTime-prevTime>50){
                horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                Serial.print(horizontalDeg,decimal_point);
                Serial.print(" ");
                Serial.println(verticalDeg,decimal_point);
                prevTime=currentTime;
            }
            if(digitalRead(PIN_HORIZONTAL_HALL)==0){
              horizontal_stepper.setCurrentPosition(0);
              target_position[0]=0;
              multi_stepper.moveTo(target_position); 
            }
            if(digitalRead(PIN_VERTICAL_HALL)==0){
              vertical_stepper.setCurrentPosition(0);
              target_position[1]=verticalDegreeToStep(75);
              multi_stepper.moveTo(target_position);     
            }
        }
      }
      else{
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
          horizontal_stepper.moveTo(target_position[0]);
          vertical_stepper.moveTo(target_position[1]);
          prevTime=millis();
          while(target_position[0]!= horizontal_stepper.currentPosition() || target_position[1]!= vertical_stepper.currentPosition()){
              horizontal_stepper.run();
              vertical_stepper.run();
              currentTime=millis();
              if(currentTime-prevTime>50){
                horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                Serial.print(horizontalDeg,decimal_point);
                Serial.print(" ");
                Serial.println(verticalDeg,decimal_point);
                prevTime=currentTime;
              }
              if(digitalRead(PIN_HORIZONTAL_HALL)==0){
                horizontal_stepper.setCurrentPosition(0);
                target_position[0]=0;
                horizontal_stepper.moveTo(target_position[0]); 
            }
              if(digitalRead(PIN_VERTICAL_HALL)==0){
                vertical_stepper.setCurrentPosition(0);
                target_position[1]=verticalDegreeToStep(75);
                vertical_stepper.moveTo(target_position);     
            } 
          }
      }
      vertical_stepper.setCurrentPosition(0);
      target_position[1]=0;
      horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
      verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
      Serial.print(horizontalDeg,decimal_point);
      Serial.print(" ");
      Serial.println(verticalDeg,decimal_point);
}

void setHome(){
    float horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition());
    float verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());
    float realHorizontalDeg=horizontalDeg+horizontal_offset_degrees;
    horizontal_offset_degrees=int(realHorizontalDeg)%360;
    float realVerticalDeg=verticalDeg+vertical_offset_degrees;
    vertical_offset_degrees=realVerticalDeg;
    horizontal_stepper.setCurrentPosition(0);
    vertical_stepper.setCurrentPosition(0);

}
/*******************************************************************************************************************************************************************************/
//keyframe functions
void deletKeyFrame(byte index){
     if(index>=0 && index<keyframe_elements){
        for(int i=index;i<keyframe_elements;i++){
                  keyframe[i]=keyframe[i+1];
                        }
        keyframe_elements--;    
        if(index<=keyframe_start_index)
            keyframe_start_index--;
            if(keyframe_start_index==-1 && keyframe_elements!=0)
               keyframe_start_index=0;    
      Serial.print("x");  
      Serial.print(" ");
      Serial.println(keyframe_start_index);

     }
}
void editKeyframe(){
     byte type=readByteFromSerial();
     byte  index=readByteFromSerial();

     Serial.println(index);
     Serial.println(type);

     if(index>=0 && index<keyframe_elements){
           if(type==0){
               keyframe[index].accelEnable=readBoolFromSerial();
           }
           else if(type==1){
               keyframe[index].msDelay=readIntFromSerial();
           }
           else if(type==2){
                 keyframe[index].horizontalDeg=readFloatFromSerial();
           }
           else if(type==3){
                 keyframe[index].verticalDeg=readFloatFromSerial();
            
           }
           else if(type==4){
                 keyframe[index].horizontalSpeed=readFloatFromSerial();
            
           }
           else if(type==5){
                  keyframe[index].verticalSpeed=readFloatFromSerial();
           }
           else if(type==6){
                  keyframe[index].horizontalAccel=readFloatFromSerial();
           }
           else if(type==7){
                  keyframe[index].verticalAccel=readFloatFromSerial();
           }
     }    
}
void addPosition(){
    if(keyframe_elements>=0 && keyframe_elements<KEYFRAME_ARRAY_LENGTH){
      keyframe[keyframe_elements].horizontalDeg=currentHDeg;
      keyframe[keyframe_elements].horizontalSpeed=horizontal_speed;
      keyframe[keyframe_elements].horizontalAccel=horizontal_accel;
      keyframe[keyframe_elements].verticalDeg=currentVDeg;
      keyframe[keyframe_elements].verticalSpeed=vertical_speed;
      keyframe[keyframe_elements].verticalAccel=vertical_accel;
      keyframe[keyframe_elements].accelEnable=accel_enable;
      keyframe[keyframe_elements].msDelay=0;
      keyframe_elements++;
      if(keyframe_start_index==-1)
         keyframe_start_index=0;
    }       
}

void moveIndex(byte index){
    if(index>=0 && index<keyframe_elements){
      horizontal_stepper.setMaxSpeed(horizontalDegreeToStep(keyframe[index].horizontalSpeed));
      vertical_stepper.setMaxSpeed(verticalDegreeToStep(keyframe[index].verticalSpeed));
      accel_enable=keyframe[index].accelEnable;
      horizontal_stepper.setAcceleration(horizontalDegreeToStep(keyframe[index].horizontalAccel));
      vertical_stepper.setAcceleration(verticalDegreeToStep(keyframe[index].verticalAccel));
      twoAxisMoveDegree(keyframe[index].horizontalDeg,keyframe[index].verticalDeg);
      delay(keyframe[index].msDelay);
    }
}
void executeMove(byte type){
     if(keyframe_elements>1){
        Serial.println("t");
        twoAxisMoveDegree(keyframe[keyframe_start_index].horizontalDeg, keyframe[keyframe_start_index].verticalDeg);
        Serial.println("e");
        if(keyframe_execute_count!=0){
            int step=keyframe_execute_count/abs(keyframe_execute_count);
             Serial.println("m");
             bool tempAccel=accel_enable;
            if(type==0)
                  for(int i=0;i!=keyframe_execute_count;i+=step){
                      byte new_start_index=(((keyframe_start_index+step)% keyframe_elements)+keyframe_elements)% keyframe_elements;
                      moveIndex(new_start_index);
                      Serial.println(new_start_index);
                      keyframe_start_index=new_start_index;
                  }
            else if(type==1)
                  for(int i=0;i!=keyframe_execute_count;i+=step){
                      byte new_start_index=(((keyframe_start_index+step)% keyframe_elements)+keyframe_elements)% keyframe_elements;
                      timelapse(number_of_pictures,delay_ms_between_pictures,keyframe_start_index,new_start_index);
                      Serial.println(new_start_index);
                      keyframe_start_index=new_start_index;
                  }
            else if(type==2)
                  for(int i=0;i!=keyframe_execute_count;i+=step){
                      byte new_start_index=(((keyframe_start_index+step)% keyframe_elements)+keyframe_elements)% keyframe_elements;
                      panoramiclapse(degrees_per_picture,delay_ms_between_pictures,keyframe_start_index,new_start_index);
                      Serial.println(new_start_index);
                      keyframe_start_index=new_start_index;
                  }
            else if(type==3){
                  Serial.println("w");
                  for(int i=0;i!=keyframe_execute_count;i+=step){
                      byte new_start_index=(((keyframe_start_index+step)% keyframe_elements)+keyframe_elements)% keyframe_elements;
                      moveIndex(new_start_index);
                      Serial.println(new_start_index);
                      keyframe_start_index=new_start_index;
                  }
                  Serial.println("W");
            }
           Serial.println("e");
           accel_enable=tempAccel;   
           setHorizontalSpeed();
           setHorizontalAccel();
           setVerticalSpeed();
           setVerticalAccel(); 
    }
  }
}
/********************************************************************************************************************************************************************************/
//photography function
void panoramiclapse(float degPerPic,unsigned int msDelay,byte startIndex,byte EndIndex){
  if (degPerPic !=0){
     if(msDelay>TAKE_PHOTO_DELAY) 
        msDelay=msDelay-TAKE_PHOTO_DELAY;
     unsigned int halfmsDelay=msDelay/2;
     float horizontalAngle=keyframe[EndIndex].horizontalDeg-keyframe[startIndex].horizontalDeg;
     float verticalAngle=keyframe[EndIndex].verticalDeg-keyframe[startIndex].verticalDeg;
     float maxAngle=(abs(horizontalAngle)>abs(verticalAngle))?horizontalAngle:verticalAngle;
     unsigned int increment=abs(maxAngle)/degPerPic;
     if(increment!=0){
          float horizontalIncrement= horizontalAngle/increment;
          float verticalIncrement=verticalAngle/increment;
          twoAxisMoveDegree(keyframe[startIndex].horizontalDeg,keyframe[startIndex].verticalDeg);
          for(int i=0;i<=increment;i++){
              twoAxisMoveDegree((keyframe[startIndex].horizontalDeg)+(i*horizontalIncrement),(keyframe[startIndex].verticalDeg)+(i*verticalIncrement));
              delay(halfmsDelay);
              Serial.println("f");
              delay(halfmsDelay);
              }  
        }  
  }
}
void timelapse(unsigned int numberOfPictures,unsigned int msDelay,byte startIndex,byte EndIndex){
     if(msDelay>TAKE_PHOTO_DELAY)
        msDelay=msDelay-TAKE_PHOTO_DELAY;
     if(numberOfPictures>1)
        numberOfPictures=numberOfPictures-1;
           
     unsigned int halfmsDelay=msDelay/2;
     float horizontalAngle=(keyframe[EndIndex].horizontalDeg)-(keyframe[startIndex].horizontalDeg);
     float verticalAngle=(keyframe[EndIndex].verticalDeg)-(keyframe[startIndex].verticalDeg);
     float horizontalIncrement=horizontalAngle/numberOfPictures;
     float verticalIncrement=verticalAngle/numberOfPictures;
     twoAxisMoveDegree(keyframe[startIndex].horizontalDeg,keyframe[startIndex].verticalDeg);
     for(int i=0;i<=numberOfPictures;i++){
       twoAxisMoveDegree((keyframe[startIndex].horizontalDeg)+(i*horizontalIncrement),(keyframe[startIndex].verticalDeg)+(i*verticalIncrement));
       delay(halfmsDelay);
       Serial.println("f");
       delay(halfmsDelay);
     }
}
/*********************************************************************************************************************************************************************************/
void setToggleAutoTrack(){
     if(auto_track_enable==true)
        auto_track_enable=false;
     else
        auto_track_enable=true;
}
//face tracking
void track_face(){
    char instruction;
    float horizontalDeg;
    float verticalDeg;
    long prevTime;
    long currentTime;
    
    if(auto_track_enable){
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
          prevTime=millis();
          horizontal_stepper.setSpeed(horizontalDegreeToStep(90));
          vertical_stepper.setSpeed(verticalDegreeToStep(90));
          horizontal_stepper.setMaxSpeed(horizontalDegreeToStep(90));
          vertical_stepper.setMaxSpeed(verticalDegreeToStep(90));

          horizontal_stepper.setAcceleration(horizontalDegreeToStep(50));
          vertical_stepper.setAcceleration(verticalDegreeToStep(50));
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
          while(1){    
                if(Serial.available()){
                  instruction=Serial.read();
                  if(instruction=='h'){
                    target_position[0]=horizontal_stepper.currentPosition()+horizontalDegreeToStep(readFloatFromSerial());
                    horizontal_stepper.moveTo(target_position[0]); 
                  }
                  else if(instruction=='v'){
                    target_position[1]=vertical_stepper.currentPosition()+verticalDegreeToStep(readFloatFromSerial());
                    vertical_stepper.moveTo(target_position[1]); 
                  }
                  else if(instruction=='q')
                        break;
                }  
                horizontal_stepper.run();
                vertical_stepper.run();
               currentTime=millis();
               if(currentTime-prevTime>50){
                 horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                 verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                 Serial.print(horizontalDeg,decimal_point);
                 Serial.print(" ");
                 Serial.println(verticalDeg,decimal_point);
                 prevTime=currentTime;
               }
            }
          horizontal_stepper.setSpeed(0);
          vertical_stepper.setSpeed(0);
          setHorizontalSpeed();
          setHorizontalAccel();
          setVerticalSpeed();
          setVerticalAccel(); 
      }
    else{
          if(accel_enable){
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());            
              prevTime=millis();
              while(1){    
                    if(Serial.available()){
                      instruction=Serial.read();
                      if(instruction=='h'){
                        target_position[0]=horizontal_stepper.currentPosition()+horizontalDegreeToStep(readFloatFromSerial());
                        horizontal_stepper.moveTo(target_position[0]); 
                      }
                      else if(instruction=='v'){
                        target_position[1]=vertical_stepper.currentPosition()+verticalDegreeToStep(readFloatFromSerial());
                        vertical_stepper.moveTo(target_position[1]); 
                      }
                      else if(instruction=='q')
                            break;
                    }
                horizontal_stepper.run();
                vertical_stepper.run();
                currentTime=millis();
                if(currentTime-prevTime>50){
                    horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                    verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                    Serial.print(horizontalDeg,decimal_point);
                    Serial.print(" ");
                    Serial.println(verticalDeg,decimal_point);
                    prevTime=currentTime;
                }
              }
        }
      else{
          prevTime=millis();
          horizontal_stepper.setCurrentPosition(horizontal_stepper.currentPosition());
          vertical_stepper.setCurrentPosition(vertical_stepper.currentPosition());
          while(1){    
                if(Serial.available()){
                  instruction=Serial.read();
                  if(instruction=='h'){
                    target_position[0]=horizontal_stepper.currentPosition()+horizontalDegreeToStep(readFloatFromSerial());
                    horizontal_stepper.moveTo(target_position[0]); 
                  }
                  else if(instruction=='v'){
                    target_position[1]=vertical_stepper.currentPosition()+verticalDegreeToStep(readFloatFromSerial());
                    vertical_stepper.moveTo(target_position[1]); 
                  }
                  else if(instruction=='q')
                        break;
                }  
                horizontal_stepper.setSpeed(horizontalDegreeToStep(horizontal_speed));
                horizontal_stepper.runSpeedToPosition();    
                vertical_stepper.setSpeed(verticalDegreeToStep(vertical_speed));
               vertical_stepper.runSpeedToPosition();

               currentTime=millis();
               if(currentTime-prevTime>50){
                 horizontalDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
                 verticalDeg=verticalStepsToDegree(vertical_stepper.currentPosition());   
                 Serial.print(horizontalDeg,decimal_point);
                 Serial.print(" ");
                 Serial.println(verticalDeg,decimal_point);
                 prevTime=currentTime;
               }
            }
              horizontal_stepper.setSpeed(0);
              horizontal_stepper.runSpeedToPosition();    
              vertical_stepper.setSpeed(0);
              vertical_stepper.runSpeedToPosition();
          }
       }
    
      float prevCurrentHdeg=currentHDeg;
      float prevCurrentVdeg=currentVDeg;
      currentHDeg=horizontalStepsToDegrees(horizontal_stepper.currentPosition()); 
      currentVDeg=verticalStepsToDegree(vertical_stepper.currentPosition());
      twoAxisMoveDegree(prevCurrentHdeg,prevCurrentVdeg);
}
/********************************************************************************************************************************************************************************/
//set arduino pins
void setPins(){
     Serial.begin(BAUD_RATE);
     pinMode(PIN_STEPPER_EN, OUTPUT);
     pinMode(PIN_STEPPER_MS1, OUTPUT);
     pinMode(PIN_STEPPER_MS2, OUTPUT);
     pinMode(PIN_VERTICAL_STEPPER_STEP, OUTPUT);
     pinMode(PIN_VERTICAL_STEPPER_DIR, OUTPUT);
     pinMode(PIN_HORIZONTAL_STEPPER_STEP, OUTPUT);
     pinMode(PIN_HORIZONTAL_STEPPER_DIR, OUTPUT);
     pinMode(PIN_HORIZONTAL_HALL, INPUT_PULLUP);
     pinMode(PIN_VERTICAL_HALL, INPUT_PULLUP);
}
/*******************************************************************************************************************************************************************************/
void detectInstruction(){
    char instruction;
    instruction=Serial.read();
    switch (instruction) {
        case 'e':{
               setToggleSteppersEnable();
              }
        break;
        case 'm':{     
                 setStepperStepMode(readByteFromSerial());
              }
        break;
        case 's':{
              horizontal_speed=readFloatFromSerial();
              setHorizontalSpeed();
              }
        break;
        case 'S':{
              vertical_speed=readFloatFromSerial();
              setVerticalSpeed();
              }
        break;
        case 'c':{
              setToggleAccel();
              }
        break;
        case 'a':{
              horizontal_accel=readFloatFromSerial();
              setHorizontalAccel();
              }
        break;
        case 'A':{
              vertical_accel=readFloatFromSerial();
              setVerticalAccel();
              }
        break;
        case 'h':{
                Serial.println("h");
                horizontalMoveDegree(readFloatFromSerial());
                Serial.println("e");
              }
        break;
        case 'v':{
                Serial.println("v");
                verticalMoveDegree(readFloatFromSerial());
                Serial.println("e");
              }
        break;    
        case 'r':{
                Serial.println("t");
                float hDeg=readFloatFromSerial();
                float vDeg=readFloatFromSerial();
                twoAxisMoveDegree(hDeg,vDeg);
                Serial.println("e");
             }
        break;
        
        case 'i':{
                keyframe_start_index=readInt8FromSerial();
        }
        break;
        case 'I':{
                keyframe_execute_count=readInt8FromSerial();
        }
        break;
        case 'n':{
                number_of_pictures=readUnsignedIntFromSerial();
        } 
        break;
        case 'b':{
            degrees_per_picture=readFloatFromSerial();
        } 
        break;
        case 'B':{
            delay_ms_between_pictures=readUnsignedIntFromSerial();
        } 
        break;
        case 'p':{
                  addPosition();
                  Serial.print("p");
                  Serial.print(" ");
                  Serial.print(keyframe[keyframe_elements-1].horizontalDeg,decimal_point);
                  Serial.print(" ");
                  Serial.print(keyframe[keyframe_elements-1].verticalDeg,decimal_point);
                  Serial.print(" ");
                  Serial.println(keyframe_elements);

             }
        break;       
        case 'L':{
                  editKeyframe(); 
                 }
        break;         
        case 'd':{
                 deletKeyFrame(readByteFromSerial());
                 }        
        break;       
        case 'M':{
                executeMove(readByteFromSerial());
          }       
        break;
        case 'U':{
              Serial.println("t");
              autoHome();
              currentHDeg=0;
              currentVDeg=0;         
              horizontal_offset_degrees=0;
              vertical_offset_degrees=0;
              Serial.println("e");
        }
        break;
        case 'f':{
             setHome();
             Serial.print("o");
             Serial.print(" ");
             Serial.print(horizontal_offset_degrees);
             Serial.print(" ");
             Serial.println(vertical_offset_degrees);
             Serial.println("t");
             twoAxisMoveDegree(0,0);
             Serial.println("e");

        }
        break;
        case 'F':{
             Serial.println("t");    
             twoAxisMoveDegree(0,0);
             Serial.println("e");
        }
        break;
        case 'z':{
              Serial.println("t");
              track_face();
              Serial.println("e");
        }
        break;
        case 'l':{
           setToggleAutoTrack();
        }
        break;
        case 'x':{
           move_increment=readFloatFromSerial();
         }
        break;

        case 'k':{
                Serial.println("h");
                float hDeg=move_increment+currentHDeg;     
                horizontalMoveDegree(hDeg);
                Serial.println("e");
             }
        break;
        case 'K':{
                Serial.println("h");   
                float hDeg=-move_increment+currentHDeg;     
                horizontalMoveDegree(hDeg);
                Serial.println("e");
             }
        break;
        case 'j':{
                Serial.println("v");
                float vDeg=move_increment+currentVDeg;
                verticalMoveDegree(vDeg);
                Serial.println("e");
             }
        break;
        case 'J':{
                Serial.println("v");
                float vDeg=-move_increment+currentVDeg;
                verticalMoveDegree(vDeg);
                Serial.println("e");
             }
        break;

        case 'g':{
                Serial.println("t");
                float hDeg=move_increment+currentHDeg;
                float vDeg=move_increment+currentVDeg;
                twoAxisMoveDegree(hDeg,vDeg);
                Serial.println("e");
             }
        break;
        case 'G':{
                Serial.println("t");
                float hDeg=move_increment+currentHDeg;
                float vDeg=-move_increment+currentVDeg;
                twoAxisMoveDegree(hDeg,vDeg);
                Serial.println("e");
             }
        break;
        case 'w':{
                Serial.println("t");
                float hDeg=-move_increment+currentHDeg;
                float vDeg=move_increment+currentVDeg;
                twoAxisMoveDegree(hDeg,vDeg);
                Serial.println("e");
             }
        break;

        case 'W':{
                Serial.println("t");
                float hDeg=-move_increment+currentHDeg;
                float vDeg=-move_increment+currentVDeg;
                twoAxisMoveDegree(hDeg,vDeg);
                Serial.println("e");
             }
        break;
        case 'Z':{
              currentHDeg=readFloatFromSerial();
              currentVDeg=readFloatFromSerial();
        }

    }
}
/*******************************************************************************************************************************************************************************/
//initial function that arduino start run
void initial_func(void){
     setPins(); 
     Serial.println(startTime);
     getSavedSetting();
     setToggleSteppersEnable();
     setStepperStepMode(steppers_step_mode);
     setAntiClockWiseToPositiveDirection();
     multi_stepper.addStepper(horizontal_stepper);
     multi_stepper.addStepper(vertical_stepper);
     Serial.println("t");
     autoHome();
     currentHDeg=0;
     currentVDeg=0;
     twoAxisMoveDegree(horizontal_offset_degrees,vertical_offset_degrees);
     horizontal_stepper.setCurrentPosition(0); 
     vertical_stepper.setCurrentPosition(0);
     currentHDeg=0;
     currentVDeg=0;   
     Serial.print(currentHDeg,decimal_point);
     Serial.print(" ");
     Serial.println(currentVDeg,decimal_point);
     Serial.println("e");

}

void loop_func(void){
    while(1){         
      if(Serial.available())
         detectInstruction();   
    }
}