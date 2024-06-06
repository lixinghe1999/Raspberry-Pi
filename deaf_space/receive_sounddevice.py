import sounddevice as sd 
import soundfile as sf
import numpy as np

def record(output_file, device=1, channels=2, recording_duration=5):
    # Audio settings
    audio_rate = 44100
    audio_output = output_file + '.flac'

    audio_data = sd.rec(int(audio_rate * recording_duration), samplerate=audio_rate, channels=channels, device=device, blocking=True)

    sf.write(audio_output, audio_data, audio_rate)
    print('Audio recording saved to', audio_output)

if __name__ == '__main__':
    record('output')