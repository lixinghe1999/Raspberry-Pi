package com.gtappdevelopers.camviewlibrary;

import android.content.Context;
import android.media.AudioDeviceInfo;
import android.media.AudioManager;
import android.media.MicrophoneInfo;
import android.util.Log;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
public class SoundDeviceLister {
    public static List<String> listSoundDevices(Context context) throws IOException {
        List<String> deviceNames = new ArrayList<>();
        AudioManager audioManager = (AudioManager) context.getSystemService(Context.AUDIO_SERVICE);
        AudioDeviceInfo[] devices = audioManager.getDevices(AudioManager.GET_DEVICES_INPUTS);
        for (AudioDeviceInfo device : devices) {
            String devicename = device.getProductName().toString();
            int device_id = device.getId();
            deviceNames.add(devicename);
            Log.d("device name + id", devicename + "" + device_id);
        }
        List<MicrophoneInfo> microphones = audioManager.getMicrophones();
        for (MicrophoneInfo mic : microphones){
            Log.d("mic", mic.getAddress());
        }

        return deviceNames;
    }
}