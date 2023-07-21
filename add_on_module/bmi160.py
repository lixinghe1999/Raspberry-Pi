import time
from BMI160_i2c import Driver
def bmi160_accsave(loc, sample_rate=1600, t=5, port=0):
    sensor = Driver(0x69, port) #change address if needed
    if sample_rate == 1600:
        sensor.set_accel_rate(12)
    else:
        sensor.set_accel_rate(11)
    num = sample_rate * t
    a = 0
    acc = ''
    time_start = time.time()
    accwriter = open(loc + str(time_start) + '_'  + str(port) + '.txt', 'w')
    while (a < num):
        if sensor.getIntACCDataReadyStatus():
            try:
                data = sensor.getAcceleration()
            except: 
                data = ''
            a = a + 1
            acc = str(data[0]) + ' ' + str(data[1]) + ' ' + str(data[2]) + ' ' + str(time.time()) + '\n'
            accwriter.write(acc)        
    print('ACC port:', port, 'sample rate:', num / (time.time() - time_start))
def bmi160_gyrosave(name, num, port):
    sensor = Driver(0x69, port)# change address if needed
    sensor.set_gyro_rate(12)
    a = 0
    gryo = ''
    time_start = time.time()
    accwriter = open(name + '_' + str(time_start) + '.txt', 'w')
    while (a < num):
        if sensor.getIntGYRODataReadyStatus():
            a = a + 1
            data = sensor.getRotation()
            gryo = gryo + str(data[0]) + ' ' + str(data[1]) + ' ' + str(data[2]) + ' ' + str(time.time()) + '\n'
        else:
            accwriter.write(gryo)
            gryo = ''
    print('GYRO port:', port, num/(time.time() - time_start))

if __name__ == "__main__":
    bmi160_accsave('acc.txt', 8000, 1)
    bmi160_gyrosave('gyro.txt', 8000, 1)