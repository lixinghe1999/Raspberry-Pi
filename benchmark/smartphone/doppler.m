function doppler(audioAll)
global FS PERIOD CHIRP_LEN CHIRP_FREQ_START CHIRP_FREQ_END dist_min dist_max VS T B dist_fft_size num_of_mps peak_thresh gt_mp_dists display_flag_gt;
rece_signal = (audioAll(:,1));
rece_signal_1 = rece_signal(1:FS);

tran_signal = zeros(CHIRP_LEN, 1);
time = (0:CHIRP_LEN-1)./FS;
tran_signal(1:CHIRP_LEN) = chirp(time, CHIRP_FREQ_START, time(end), CHIRP_FREQ_END);

[c,lags] = xcorr(tran_signal,rece_signal_1);
delay =  -(lags(c == max(c)));

%fft
dist_search = linspace(0,FS/2,dist_fft_size/2)*VS*T/(2*B);
dist_idx = (dist_search >= dist_min) & (dist_search <= dist_max);
dist_search = dist_search(dist_idx);

maxframe = 10;
accumulate_range_fft = zeros(size(dist_search, 2), maxframe);
dist_total = 0;
pks_total = 0;
count = 0;
chirp_dist = 1;
chirp_count = 0;
for frameNumber = 1 : maxframe
    %mix signal
    rece_signal_1 = rece_signal(delay+1:delay+CHIRP_LEN);
    mix_signal = rece_signal_1.*tran_signal;
    low_freq = dist_min*2/VS/T*B;
    high_freq = dist_max*2/VS/T*B;
    lpFilt_chirp = fir1(300,[(low_freq)/(FS/2) (high_freq)/(FS/2)],'bandpass');
    mix_signal = filtfilt(lpFilt_chirp,1,mix_signal);
    dist_fft = fft(mix_signal,dist_fft_size);  
    amulate_range_fft(:, frameNumber) = dist_fft(dist_idx);
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
                pks_total = pks_total + pks_locs(pks_idx(mp_idx));
                count = count + 1;
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

dist_average = dist_total/count
pks_total = round(pks_total/count)
size(accumulate_range_fft)
selected_range_bin = accumulate_range_fft(pks_total, :);
selected_range_bin_mag = abs(selected_range_bin);
selected_range_bin_pha = angle(selected_range_bin);
doppler_fft = fft(selected_range_bin_pha, maxframe);
doppler_fft = abs(doppler_fft).^2/maxframe;
subplot(4, 1, 1);
plot(dist_search, abs(accumulate_range_fft));
subplot(4, 1, 2);
plot(selected_range_bin_mag);
subplot(4, 1, 3);
plot(selected_range_bin_pha);
subplot(4, 1, 4);
plot(doppler_fft);
end

