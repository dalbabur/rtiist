import time
import schedule
import logging
logging.basicConfig(format='%(asctime)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level = logging.INFO)
log = logging.getLogger(__name__)

from engine import Engine
from ilumination import Measurement, Stimulation, LightSchedule

e = Engine(MotorDict = {'FilterWheel':'default'})
m1 = Measurement('red',(255,0,0),'FB610',[(5,5),],10,7,'PROCESS')
m2 = Measurement('green',(255,0,0),'FB520',[(5,5),],10,7.5,'PROCESS')

blue_on = LightSchedule(lambda t: (0,0,255))
s = Stimulation('s',1,[blue_on], [[(5,5)]])
    
e.set_measurements([m1,m2])
e.set_stimulation(s)

e.start(duration = 30)