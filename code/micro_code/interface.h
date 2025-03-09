#ifndef INTERFACE
#define INTERFACE

#define PIN_STEPPER_EN 12
#define PIN_STEPPER_MS1 11
#define PIN_STEPPER_MS2 10
#define PIN_HORIZONTAL_STEPPER_STEP 5
#define PIN_HORIZONTAL_STEPPER_DIR 4
#define PIN_VERTICAL_STEPPER_STEP 8
#define PIN_VERTICAL_STEPPER_DIR 7
#define PIN_HORIZONTAL_HALL A1
#define PIN_VERTICAL_HALL A0


#define HORIZONTALL_GEAR_RATIO 8.4705882352941176470588235294118 //144/17 teeth
#define VERTICAL_GEAR_RATIO 3.047619047619047619047619047619 //64/21 teeth

#define HALF_STEP 2
#define QUARTER_STEP 4
#define EIGHTH_STEP 8
#define SIXTEENTH_STEP 16

#define TAKE_PHOTO_DELAY 50
#define KEYFRAME_ARRAY_LENGTH 30

#define BAUD_RATE 9600


struct KeyFrameElements {
    float horizontalDeg = 0;
    float horizontalSpeed = 0;
    float horizontalAccel = 0;
    float verticalDeg = 0;
    float verticalSpeed = 0;
    float verticalAccel = 0;
    bool accelEnable=false;
    unsigned int msDelay = 0;

};

/****************************************************************************************************************************************************************/
//serial communication function 
void serialFlush();
char readCharFromSerial();
byte readByteFromSerial();
bool readBoolFromSerial();
int8_t readInt8FromSerial();
int readIntFromSerial();
unsigned int readUnsignedIntFromSerial();
float readFloatFromSerial();
void sendSuccessMessage();
void sendErrorMessage();
/****************************************************************************************************************************************************************************************/
//Get saved parameter from python app
void getSavedSetting(void);
/****************************************************************************************************************************************************************************************/
//stepper motor setting function
//set functions
void setToggleSteppersEnable();
void setStepperStepMode(byte steppersNewStepMode);
void setAntiClockWiseToPositiveDirection();
void setHorizontalSpeed();
void setVerticalSpeed();
void setToggleAccel();
void setHorizontalAccel();
void setVerticalAccel();
/******************************************************************************************************************************************************************************************/
//requirement function for stepper motor function
float horizontalDegreeToStep(float degree);
float verticalDegreeToStep(float degree);
float horizontalStepsToDegrees(long steps);
float horizontalStepsToDegrees(float steps);
float verticalStepsToDegree(long steps);
float verticalStepsToDegree(float steps);

/********************************************************************************************************************************************************************************/
//position functions
void twoAxisMoveDegree(float hDegree,float vDegree);
void horizontalMoveDegree(float degree);
void verticalMoveDegree(float degree);
void autoHome();
void setHome();
/*******************************************************************************************************************************************************************************/
//keyframe functions
void deletKeyFrame(byte index);
void editKeyframe();
void addPosition();
void printKeyFrames();
void moveIndex(byte index);
void executeMove(byte type);
/********************************************************************************************************************************************************************************/
//photography function
void panoramiclapse(float degPerPic,unsigned int msDelay,byte startIndex,byte EndIndex);
void timelapse(unsigned int numberOfPictures,unsigned int msDelay,byte startIndex,byte EndIndex);
/********************************************************************************************************************************************************************************/
//set arduino pins
void setPins();
/*******************************************************************************************************************************************************************************/
void detectInstruction();
/*******************************************************************************************************************************************************************************/
//initial function that arduino start run
void initial_func(void);
void loop_func(void);
#endif