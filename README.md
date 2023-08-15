This is the all-in-one illustraion and troubleshooting for my PhD journey.


# Outline
### 1. [Raspberry Pi (Python) earphone](#Rpi)
### 2. [Arduino (C) earphone](#earphone)
### 3. [EXG earphone](#exg)
### 4. [Multi-modal learning](#multimodal)
### 5. [3D model](#3d)

## Raspberry Pi earphone
<span id="Rpi">

The below code has been tested on Rasbian11
1. check i2c status: 
```
# Google search "Raspberry Pi, pinout"
i2cdetect -y 0/1 (two bus on RPi)
```
2. set the i2c speed: 
```
# may need sudo apt update before
sudo nano /boot/config.txt
# add or revise the following lines
dtparam=i2c_arm=on
dtparam=i2c_arm_baudrate=1000000
dtparam=i2c0=on
dtparam=i2c0_baudrate=1000000
```

3. [BMI160](https://github.com/lefuturiste/BMI160-i2c), [BMI-270](https://github.com/CoRoLab-Berlin/bmi270_python)

4. [bluetoothe HSP profile on Linux](http://youness.net/raspberry-pi/how-to-connect-bluetooth-headset-or-speaker-to-raspberry-pi-3). I believe it only works for Headset, not True Wireless Stereo earphone. (don't try to record audio from AirPods or Galaxy Buds on Linux!)
 </span>


 ## Arduino earphone
<span id="earphone">

1. [Arduino BLE Sense Nano microphone recording](https://github.com/macca0612/Audio-based-classification-with-TinyML-on-embeddeddevice) Note that the data from serial should be converted to short (16-bit) + 8000 sample rate (HFS profile)

2. Arduino BLE Sense Nano Rev2: IMU is updated to BMI270 (finished, at arduino/arduino_code/bmi270.ino)

3. Serial data for two sensors: /arduino/receive.py (still working on it) next step: interrupt + FIFO to reach stable sample rate without loss

4. [Arduino work on BMI323 (New IMU 2023)](https://forum.arduino.cc/t/using-bmi323-with-i-c/1092880), [Mouser](https://www.mouser.hk/ProductDetail/Bosch-Sensortec/Shuttle-Board-3.0-BMI323?qs=By6Nw2ByBD2%252BWPBpp%2Fi%252BOg%3D%3D). 
You may need 1.27mm to 2.54mm adaptor to connect.

 </span>

 ## EXG
 <span id="exg">

1. [OpenBCI-earable](https://github.com/MKnierim/openbci-headphones)

2. EMOTIV, IDUN ....
 </span>

 ## Multi-modal
 <span id="multimodal">
I list all the multi-modal tasks worth exploring.

1. Camera+Point cloud, BEVFusion

2. Visual question answering (instruction comprehension), [MobiVQA](https://dl.acm.org/doi/abs/10.1145/3534619), [efficient VLM](https://arxiv.org/pdf/2305.15033.pdf), [COSM2IC](https://ieeexplore.ieee.org/document/9844171)

</span>

 
 ## 3D model
 <span id="3d">

1. insert-based IMU + commercial earphone

2. Full earphone

3. Bio-sensing earphone

4. out-eardrum earphone

 </span>

