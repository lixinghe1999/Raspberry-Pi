#include <LSM6DS3.h>
#include <Wire.h>

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A
int16_t x, y, z;
uint8_t sampleBuffer_8bit[192];
int sb_index = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);
  //Call .begin() to configure the IMUs
  if (myIMU.begin() != 0) {
    Serial.println("Device error");
  } else {
    Serial.println("aX,aY,aZ,gX,gY,gZ");
  }
}

void loop() {
  // wait for significant motion
    // read the acceleration data
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
    
    
    if (sb_index >= 192){
        Serial.write(sampleBuffer_8bit, sb_index);
        sb_index=0;
        }   
}