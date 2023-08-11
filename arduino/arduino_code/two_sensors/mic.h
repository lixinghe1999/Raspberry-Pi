// default number of output channels
const char channels = 1;

// default PCM output frequency
const int frequency = 16000;
// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512]; 
// Number of audio samples read
int samplesRead;

void mic_setup();
void onPDMdata();