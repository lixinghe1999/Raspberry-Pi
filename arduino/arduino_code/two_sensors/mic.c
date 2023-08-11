#include "mic.h"
#include <PDM.h>

// // default number of output channels
// const char channels = 1;

// // default PCM output frequency
// const int frequency = 16000;

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512]; 


// Number of audio samples read
volatile int samplesRead;

void mic_setup() {
  SerialUSB.begin(115200);
  while(!SerialUSB);
  // Configure the data receive callback
  PDM.onReceive(onPDMdata);

  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and 24 on the Portenta Vision Shield
   PDM.setGain(5);

  if (!PDM.begin(channels, frequency)) {
    SerialUSB.println("Failed to start PDM!");
    while (1);
  }
}

/**
 * Callback function to process the data from the PDM microphone.
 * NOTE: This callback is executed as part of an ISR.
 * Therefore using `Serial` to print messages inside this function isn't supported.
 * */
 
void onPDMdata() {
  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;

}