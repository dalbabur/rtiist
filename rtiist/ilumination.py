import string
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import threading

exR = (255,0,0)
exG = (0,255,0)
exB = (0,0,255)

ex584 = (255,239,0)
ex485 = (0,230,255)

plate96 = [(x,y) for y in range(1,12,3) for x in range(15,51,3)]
plate96_full = [(x,y) for y in range(0,36,1) for x in range(0,64,1)]


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
#rgb_to_hex((255, 255, 195))

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
#hex_to_rgb("FF65BA")

import logging
log = logging.getLogger(__name__)

from dataclasses import dataclass, field

@dataclass
class Measurement:
    """ 
    Container for all measurement-related information

    Args:
        label (str): measurement label for identification
        exRGB (tuple): excitation RGB for LEDs
        emFilter (str): filter name
        layout (list): list of LED to turn on
        exposure (float): camera exposure time, in seconds
        frequency (float): frequency of measurements, in minutes
        output (string): 'RAW' or 'PROCESS'
    """
    label: str 
    exRGB: list
    emFilter: str
    layout: list
    exposure: float
    frequency: float
    output: string

class LightSchedule:
    def __init__(self, func):
        self.f = func
        # checks on func

    def evaluate(self, time : float):
        return self.f(time)

    def preview(self, times : list):
        L = []
        for t in times:
            L.append(self.evaluate(t))
        return L

    def rgb_to_hex(self, RGBs):
        return list(map(rgb_to_hex, RGBs))

@dataclass
class Stimulation:
    """ 
    Container for all stimulation-related information

    Args:
        label (str): measurement label for identification
        frequency (float): frequency of schedule evaluation, in minutes
        schedules (list): list of LightShedules. Defaults to [].
        positions (list): list of (x,y) pairs. Defaults to [].
    """
    label: str 
    frequency : float
    schedules: list = field(default_factory=list)
    positions: list = field(default_factory=list)

    def add_schedule(self, schedule : LightSchedule):
        self.schedules.append(schedule)

    def add_positions(self, positions: list):
        self.positions.append(positions)

    def _check(self):
        if len(self.schedules) != len(self.positions):
            print('Error')

    def evaluate(self, time):
        self._check()
        log.info('Turning ON LEDs for stimualation '+ self.label)
        return list(map(lambda L: L.evaluate(time),self.schedules)), self.positions

class Iluminator:
    """
    Controls RGBMatrix

    """
    # default options
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat'
    options.gpio_slowdown = 4
    options.chain_length = 1
    options.drop_privileges = False

    def __init__(self, options = None):
        """
        _summary_

        Args:
            options (RGBMatrixOptions, optional): RGBMatrixOptions used to construct RGBMatrix. Defaults to None.
        """
        if options:
            self._matrix = RGBMatrix(options = options)
        else:
            self._matrix = RGBMatrix(options = self.options)
        self._state = 0
        self._memory = None
        self.done = 0
        
    def update_matrix(self, matrix: RGBMatrix):
        self._matrix = matrix

    def turn_off(self):
        self._state = 0
        self._matrix.Fill(0,0,0)

    def on_measure(self, measurement: Measurement):
        self.turn_off()
        log.info('Turning ON LEDs for measurement '+measurement.label)

        self._state = 1
        for p in measurement.layout:
            self._matrix.SetPixel(p[0],p[1],*measurement.exRGB)
        time.sleep(measurement.exposure)

        log.info('Turning OFF LEDs for measurement '+measurement.label)
        self.turn_off()

    def on_stimulate(self, RGBs:list, positions:list): # static. if dynamic call multiple times
        log.info('updating LEDs for stimulation')
        self.turn_off()
        self._state = 2

        for k,rgb in enumerate(RGBs):
            for p in positions[k]:
                self._matrix.SetPixel(p[0],p[1],*rgb)

    def stim_wrap(self,d):
        print('Wrap \n')
        self.on_stimulate('test',d)
        self.turn_off()
        print('Wrap Done \n')
       

