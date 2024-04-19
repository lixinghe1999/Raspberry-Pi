import sounddevice as sd
import scipy.io.wavfile as wavfile
def play_and_rec(file='fmcw.wav'):
    rate, wave = wavfile.read(file)
    myrecording = sd.playrec(wave, rate, )
    sd.wait()
    return myrecording