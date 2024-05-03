#include <LSM6DS3.h>
#include <Wire.h>
int16_t ax, ay, az, gx, gy, gz;

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

void imu_setup() {
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

bool data_ready(){
  return myIMU.DRDY_G() & myIMU.DRDY_XL();
}

//void imu_data(int16_t ax, int16_t ay, int16_t az, int16_t gx, int16_t gy, int16_t gz){
void imu_data(){
      ax = myIMU.readRawAccelX();
      ay = myIMU.readRawAccelY();
      az = myIMU.readRawAccelZ();

      gx = myIMU.readRawGyroX();
      gy = myIMU.readRawGyroY();
      gz = myIMU.readRawGyroZ();
}
// void loop() {
//   // wait for significant motion
//     // read the acceleration data
//   if (myIMU.DRDY_G() & myIMU.DRDY_XL()){
//     x = myIMU.readRawAccelX();
//     y = myIMU.readRawAccelY();
//     z = myIMU.readRawAccelZ();

//     sampleBuffer_8bit[sb_index] = (x & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
//     sb_index ++;
    
//     sampleBuffer_8bit[sb_index] = (y & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (y >> 8) & 0xFF;
//     sb_index ++;
    
//     sampleBuffer_8bit[sb_index] = (z & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (z >> 8) & 0xFF;
//     sb_index ++;

//     x = myIMU.readRawGyroX();
//     y = myIMU.readRawGyroY();
//     z = myIMU.readRawGyroZ();

//     sampleBuffer_8bit[sb_index] = (x & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
//     sb_index ++;
    
//     sampleBuffer_8bit[sb_index] = (y & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (y >> 8) & 0xFF;
//     sb_index ++;
    
//     sampleBuffer_8bit[sb_index] = (z & 0xFF);
//     sb_index ++;
//     sampleBuffer_8bit[sb_index] = (z >> 8) & 0xFF;
//     sb_index ++;
//     
//   }
// }