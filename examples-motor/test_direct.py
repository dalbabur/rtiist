import time
import board

print(board.board_id)

from adafruit_pca9685 import PCA9685 as PCA
from adafruit_servokit import ServoKit
import digitalio as dio

pca = PCA(board.I2C())
pca.frequency = 50
print(pca.frequency)

servos = ServoKit(channels=16)
csn = 7
# servos.servo[sn].set_pulse_width_range(425, 2550)

button = dio.DigitalInOut(board.D19)
button.direction = dio.Direction.INPUT
button.pull = dio.Pull.UP

while True:
    if not button.value:
        servos.continuous_servo[csn].throttle = 1
    else:
        servos.continuous_servo[csn].throttle = 0


