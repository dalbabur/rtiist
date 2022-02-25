from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import asyncio
from ilumination import Iluminator

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 4
options.chain_length = 1

matrix = RGBMatrix(options = options)

ex584 = (255,239,0)
ex485 = (0,230,255)
exB = (0,0,255)
exR = (50,0,0)
exG = (0,50,0)

async def main():
    a = Iluminator(matrix)
    for x in range(15,51,3):
        for y in range(1,12,3):
            a._matrix.SetPixel(x,y,*exR)
            time.sleep(0.001)

if __name__ == "__main__":
    asyncio.run(main())
    time.sleep(5)