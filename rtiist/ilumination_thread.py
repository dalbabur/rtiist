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


class Iluminator:

    # default options
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat'
    options.gpio_slowdown = 4
    options.chain_length = 1
    options.drop_privileges = False

    def __init__(self, options = None):
        if options:
            self._matrix = RGBMatrix(options = options)
        else:
            self._matrix = RGBMatrix(options = self.options)
        self._state = 0
        self._memory = None
        self.done = 0
        
    def update_matrix(self, matrix: RGBMatrix):
        self._matrix = matrix

    def _manager(self, operation_mode, time):
        # schedule, duration, t0 = self._memory
        # dt =  time - t0

        if (self._state == 2):
            if operation_mode == 'PAUSE': # pause stimulaiton timer while taking measurement

                pass
            elif operation_mode == 'NO_PAUSE': # stimulation timer does not stop while taking measurement

                pass
            else:
                raise ValueError('operation_mode '+operation_mode+' not recognized. Only "PAUSE" or "NO_PAUSE"')
            
        else:
            pass

    def turn_off(self):
        self._state = 0
        self._matrix.Fill(0,0,0)

    def on_measure(self, RGB: tuple, duration: float, pattern = plate96, operation_mode = 'PAUSE'):
        self.turn_off()
        self._manager(operation_mode, time.time())

        self._state = 1
        for p in pattern:
            self._matrix.SetPixel(p[0],p[1],*RGB)
        time.sleep(duration)

        if self.done == 0:
            self.on_stimulate('test',0)
        else:
            self.turn_off()

    def on_stimulate(self, schedule, duration: float): # static. if dynamic call multiple times

        self._state = 2
        self._memory = (schedule, duration, time.time())

        # do schedule
        self._matrix.Fill(*exB)
        time.sleep(duration)

    def stim_wrap(self,d):
        print('Wrap \n')
        self.on_stimulate('test',d)
        self.turn_off()
        print('Wrap Done \n')
       

