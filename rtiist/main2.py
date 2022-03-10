import time
import logging
logging.basicConfig(format='%(asctime)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level = logging.INFO)
log = logging.getLogger(__name__)

from engine import Engine
from ilumination import Measurement

e = Engine(MotorDict = {'FilterWheel':'default'})
m1 = Measurement('lol',(255,0,0),'4',[(5,5),],10,10)

for i in range(5):
    e.measure(m1)
    time.sleep(20)
