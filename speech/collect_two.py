import receive_arduino
import receive_knowles 
import argparse
import os
import datetime
import PySimpleGUI as sg
from verify import stats_metric
import random
import os
full_transcript = "aishell_transcript_v0.8.txt"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--sensor', '-s', action = "store", type=str, default='knowles', required=False)    
    parser.add_argument('--volunteer1', '-v1', action = "store", type=str, default='test1', required=False) 
    parser.add_argument('--volunteer2', '-v2', action = "store", type=str, default='test2', required=False)    
   
    args = parser.parse_args()
    transcripts = open(full_transcript, 'r', encoding='utf-8').readlines()
    len_transcripts = len(transcripts)
    date = datetime.datetime.now().date()
    parent_dicteroy1 = os.path.join(args.sensor, args.volunteer1, str(date))
    parent_dicteroy2 = os.path.join(args.sensor, args.volunteer2, str(date))

    if not os.path.exists(parent_dicteroy1):
        os.makedirs(parent_dicteroy1)
    if not os.path.exists(parent_dicteroy2):
        os.makedirs(parent_dicteroy2)
    if args.sensor == 'arduino':
        start = getattr(receive_arduino, 'start')
        record = getattr(receive_arduino, 'record')
    else:
        start = getattr(receive_knowles, 'start_two')
        record = getattr(receive_knowles, 'record_two')

    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('sensor1: ' + args.volunteer1 + ' sensor2: ' + args.volunteer2 + ' time: ' + str(date))],
        [sg.Text('在按下开始键后，请阅读以下文字，在阅读完成后点击完成键')],
                [sg.Text('Volunteer1 (sensor1)',), 
                 sg.Text('还未开始', key='content1', size=(25,4), font = ("Arial", 40))],
                [sg.Text('Volunteer2 (sensor2)',), 
                 sg.Text('还未开始', key='content2', size=(25,4), font = ("Arial", 40))],
                [sg.Text('采集时间:0', key='time')],
                [sg.Button('开始', size=(20, 3)), sg.Button('完成', size=(20, 3)),
                  sg.Button('重做', size=(20, 3)), sg.Button('结束', size=(20, 3))] ]
    # Create the Window
    window = sg.Window('Audio Recording Tool', layout)
    recording = False
    labels1 = []; labels2 = []
    time_sum = 0
    device_1, device2 = receive_knowles.select_device()
    while True:
        event, values = window.read()
        if event == '重做' and recording == False:
            # remove the previous recording
            os.remove(os.path.join(parent_dicteroy1, fname + '.wav'))
            os.remove(os.path.join(parent_dicteroy2, fname + '.wav'))

            start_time = datetime.datetime.now()
            fname = start_time.time().strftime("%H_%M_%S")
            thread1, thread2 = start(device_1, device2, os.path.join(parent_dicteroy1, fname + '.wav'), os.path.join(parent_dicteroy2, fname + '.wav'))
            window['content1'].update('阅读内容：' + ''.join(transcript1))
            window['content2'].update('阅读内容：' + ''.join(transcript2))

            recording = True
        if event == '开始' and recording == False:
            start_time = datetime.datetime.now()
            fname = start_time.time().strftime("%H_%M_%S")
            index = random.randint(0, len_transcripts-1)
            transcript1 = transcripts[index].split()[1:]
            index = random.randint(0, len_transcripts-1)
            transcript2 = transcripts[index].split()[1:]

            labels1.append(' '.join([fname] + transcript1))
            labels2.append(' '.join([fname] + transcript2))
        
            thread1, thread2 = start(device_1, device2, os.path.join(parent_dicteroy1, fname + '.wav'), os.path.join(parent_dicteroy2, fname + '.wav'))
            window['content1'].update('阅读内容：' + ''.join(transcript1))
            window['content2'].update('阅读内容：' + ''.join(transcript2))

            recording = True
        if event == '完成' and recording == True:
            duration = (datetime.datetime.now() - start_time).total_seconds()
            record(thread1, thread2)
            window['content1'].update('录制完成')
            window['content2'].update('录制完成')

            time_sum += duration
            window['time'].update('采集时间:' + str(time_sum))
            recording = False
        if event == sg.WIN_CLOSED or event == '结束': # if user closes window or clicks cancel
            break

    if os.path.exists(os.path.join(parent_dicteroy1, 'labels.txt')):
        if labels1 == []:
            pass
        else:
            open(os.path.join(parent_dicteroy1, 'labels.txt'), 'a', encoding='utf-8').write('\n' + '\n'.join(labels1))
    else:
        open(os.path.join(parent_dicteroy1, 'labels.txt'), 'w', encoding='utf-8').write('\n'.join(labels1))
    
    if os.path.exists(os.path.join(parent_dicteroy2, 'labels.txt')):
        if labels2 == []:
            pass
        else:
            open(os.path.join(parent_dicteroy2, 'labels.txt'), 'a', encoding='utf-8').write('\n' + '\n'.join(labels2))
    else:
        open(os.path.join(parent_dicteroy2, 'labels.txt'), 'w', encoding='utf-8').write('\n'.join(labels2))
    window.close()
