from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import sys

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 4

matrix = RGBMatrix(options = options)

ex584 = (255,239,0)
ex485 = (0,230,255)
exB = (200,0,0)

matrix.Fill(250,250,250)

# for x in range(0,64,1):
#     for y in range(0,32,1):
#         matrix.SetPixel(x,y,150,0,0)
#         time.sleep(0.01)
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)