'''
we need to compress the data from serial communication
'''
from pydub import AudioSegment
import os
target_folder = ['AM']
for folder in target_folder:
    for file in os.listdir(folder):
        if file[-4:] == '.wav':
            f = os.path.join(folder, file)
            f_new = os.path.join(folder+'_compressed', file[:-3] +'mp3')
            AudioSegment.from_file(f).export(f_new, format="mp3", bitrate="96k")
