function two_period(audioAll)
global FS PERIOD CHIRP_LEN CHIRP_FREQ_START CHIRP_FREQ_END dist_min dist_max VS T B dist_fft_size num_of_mps peak_thresh gt_mp_dists display_flag_gt;
rece_signal_1 = (audioAll(:,1));
rece_signal_1 = rece_signal_1(1:FS);

tran_signal = zeros(CHIRP_LEN, 1);
time = (0:CHIRP_LEN-1)./FS;
tran_signal(1:CHIRP_LEN) = chirp(time, CHIRP_FREQ_START, time(end), CHIRP_FREQ_END);

[c,lags] = xcorr(tran_signal,rece_signal_1);
%[max_c,I] = max(c);
delay =  -(lags(c == max(c)));

%delay = finddelay(tran_signal,rece_signal_1);
rece_signal_1 = rece_signal_1(delay+1:delay+CHIRP_LEN);


rece_signal_2 = (audioAll(:,1));
rece_signal_2 = rece_signal_2(FS+1:FS*2);
delay_2 = finddelay(tran_signal,rece_signal_2);
rece_signal_2 = rece_signal_2(delay_2+1:delay_2+CHIRP_LEN);

%mix signal

mix_signal_1 = rece_signal_1.*tran_signal;
mix_signal_2 = rece_signal_2.*tran_signal;
mix_signal = mix_signal_1-mix_signal_2;
low_freq = dist_min*2/VS/T*B;
high_freq = dist_max*2/VS/T*B;
lpFilt_chirp = fir1(300,[(low_freq)/(FS/2) (high_freq)/(FS/2)],'bandpass');
mix_signal = filtfilt(lpFilt_chirp,1,mix_signal);

%fft
dist_search = linspace(0,FS/2,dist_fft_size/2)*VS*T/(2*B);
dist_idx = (dist_search >= dist_min) & (dist_search <= dist_max);
dist_search = dist_search(dist_idx);

dist_fft = fft(mix_signal,dist_fft_size);  
dist_fft = abs(dist_fft(dist_idx)).^2/dist_fft_size; 
%dist_fft = dist_fft/max(dist_fft);

%find peaks
selected_chirp = dist_fft; 
[pks_amps, pks_locs] = findpeaks(selected_chirp);
[~, pks_idx] = sort(pks_amps,'descend');

max_peak_amp = pks_amps(pks_idx(1));
all_sig_path_paras = cell(1,num_of_mps);
for mp_idx = 1:num_of_mps
    if mp_idx <= length(pks_idx)
        if pks_amps(pks_idx(mp_idx)) >= peak_thresh*max_peak_amp
            est_dist =  dist_search(pks_locs(pks_idx(mp_idx)));
            pks_locs(pks_idx(mp_idx));
        end
    else 
        % avoid the case where # estimated paths are less than # true paths
        non_empty_idx = find(~cellfun(@isempty, all_sig_path_paras));
        last_idx = non_empty_idx(end);
        est_dist = all_sig_path_paras{last_idx}.raw_dist;
    end
end
    
dist_display_step = 0.2;
figure;
plot(dist_search,selected_chirp,'linewidth',3);
if display_flag_gt
    % ------ Ground Truth -----
    hold on;
    point = plot([gt_mp_dists(1) gt_mp_dists(1)],[min(selected_chirp) max(selected_chirp)],'--r','linewidth',3);
    for mp_idx=2:num_of_mps
        hold on;
        plot([gt_mp_dists(mp_idx) gt_mp_dists(mp_idx)],[min(selected_chirp) max(selected_chirp)],'--r','linewidth',3);
    end
    legend(point,'Groundtruth');
end
xlabel('Range (m)');
xlim([dist_min dist_max]);
xticks(dist_min:dist_display_step:dist_max);
set(gca,'xtick',[dist_min:dist_display_step:dist_max]);
ylabel('Amplitude');
title('Range FFT');
set(gca,'linewidth',1.5,'fontsize',20,'fontname','Arial');
end


