import threading
from tkinter import N


from ilumination import Iluminator, Measurement, exG, plate96_full, ex584
from concurrent.futures import ThreadPoolExecutor

import time

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE
import schedule

import logging
from imaging import Measurement, Stimulation, Imager
from motors import FilterWheel
log = logging.getLogger(__name__)

class Engine:
    def __init__(self, ImgProcessor = None, RGBMatrixOptions = None, MotorDict = {}) -> None:
        self._setup_imager()
        self._setup_img_processor(ImgProcessor)
        self._setup_iluminator(RGBMatrixOptions)
        self._setup_motor(MotorDict)

        self.measurements = []
        self.stimulation = None
        self.controller = None

        self.scheduler = schedule.Scheduler()

        self.raw_data = []
        self.data = []

        self._t0 = time.time()
        self.t0 = None
        self.tf_hat = None
        self.tf = None
        self.times = []

    def _setup_imager(self):
        try:
            self._camSDK = TLCameraSDK() # make sure to dispose!
        except:
            pass

        def get_camera():
            camera_list = self._camSDK.discover_available_cameras()
            try:
                self._cam = self._camSDK.open_camera(camera_list[0])
                found = True
            except:
                found = False
            return found

        looking = True
        while looking:
            found = get_camera()
            if found:
                looking = False
                break

            elif not found:
                do = input("No camera found. Make sure camera is connected. Retry ['r'] or Continue without camera ['c'] ?\n")
                if do == 'r':
                    continue
                elif do == 'c':
                    log.info('Continuing without camera.')
                    looking = False
                    self._cam = None
                    self.imager = None
                    break
                else:
                    print('\n Invalid input. Retry.')
                    continue
        
        if self._cam:
            log.info('Setting up and arming camera.')
            
            self._cam.frames_per_trigger_zero_for_unlimited = 1
            self._cam.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
            self._cam.arm(1)
            self.imager = Imager(self._cam)

    def _setup_img_processor(self, ImgProcessor = None):
        if not ImgProcessor:
            self.img_processor = DefaultImgProcessor()
        else:
            self.img_processor = ImgProcessor
    
    def _setup_iluminator(self, RGBMatrixOptions):
        self.iluminator = Iluminator(RGBMatrixOptions)

    def _setup_motor(self, MotorDict):
        for k,v in MotorDict.items():
            if k == 'FilterWheel':
                if v == 'default':
                    self.filterWheel = FilterWheel()
                else:
                    self.filterWheel = FilterWheel(v.filter_list, v.servo_channel, v.alignment_channel, v.first_channel)
            else:
                print(k+' not recognized')
        pass

    def _setup_controller(self):
        pass

    def __del__(self):
        to_dispose = [self.camera, self._cam, self._camSDK]
        try:
            [x.dispose() for x in to_dispose]
        except:
            pass
        print('Everything disposed correctly')

    def _setup_thread(self, target, name, args):
        thread  = threading.Thread(target=target, name=name, args=args)
        thread.start()
        log.info('Thread ' + name + ' started.\n')

    def set_measurements(self, measurements:list):
        for m in measurements:
            self.measurements.append(m)
    
    def set_stimulation(self, stimulation: Stimulation):
        self.stimulation = stimulation

    def set_controller(self):
        pass

    def measure(self, measurement: Measurement, output = 'RAW'):
        log.info('Measurement ' + measurement.label + ' started.\n')
        
        self.iluminator.on_measure(measurement)

        if self.imager:
            self.imager._camera.exposure_time_us = measurement.exposure *1000 *1000
            self.imager._camera.issue_software_trigger()

            get_img = threading.Thread(target = lambda: self.raw_data.append(self.imager.run()))
            get_img.start()
        else:
            print('No camera, no measurement.')
        
        if output == 'RAW':
            pass
        elif output == 'PROCESS':
            get_img.join()
            label = 'processing_'+measurement.label
            self._setup_thread(self.process_data, label, self.raw_data[-1])

        pass
    
    def process_data(self, raw_data):
        self.data.append(self.img_processor.run(raw_data))
        
    def _setup_schedule(self):
        for m in self.measurements:
            label = m.label + '_' + str(time.time()-self._t0)
            self.scheduler.every(m.frequency).minutes.do(self._setup_thread,label,m)

        if self.stimulation:
            self.scheduler.every(self.stimulation.frequency).minuted.do(f,args)
        
        if self.controller:
            self.scheduler.every(self.controller.frequency).minutes.do(f,args)

    def start(self):
        self.t0 = time.time()
        pass

    def stop():
        pass