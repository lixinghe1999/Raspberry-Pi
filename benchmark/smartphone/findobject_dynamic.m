%parameters and load
global FS PERIOD CHIRP_LEN CHIRP_FREQ_START CHIRP_FREQ_END dist_min dist_max VS T B dist_fft_size num_of_mps peak_thresh gt_mp_dists display_flag_gt;
FS = 48000;
VS = 340;
PERIOD = 1920;  
CHIRP_LEN = 1440; 
CHIRP_FREQ_START = 17000;  
CHIRP_FREQ_END = 21000; 
T = CHIRP_LEN/FS;
B = CHIRP_FREQ_END - CHIRP_FREQ_START;
dist_fft_size = 10*FS*T;
num_of_mps = 1;
peak_thresh = 0;
dist_min = 0.1;
dist_max = 0.5;
gt_mp_dists = 0.75;
display_flag_gt = 0;


precision = 'int16';
fname = '1706411830060';
fname = strcat('data/', fname, '.pcm');
fid = fopen(fname);               % Open raw pcm file
audio = int16(fread(fid, Inf, precision));  % Convert data to 16 bit
fclose(fid);
audioAll = double(audio) / 32767;
audioAll = audioAll(1:2:end);

%[audioAll,Fs] = audioread('data/mic/lixing-mic-CA1x.wav');

%two_period(audioAll);
average_period(audioAll);
%doppler(audioAll);