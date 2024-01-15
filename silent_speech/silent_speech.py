import receive_knowles
import datetime
from scipy.io.wavfile import write
import time

if __name__ == '__main__':
    start = getattr(receive_knowles, 'start')
    record = getattr(receive_knowles, 'record')
    start_time = datetime.datetime.now()
    fname = start_time.time().strftime("%H_%M_%S") + '.wav'
    start(5)
    time.sleep(5)
    record(fname, 5, plot=False)
