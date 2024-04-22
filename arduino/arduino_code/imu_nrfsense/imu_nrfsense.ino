#include <LSM6DS3.h>
#include <Wire.h>

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A
int16_t x, y, z;
const int buffer_len = 384;
uint8_t sampleBuffer_8bit[buffer_len];
int sb_index = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);
  //Call .begin() to configure the IMUs
  myIMU.begin();
  // if (myIMU.begin() != 0) {
  //   Serial.println("Device error");
  // } else {
  //   Serial.println("good");
  // }
}

void loop() {
  // wait for significant motion
    // read the acceleration data
  if (myIMU.DRDY_G() & myIMU.DRDY_XL()){
    x = myIMU.readRawAccelX();
    y = myIMU.readRawAccelY();
    z = myIMU.readRawAccelZ();

    sampleBuffer_8bit[sb_index] = (x & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
    sb_index ++;
    
    sampleBuffer_8bit[sb_index] = (y & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (y >> 8) & 0xFF;
    sb_index ++;
    
    sampleBuffer_8bit[sb_index] = (z & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (z >> 8) & 0xFF;
    sb_index ++;

    x = myIMU.readRawGyroX();
    y = myIMU.readRawGyroY();
    z = myIMU.readRawGyroZ();

    sampleBuffer_8bit[sb_index] = (x & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
    sb_index ++;
    
    sampleBuffer_8bit[sb_index] = (y & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (y >> 8) & 0xFF;
    sb_index ++;
    
    sampleBuffer_8bit[sb_index] = (z & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (z >> 8) & 0xFF;
    sb_index ++;
    if (sb_index >= buffer_len){
        Serial.write(sampleBuffer_8bit, sb_index);
        sb_index=0;
        }   
  }
}