extern int16_t chip_id, x, y, z;

void imu_setup();
void readAllAccel();
uint8_t readRegister8(uint8_t reg);
uint16_t readRegister16(uint16_t reg);
void writeRegister8(uint16_t reg, uint8_t value);
void writeRegister16(uint16_t reg, uint16_t value);
