#include "bmi270.h"
#include "mic.h"


uint8_t sampleBuffer_8bit[1536]; 
int sb_index = 0;

void setup(){
  mic_setup();
}

void loop() {
  // Wait for samples to be read
  if (samplesRead) {
    // Conversion 16bit sample to 8 bit sample, adding \n 
    for (int i = 0; i < samplesRead; i=i+1) {
      sampleBuffer_8bit[sb_index] = (sampleBuffer[i] >> 8) & 0xFF;
      sb_index ++;
      sampleBuffer_8bit[sb_index] = (sampleBuffer[i] & 0xFF);
      sb_index ++;
      //Sending data via SerialUSB
      if (sb_index >= 1536){
        SerialUSB.write(sampleBuffer_8bit,sb_index);
        sb_index=0;
        }
  }
    // Clear the read count
    samplesRead = 0;
  }
}