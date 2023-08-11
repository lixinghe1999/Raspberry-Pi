#include <PDM.h>

// Buffer to read samples into, each sample is 16-bits
extern short sampleBuffer[512]; 
// Number of audio samples read
extern int samplesRead;

void mic_setup();
void onPDMdata();