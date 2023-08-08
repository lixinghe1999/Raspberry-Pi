#include <Wire.h> //I2C Arduino Library

#define address 0x69 //I2C 7bit address

int response;

void setup(){
  //Initialize Serial and I2C communications
  Serial.begin(9600);
  Wire.begin();
  delay(100);
//  Wire.setClock(400000UL);
 
// setting IMU270 in normal mode
  // Wire.beginTransmission(address);  
  // Wire.write(0x7D); //PWR_Control Register
  // Wire.write(0x0E); // enable acquistion of acc,gyro and temp
  // Wire.endTransmission();
  //   delay(100);

  // Wire.beginTransmission(address);
  // Wire.write(0x40);   // Acc config
  // Wire.write(0xA8);   // 
  // Wire.endTransmission();
  // delay(100);

  // Wire.beginTransmission(address);  
  // Wire.write(0x42);   // Gyro config
  // Wire.write(0xA9);
  // Wire.endTransmission();
  // delay(100);

  // Wire.beginTransmission(address); // 
  // Wire.write(0x7C);   // PWR config
  // Wire.write(0x02);
  // Wire.endTransmission();
  // delay(100);

//  Wire.beginTransmission(address); 
//  Wire.write(0x7E);   // soft reset in CMD
//  Wire.write(0xb6);
//  Wire.endTransmission();
}     

void loop()
{
  Wire.beginTransmission(address);
  Wire.write(0x10);    // reading LSB of Acc
  Wire.endTransmission();
  Wire.requestFrom(address, 2); 
  if(2<= Wire.available())
  {
      response = Wire.read()|Wire.read()<<8;
  }

  Serial.println(response);
}
