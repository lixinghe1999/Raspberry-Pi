#include <Wire.h> //I2C Arduino Library
#include "bmi270.h"

#define INC_ADDRESS 0x68 //I2C 7bit address
#define CMD 0x7E
#define PWR_CTRL 0x7D
#define PWR_CONF 0x7C
#define ACC 0x40
#define GYRO 0x42
#define CHIP 0x00
#define DATA 0x0C
#define DRDY 0x1D
#define STATUS 0x03

#define WIRE Wire1 // Be careful!


int16_t chip_id, x, y, z;
uint8_t sampleBuffer_8bit[192];
int sb_index = 0;

void setup(){
  //Initialize Serial and I2C communications
  Serial.begin(115200);
  while (!Serial) ;
  WIRE.begin();
  WIRE.setClock(400000);

  // Serial.println("get started!");
  // Serial.print("CHIP_ID (36): ");
  // Serial.println(readRegister8(CHIP));

  // if (bmi270_config_file[0]==0xc8){
  //   Serial.println("load config!");
  // }
  // else{Serial.println("load fail!");}

  // initialization
  writeRegister8(PWR_CONF, 0x00); 
  delay(50);
  writeRegister8(0x59, 0x00);

  // load config
  for (int i=0; i<256; i++)
  {
    writeRegister8(0x5B, 0x00);
    writeRegister8(0x5C, i);

    WIRE.beginTransmission(INC_ADDRESS);
    WIRE.write(0x5E);
    WIRE.write(&bmi270_config_file[i*32], 32);
    WIRE.endTransmission();    
    delay(1);
  }
  writeRegister8(0x59, 0x01);
  
  // check 
  // delay(50);
  // byte init_status = readRegister8(0x21);
  // if ((init_status & 0x01) != 0)
  // {
  //   Serial.println("config ok");
  // }
  // else{
  //   Serial.println("config fail");
  //   Serial.println(init_status);
  // }

  // configuration
  writeRegister8(PWR_CTRL, 0x04); //enable
  
  writeRegister8(ACC, 0xAC); //ACC_CONF

  //writeRegister8(GYRO, 0xE9); //GYRO_CONF

  writeRegister8(PWR_CONF, 0x02); //disable power saving
 
}     

void loop()
{ 
  if ((readRegister8(STATUS) & 0x80) != 0)
  //if (readRegister8(DRDY) == 0x00)
  {
    readAllAccel();
    // Serial.print(" \tx:");
    // Serial.print(x);
    // Serial.print(" \ty:");
    // Serial.print(y);
    // Serial.print(" \tz:");
    // Serial.println(z);

  
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
    
    
    if (sb_index >= 192){
        Serial.write(sampleBuffer_8bit, sb_index);
        sb_index=0;
        }   
  }
}

//Read all axis
void readAllAccel() {
  WIRE.beginTransmission(INC_ADDRESS);
  WIRE.write(DATA);
  WIRE.endTransmission();
  WIRE.requestFrom(INC_ADDRESS, 6);

  x =             (WIRE.read()   | WIRE.read() << 8); 
  y =             (WIRE.read()   | WIRE.read() << 8); 
  z =             (WIRE.read()   | WIRE.read() << 8); 
}

//Read data in 8 bits
uint8_t readRegister8(uint8_t reg) {
  WIRE.beginTransmission(INC_ADDRESS);
  WIRE.write(reg);
  WIRE.endTransmission(false);
  WIRE.requestFrom(INC_ADDRESS, 1);  
  return WIRE.read();
}

//Read data in 16 bits
uint16_t readRegister16(uint16_t reg) {
  WIRE.beginTransmission(INC_ADDRESS);
  WIRE.write(reg);
  WIRE.endTransmission(false);
  WIRE.requestFrom(INC_ADDRESS, 2);  
  return (WIRE.read()|WIRE.read()<<8);
}

void writeRegister8(uint16_t reg, uint8_t value) {
  WIRE.beginTransmission(INC_ADDRESS);
  WIRE.write(reg);
  WIRE.write(value);
  WIRE.endTransmission();
}

//Write data in 16 bits
void writeRegister16(uint16_t reg, uint16_t value) {
  WIRE.beginTransmission(INC_ADDRESS);
  WIRE.write(reg);
  WIRE.write((uint16_t)value & 0xff);
  WIRE.write((uint16_t)value >> 8);
  WIRE.endTransmission();
}
