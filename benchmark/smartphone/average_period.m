function average_period(audioAll)
global FS PERIOD CHIRP_LEN CHIRP_FREQ_START CHIRP_FREQ_END dist_min dist_max VS T B dist_fft_size num_of_mps peak_thresh gt_mp_dists display_flag_gt;
rece_signal = (audioAll(:,1));
rece_signal_1 = rece_signal(1:FS);

tran_signal = zeros(CHIRP_LEN, 1);
time = (0:CHIRP_LEN-1)./FS;
tran_signal(1:CHIRP_LEN) = chirp(time, CHIRP_FREQ_START, time(end), CHIRP_FREQ_END);

[c,lags] = xcorr(tran_signal,rece_signal_1);
delay =  -(lags(c == max(c)));
dist_total = 0;
count = 0;
chirp_dist = 1;
chirp_count = 0;
for frameNumber = 1 : 1
    %mix signal
    rece_signal_1 = rece_signal(delay+1:delay+CHIRP_LEN);
    rece_signal_2 = rece_signal(delay+1+PERIOD:delay+CHIRP_LEN+PERIOD);
    mix_signal_1 = rece_signal_1.*tran_signal;
    mix_signal_2 = rece_signal_2.*tran_signal;
    mix_signal = mix_signal_1-mix_signal_2;
    low_freq = dist_min*2/VS/T*B;
    high_freq = dist_max*2/VS/T*B;
    low_freq
    high_freq
    lpFilt_chirp = fir1(300,[(low_freq)/(FS/2) (high_freq)/(FS/2)],'bandpass');
    mix_signal = filtfilt(lpFilt_chirp,1,mix_signal);
    figure;
    subplot(3, 1, 1)
    plot(rece_signal_1)
    subplot(3, 1, 2)
    plot(tran_signal)
    subplot(3, 1, 3)
    plot(mix_signal_1)
    %fft
    dist_search = linspace(0,FS/2,dist_fft_size/2)*VS*T/(2*B);
    dist_idx = (dist_search >= dist_min) & (dist_search <= dist_max);
    dist_search = dist_search(dist_idx);

    dist_fft = fft(mix_signal,dist_fft_size);  
    dist_fft = abs(dist_fft(dist_idx)).^2/dist_fft_size; 

    %find peaks
    selected_chirp = dist_fft; 
    [pks_amps, pks_locs] = findpeaks(selected_chirp);
    [~, pks_idx] = sort(pks_amps,'descend');
    
    max_peak_amp = pks_amps(pks_idx(1));
    all_sig_path_paras = cell(1,num_of_mps);
    for mp_idx = 1:num_of_mps
        if mp_idx <= length(pks_idx)
            pks_value = pks_amps(pks_idx(mp_idx));
            if pks_value >= peak_thresh*max_peak_amp
                est_dist =  dist_search(pks_locs(pks_idx(mp_idx)));
                dist_total = dist_total + est_dist;
                count = count + 1;
              
                %if abs(est_dist - gt_mp_dists(1)) <= 0.2 * gt_mp_dists(1)
                 %   dist_total = dist_total + est_dist;
                  %  count = count + 1;
                %end
                pks_locs(pks_idx(mp_idx));
            end
        else 
            % avoid the case where # estimated paths are less than # true paths
            non_empty_idx = find(~cellfun(@isempty, all_sig_path_paras));
            last_idx = non_empty_idx(end);
            est_dist = all_sig_path_paras{last_idx}.raw_dist;
        end
    end
    delay = delay + PERIOD;
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
dist_average = dist_total/count
xlabel('Range (m)');
xlim([dist_min dist_max]);
xticks(dist_min:dist_display_step:dist_max);
set(gca,'xtick',[dist_min:dist_display_step:dist_max]);
ylabel('Amplitude');
title('Range FFT');
set(gca,'linewidth',1.5,'fontsize',20,'fontname','Arial');
end

