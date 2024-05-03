#include "mic.h"

// // default number of output channels
const char channels = 1;

// // default PCM output frequency
const int frequency = 16000;

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512]; 

// Number of audio samples read
int samplesRead;

extern "C" {
    #include <hal/nrf_pdm.h>
}

/* Private functions ------------------------------------------------------- */

/**
 * @brief PDM clock frequency calculation based on 32MHz clock and
 * decimation filter ratio 80
 * @details For more info on clock generation:
 * https://infocenter.nordicsemi.com/index.jsp?topic=%2Fps_nrf5340%2Fpdm.html
 * @param sampleRate in Hz
 * @return uint32_t clk value
 */
static uint32_t pdm_clock_calculate(uint64_t sampleRate)
{
    const uint64_t PDM_RATIO = 80ULL;
    const uint64_t CLK_32MHZ = 32000000ULL;
    uint64_t clk_control = 4096ULL * (((sampleRate * PDM_RATIO) * 1048576ULL) / (CLK_32MHZ + ((sampleRate * PDM_RATIO) / 2ULL)));

    return (uint32_t)clk_control;
}

void mic_setup() {
  Serial.begin(115200);
  // while(!SerialUSB);
  // Configure the data receive callback
  PDM.onReceive(onPDMdata);
  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and 24 on the Portenta Vision Shield
   PDM.setGain(0);

  if (!PDM.begin(channels, frequency)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
  nrf_pdm_clock_set((nrf_pdm_freq_t)pdm_clock_calculate(8000));
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