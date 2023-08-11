#include "bmi270.h"
#include "mic.h"

uint8_t sampleBuffer_mic[512], sampleBuffer_imu[192]; 
int mic_index, imu_index;


void setup(){
  //mic_setup();
  imu_setup();
}


void loop() {
  // Wait for samples to be read
  // if (samplesRead) {
  //   // Conversion 16bit sample to 8 bit sample, adding \n 
  //   for (int i = 0; i < samplesRead; i=i+1) {
  //     sampleBuffer_mic[mic_index] = (sampleBuffer[i] >> 8) & 0xFF;
  //     mic_index ++;
  //     sampleBuffer_mic[mic_index] = (sampleBuffer[i] & 0xFF);
  //     mic_index ++;
  //     //Sending data via SerialUSB
  //     if (mic_index >= 512){
  //       Serial.write(sampleBuffer_mic, mic_index);
  //       mic_index=0;
  //       }
  // }
  //   // Clear the read count
  //   samplesRead = 0;
  // }
  read_imu();
}
void read_imu(){
if ((readRegister8(0x03) & 0x80) != 0)
  {
    readAllAccel();  
    sampleBuffer_imu[imu_index] = (x & 0xFF);
    imu_index ++;
    sampleBuffer_imu[imu_index] = (x >> 8) & 0xFF;
    imu_index ++;
    sampleBuffer_imu[imu_index] = (y & 0xFF);
    imu_index ++;
    sampleBuffer_imu[imu_index] = (y >> 8) & 0xFF;
    imu_index ++;
    sampleBuffer_imu[imu_index] = (z & 0xFF);
    imu_index ++;
    sampleBuffer_imu[imu_index] = (z >> 8) & 0xFF;
    imu_index ++;
    
    
    if (imu_index >= 192){
        Serial.write(sampleBuffer_imu, imu_index);
        imu_index=0;
        }   
  }
}
