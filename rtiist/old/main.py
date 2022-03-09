import matplotlib.pyplot as plt
import numpy as np

from imaging import Imager
from rtiist.old.ilumination import Iluminator, exR
import asyncio
import aiofiles
import time

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE

imgs = []

async def save_image(path: str, image):
    async with aiofiles.open(path, "wb") as file:
        await file.write(image)

async def main():
    a = Iluminator()
    t1 = asyncio.create_task(a.stim_wrap(2))

    with TLCameraSDK() as sdk:
        camera_list = sdk.discover_available_cameras()
        with sdk.open_camera(camera_list[0]) as camera:

            print("Setting camera parameters...")
            image_acquisition = Imager(camera)
            camera.frames_per_trigger_zero_for_unlimited = 1
            camera.exposure_time_us = 3*1000*1000
            camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
            camera.arm(1)

            while a.done == 0:
                camera.issue_software_trigger()
                await a.on_measure(exR, 3)
                imgs.append(image_acquisition.run())
                print(type(imgs[-1]))
                time.sleep(5)
            
            image_acquisition.stop()

    await t1

if __name__ == "__main__":
    asyncio.run(main())
    for k,img in enumerate(imgs):
        asyncio.run(save_image('/home/pi/LAB/rt-opto/rtiist/img-'+str(k)+'.svg', img))






