import threading
import time
import schedule
import logging
import os
print(os.getcwd())
from ilumination import Iluminator, Measurement

logging.basicConfig(format='%(asctime)s - %(threadName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level = logging.INFO)
log = logging.getLogger(__name__)

ilum = Iluminator()
m1 = Measurement('lol',(255,0,0),'4',[(5,5),],1,10)
m2 = Measurement('m2',(255,0,0),'4',[(5,5),],1,10)

def job1():
    ilum.on_measure(m1)

def job2():
    ilum.on_measure(m2)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(5).seconds.do(run_threaded, job1)
schedule.every(10).seconds.do(run_threaded, job2)


while 1:
    schedule.run_pending()
    time.sleep(1)