#include "audio_stream.h"
#include "imu_nrfsense.h"
<<<<<<< HEAD
uint8_t sampleBuffer_mic[256], sampleBuffer_8bit[256];
=======
uint8_t sampleBuffer_mic[512], sampleBuffer_8bit[256];
>>>>>>> 39e21974d7f72e437a2abc839d3bf8c84b048c94
int buffer_len=256;
int mic_index, sb_index;



void setup(){
  mic_setup();
  imu_setup();
}

void loop() {
  if (samplesRead) {
    // Serial.println(samplesRead); actually samplesRead is always 256
    for (int i = 0; i < samplesRead; i=i+1) {
      sampleBuffer_mic[mic_index] = (sampleBuffer[i] >> 8) & 0xFF;
      mic_index ++;
      sampleBuffer_mic[mic_index] = (sampleBuffer[i] & 0xFF);
      mic_index ++;
<<<<<<< HEAD
      if (mic_index >= buffer_len){
=======
      if (mic_index >= 512){
>>>>>>> 39e21974d7f72e437a2abc839d3bf8c84b048c94
        Serial.write((uint8_t)'\n');
        Serial.write((uint8_t)0x01);
        Serial.write(sampleBuffer_mic, mic_index);
        mic_index=0;
        }
    }
    samplesRead = 0;
  }
  receive_imu();

}
void receive_imu(){
    if (data_ready()){
          //imu_data(ax, ay, az, gx, gy, gz);
          imu_data();
          // Serial.println("1");
          // Serial.println(ax);
          // Serial.println(ay);
          // Serial.println(az);


          sampleBuffer_8bit[sb_index] = (ax & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (ax >> 8) & 0xFF;
          sb_index ++;
          
          sampleBuffer_8bit[sb_index] = (ay & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (ay >> 8) & 0xFF;
          sb_index ++;
          
          sampleBuffer_8bit[sb_index] = (az & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (az >> 8) & 0xFF;
          sb_index ++;
         

          sampleBuffer_8bit[sb_index] = (gx & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (gx >> 8) & 0xFF;
          sb_index ++;
          
          sampleBuffer_8bit[sb_index] = (gy & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (gy >> 8) & 0xFF;
          sb_index ++;
          
          sampleBuffer_8bit[sb_index] = (gz & 0xFF);
          sb_index ++;
          sampleBuffer_8bit[sb_index] = (gz >> 8) & 0xFF;
          sb_index ++;
          if (sb_index >= buffer_len){
            Serial.write((uint8_t)'\n');
            Serial.write((uint8_t)0x00);
            Serial.write(sampleBuffer_8bit, sb_index);
            sb_index=0;
        }   
    }
}