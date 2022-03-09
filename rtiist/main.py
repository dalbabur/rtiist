import matplotlib.pyplot as plt

from imaging import Imager
from rtiist.ilumination import Iluminator, exG, plate96_full, ex584
import threading
from concurrent.futures import ThreadPoolExecutor

import time

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE


import logging

logging.basicConfig(format='%(asctime)s - %(thread)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level = logging.INFO)
log = logging.getLogger(__name__)

def main():
    with TLCameraSDK() as sdk:
        camera_list = sdk.discover_available_cameras()
        with sdk.open_camera(camera_list[0]) as camera:
            print("Setting camera parameters...")
            image_acquisition = Imager(camera)
            camera.frames_per_trigger_zero_for_unlimited = 1
            camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
            camera.arm(1)

            a = Iluminator()
            stimulation = threading.Thread(target=a.stim_wrap, args=(22,))
            stimulation.start()
            t0 = time.time()
            imgs = []

            while stimulation.is_alive():


                camera.exposure_time_us = 3*1000*1000
                camera.issue_software_trigger()

                a.on_measure(ex584,30, plate96_full)
                
                get_img = threading.Thread(target = lambda: imgs.append(image_acquisition.run()))
                get_img.start()

                time.sleep(6)

            print(time.time()-t0)
            image_acquisition.stop()

    save_img = lambda enum: plt.imsave('/home/pi/LAB/rt-opto/rtiist/images/img-'+str(enum[0])+'.svg', enum[1])
    with ThreadPoolExecutor(len(imgs)) as executor:
        executor.map(save_img, list(enumerate(imgs)))
    return 

if __name__ == "__main__":
    main()







