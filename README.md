This is the all-in-one illustraion and troubleshooting for my PhD journey.


## Outline
### 1. [Audio + IMU on Raspberry Pi](#Rpi)
### 2. [Arduino-based Earphone prototype](#earphone)
### 3. [Multi-modal learning](#multimodal)


## Audio + IMU on Raspberry Pi

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

 </span>


 ## Arduino
<span id="earphone">

1. [Arduino BLE Sense Nano microphone recording](https://github.com/macca0612/Audio-based-classification-with-TinyML-on-embeddeddevice) Note that the data from serial should be converted to short (16-bit)

2. Arduino BLE Sense Nano Rev2: IMU is updated to BMI270

3. Serial data for two sensors

 </span>

 ## Multi-modal
 <span id="multimodal">

 </span>

