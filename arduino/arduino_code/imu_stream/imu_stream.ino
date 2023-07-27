/*
  Arduino LSM9DS1 - Accelerometer Application

  This example reads the acceleration values as relative direction and degrees,
  from the LSM9DS1 sensor and prints them to the Serial Monitor or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense

  Created by Riccardo Rizzo

  Modified by Jose García
  27 Nov 2020

  This example code is in the public domain.
*/

#include <Arduino_LSM9DS1.h>

int16_t x, y, z;
uint8_t sampleBuffer_8bit[256]; 
int sb_index = 0;

void setup() {
  SerialUSB.begin(115200);
  while (!SerialUSB);
  SerialUSB.println("Started");

  if (!IMU.begin()) {
    SerialUSB.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readRawAcceleration(x, y, z);
    sampleBuffer_8bit[sb_index] = '\n';
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (x & 0xFF);
    sb_index ++;
    if (sb_index >= 256){
        SerialUSB.write(sampleBuffer_8bit,sb_index);
        sb_index=0;
        }
  }
}
