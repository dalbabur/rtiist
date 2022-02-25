from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK


""" ImageAcquisitionThread

This class derives from threading.Thread and is given a TLCamera instance during initialization. When started, the 
thread continuously acquires frames from the camera and converts them to PIL Image objects. These are placed in a 
queue.Queue object that can be retrieved using get_output_queue(). The thread doesn't do any arming or triggering, 
so users will still need to setup and control the camera from a different thread. Be sure to call stop() when it is 
time for the thread to stop.

"""


class Imager:
    
    def __init__(self, camera):
        self._camera = camera
        self._previous_timestamp = 0

        # setup color processing if necessary
        if self._camera.camera_sensor_type != SENSOR_TYPE.BAYER:
            # Sensor type is not compatible with the color processing library
            self._is_color = False
        else:
            self._mono_to_color_sdk = MonoToColorProcessorSDK()
            self._image_width = self._camera.image_width_pixels
            self._image_height = self._camera.image_height_pixels
            self._mono_to_color_processor = self._mono_to_color_sdk.create_mono_to_color_processor(
                SENSOR_TYPE.BAYER,
                self._camera.color_filter_array_phase,
                self._camera.get_color_correction_matrix(),
                self._camera.get_default_white_balance_matrix(),
                self._camera.bit_depth
            )
            self._is_color = True

        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = 1000  # Do not want to block for long periods of time
        self._image = None
        self._stop_event = False

    def get_output(self):
        return self._image

    def _get_color_image(self, frame):
        # verify the image size
        width = frame.image_buffer.shape[1]
        height = frame.image_buffer.shape[0]
        if (width != self._image_width) or (height != self._image_height):
            self._image_width = width
            self._image_height = height
            print("Image dimension change detected, image acquisition thread was updated")
        # color the image. transform_to_24 will scale to 8 bits per channel
        color_image_data = self._mono_to_color_processor.transform_to_24(frame.image_buffer,
                                                                         self._image_width,
                                                                         self._image_height)
        color_image_data = color_image_data.reshape(self._image_height, self._image_width, 3)
        # return PIL Image object
        return color_image_data

    def _get_image(self, frame):
        # no coloring, just scale down image to 8 bpp and place into PIL Image object
        scaled_image = frame.image_buffer >> (self._bit_depth - 8)
        return scaled_image

    def run(self):
        if not self._stop_event:
            try:
                frame = self._camera.get_pending_frame_or_null()
                if frame is not None:
                    print('got frame')
                    if self._is_color:
                        pil_image = self._get_color_image(frame)
                    else:
                        pil_image = self._get_image(frame)
                    self._image = pil_image
                    print(type(pil_image))

            except Exception as error:
                print("Encountered error: {error}, image acquisition will stop.".format(error=error))
                self.stop()
        
        return self._image

    def stop(self):
        self._stop_event = True  
        print("Image acquisition has stopped")
        if self._is_color:
            self._mono_to_color_processor.dispose()
            self._mono_to_color_sdk.dispose()