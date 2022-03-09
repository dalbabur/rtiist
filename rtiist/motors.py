import board
print(board.board_id)

from adafruit_pca9685 import PCA9685 as PCA
from adafruit_servokit import ServoKit
import digitalio as dio

emR = 'FB610'
emG = 'FB520'

class FilterWheel:
    def __init__(self, filter_list = [emR, emG], servo_channel = 7, alignment_channel = board.D19, first_channel = board.D25):
        self.filter_list = filter_list
        self.filter_N = len(filter_list)
        self.current_pos = None

        pca = PCA(board.I2C())
        pca.frequency = 50
        servos = ServoKit(channels=16)
        self.motor = servos.continuous_servo[servo_channel]

        self.aligned_sensor = dio.DigitalInOut(alignment_channel)
        self.aligned_sensor.direction = dio.Direction.INPUT
        self.aligned_sensor.pull = dio.Pull.UP

        self.first_sensor = dio.DigitalInOut(first_channel)
        self.first_sensor.direction = dio.Direction.INPUT
        self.first_sensor.pull = dio.Pull.UP

        self._find_first()

    def _counter(self):
        self.current_pos = self.current_pos + 1
        if self.current_pos > self.filter_N:
            self.current_pos = 0

    def _next(self): # could go fwd and rev, probs not worth it
        while not self.aligned_sensor.value:
            self.motor.throttle = 1
        self.motor.throttle = 0
        self._counter()

    def _find_first(self): # time it just in case it goes on forever 
        while not self.first_sensor.value:
            self._next()
        self.current_pos = 0

    def set_filter(self, filter):
        # if filter not in self.filter_list: # or try excecpt
        #     print('Error')

        new_pos = self.filter_list.index(filter)

        while self.current_pos != new_pos:
            self._next()

        