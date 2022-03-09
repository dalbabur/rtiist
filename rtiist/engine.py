import threading


from imaging import Imager
from ilumination import Iluminator, exG, plate96_full, ex584
from concurrent.futures import ThreadPoolExecutor

import time

from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_camera_enums import OPERATION_MODE



class Engine:
    def __init__(self) -> None:

        pass
