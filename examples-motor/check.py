import os

os.environ['BLINKA_MCP2221'] = '1'
os.environ['BLINKA_MCP2221_RESET_DELAY'] = '20'

import multiprocessing
import time

import hid

print(hid.enumerate()[-1]['product_string'])

def loadlib():
	import board
	print(board.board_id)
	print(board.I2C())

proc = multiprocessing.Process(target = loadlib)

print('trying to import board...')
proc.start()
time.sleep(33)
proc.terminate()

print('process terminated by timeout')
