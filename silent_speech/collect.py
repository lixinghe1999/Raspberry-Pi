import receive_arduino
import receive_knowles 
import argparse
import os
import datetime
import PySimpleGUI as sg
import random
import os
full_transcript = "aishell_transcript_v0.8.txt"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--sensor', '-s', action = "store", type=str, default='knowles', required=False)    
    parser.add_argument('--volunteer', '-v', action = "store", type=str, default='Lixing_He', required=False)    
    args = parser.parse_args()
    transcripts = open(full_transcript, 'r', encoding='utf-8').readlines()
    len_transcripts = len(transcripts)

    date = datetime.datetime.now().date()

    if args.sensor == 'arduino':
        start = getattr(receive_arduino, 'start')
        record = getattr(receive_arduino, 'record')
    else:
        start = getattr(receive_knowles, 'start')
        record = getattr(receive_knowles, 'record')
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text(args.sensor + ' ' + args.volunteer + ' ' + str(date))],
        [sg.Text('在按下开始键后，请阅读以下文字，在阅读完成后点击完成键')],
                [sg.Listbox(['parkinson', 'silent speech (whisper)'], size=(20, 3), key='type'), sg.Button('选择', size=10)],
                [sg.Text('还未开始', key='content', size=(25,4), font = ("Arial", 40))],
                [sg.Text('采集时间:0', key='time')],
                [sg.Button('开始', size=10), sg.Button('完成', size=10), sg.Button('重做', size=10)],
                [sg.Button('结束', size=10)] ]
    # Create the Window
    window = sg.Window('Audio Recording Tool', layout)

    recording = False
    labels = []
    time_sum = 0
    while True:
        event, values = window.read()
        if event == '选择':
            print(event, values)
            parent_dicteroy = os.path.join(args.sensor, args.volunteer + '+' + values['type'][0], str(date))
            if not os.path.exists(parent_dicteroy):
                os.makedirs(parent_dicteroy)
        if event == '重做' and recording == False:
            # remove the previous recording
            os.remove(os.path.join(parent_dicteroy, fname + '.wav'))

            start_time = datetime.datetime.now()
            fname = start_time.time().strftime("%H_%M_%S")
            start()
            window['content'].update('阅读内容：' + ''.join(transcript))
            recording = True
        if event == '开始' and recording == False:
            start_time = datetime.datetime.now()
            fname = start_time.time().strftime("%H_%M_%S")
            index = random.randint(0, len_transcripts-1)
            transcript = transcripts[index].split()[1:]
            labels.append(' '.join([fname] + transcript))
            start()
            window['content'].update('阅读内容：' + ''.join(transcript))
            recording = True
        if event == '完成' and recording == True:
            duration = (datetime.datetime.now() - start_time).total_seconds()
            record(os.path.join(parent_dicteroy, fname + '.wav'), int(duration)+1, plot=False)
            window['content'].update('录制完成')
            time_sum += duration
            window['time'].update('采集时间:' + str(time_sum))
            recording = False
        if event == sg.WIN_CLOSED or event == '结束': # if user closes window or clicks cancel
            break

    if os.path.exists(os.path.join(parent_dicteroy, 'labels.txt')):
        if labels == []:
            pass
        else:
            open(os.path.join(parent_dicteroy, 'labels.txt'), 'a', encoding='utf-8').write('\n' + '\n'.join(labels))
    else:
        open(os.path.join(parent_dicteroy, 'labels.txt'), 'w', encoding='utf-8').write('\n'.join(labels))
    window.close()
