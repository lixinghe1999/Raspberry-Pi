import sounddevice as sd 
import soundfile as sf
import numpy as np

def record(output_file, device=1, channels=2, recording_duration=5):
    # Audio settings
    audio_rate = 44100
    audio_frames_per_buffer = 1024
    audio_output = output_file + '.flac'

    # Initialize audio recording
    audio_frames = []
    total_audio_frames = int(audio_rate * recording_duration) // audio_frames_per_buffer

    def audio_callback(indata, frames, time, status):
        audio_frames.append(indata.copy())

    # Start audio recording
    audio_stream = sd.InputStream(channels=channels,
                                samplerate=audio_rate,
                                callback=audio_callback, device=device)

    audio_stream.start()

    # Recording loop
    while len(audio_frames) < total_audio_frames:
        pass

    # Stop audio recording
    audio_stream.stop()

    # Save audio recording
    audio_frames = np.concatenate(audio_frames, axis=0)
    sf.write(audio_output, audio_frames, audio_rate)
    print('Audio recording saved to', audio_output)

if __name__ == '__main__':
    record('output')