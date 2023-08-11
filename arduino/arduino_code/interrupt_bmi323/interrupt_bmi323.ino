
#include <Wire.h>

#define INC_ADDRESS 0x69
#define ACC_CONF  0x20  //Page 91
#define GYR_CONF  0x21  //Page 93
#define CMD       0x7E  //Page 65
#define Interrupt 0x3B  //Page 111
#define InterruptConf 0x38 // Page 105

const int interruptPin  = 2;  
int16_t  x, y, z;
// int16_t data[8];
volatile bool data_ready;
uint8_t sampleBuffer_8bit[1536];
int sb_index = 0;

void accel_drdy()
{
  data_ready = true;
}

void setup(void) {  

  Serial.begin(115200); 
  Serial.println("get started!");

  //Accelerometer
  Wire.begin();  
  Wire.setClock(1000000);      // I2C Fast Mode (400kHz)  
  softReset();  

  writeRegister16(InterruptConf, 0x0005); //
  delay(50);    

  writeRegister16(Interrupt, 0x0400); //Setting interrupt
  delay(50);   

  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), accel_drdy, RISING);

  writeRegister16(ACC_CONF,0x700D);//Setting accelerometer   
}

void softReset(){  
  writeRegister16(CMD, 0xDEAF);
  delay(50);    
}
void loop() {
  if (data_ready){
    readAllAccel();             // read all accelerometer   

    sampleBuffer_8bit[sb_index] = (x & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (x >> 8) & 0xFF;
    sb_index ++;

    sampleBuffer_8bit[sb_index] = (y & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (y >> 8) & 0xFF;
    sb_index ++;

    sampleBuffer_8bit[sb_index] = (z & 0xFF);
    sb_index ++;
    sampleBuffer_8bit[sb_index] = (z >> 8) & 0xFF;
    sb_index ++;
    
    if (sb_index >= 1536){
        Serial.write(sampleBuffer_8bit, sb_index);
        sb_index=0;
        } 
    data_ready = false;  
  }
}

//Write data in 16 bits
void writeRegister16(uint16_t reg, uint16_t value) {
  Wire.beginTransmission(INC_ADDRESS);
  Wire.write(reg);
  //Low 
  Wire.write((uint16_t)value & 0xff);
  //High
  Wire.write((uint16_t)value >> 8);
  Wire.endTransmission();
}

//Read data in 16 bits
uint16_t readRegister16(uint8_t reg) {
  Wire.beginTransmission(INC_ADDRESS);
  Wire.write(reg);
  Wire.endTransmission(false);
  int n = Wire.requestFrom(INC_ADDRESS, 4);  
  int i = 0;
  Wire.read();
  Wire.read();
  return (Wire.read() | Wire.read() << 8);
}

//Read all axis
void readAllAccel() {
  Wire.beginTransmission(INC_ADDRESS);
  Wire.write(0x03);
  Wire.endTransmission();
  Wire.requestFrom(INC_ADDRESS, 8);
  Wire.read();
  Wire.read();
  x = (Wire.read() | Wire.read() << 8);
  y = (Wire.read() | Wire.read() << 8);
  z = (Wire.read() | Wire.read() << 8);
}