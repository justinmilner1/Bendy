import time
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import argparse
import logging
import time
import threading
import sched
import os
import cv2
import numpy as np
import shutil
import loading_page
from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh


class measurement_page(BoxLayout, MDApp, Screen):

    recording_length =  int(open("storage/default_recording_length.txt", "r").read())
    ret = None
    frame = None
    cam = None
    resized_frame = None
    recording = False
    non_recording_thread = None
    recording_thread = None
    end_measurement_bool = False

    take_measurement = False
    frame_count = 1
    measurements = []
    time_stamps = []
    images = []
    initial_time = None
    counter = 0
    remaining_time = recording_length
    image_number = 0

    def on_enter(self):
        self.take_measurement = False
        self.initial_time = None
        self.counter = 0
        self.image_number = 0
        self.cam = cv2.VideoCapture(0)
        if os.path.isdir("./images/curr_measurement_images"):
            shutil.rmtree("./images/curr_measurement_images")
        os.makedirs("./images/curr_measurement_images")
        self.non_recording_thread = Clock.schedule_interval(self.main_loop, 1.0/25.0)


    def main_loop(self, *args):
        #take readings from camera
        self.ret, self.frame = self.cam.read()

        #if user has started measurement: intake image and display time remaining on screen
        if self.take_measurement:
            if not self.initial_time:
                self.initial_time = time.time()
            if self.counter % 12 == 0:
                cv2.imwrite("./images/curr_measurement_images/" + str(self.image_number) +".png", cv2.resize(self.frame, (256, 256)))
                self.counter = 0
                self.image_number+=1
            self.remaining_time = self.recording_length - (time.time() - self.initial_time)
            cv2.putText(self.frame,
                        str(int(self.remaining_time)+1),
                        (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 4,
                        (0, 255, 0), 4)
            # time is up. End the loop, save the images, and go to the next page
            if self.remaining_time <= 0:
                self.non_recording_thread.cancel()
                print("Images length: ", self.image_number)
                # Go to measurement_result_page
                print("going to loading page")
                self.cam.release()
                #self.manager.current = "loading_page"
                try:
                    self.manager.current = "loading_page"
                except:
                    print("warning: went to except block")
                    self.non_recording_thread.cancel()
                return

        #build texture and display on screen
        buffer = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.main_video.texture = texture

        self.counter += 1





    # def start_recording(self):
    #     #start the thread which retrieves the measurements
    #     recording_thread = threading.Thread(target=self.do_recording)
    #     recording_thread.start()
    #
    #     #loop until the recording is done
    #     initial_time = round(time.time())
    #     curr_time = initial_time
    #     while abs(initial_time - curr_time) < self.recording_length:
    #         time.sleep(1)
    #         curr_time = round(time.time())
    #         print(curr_time, initial_time)
    #
    #     #set thread-ending boolean True and wait for it to fininsh up
    #     self.end_measurement_bool = True
    #     recording_thread.join()
    #
    #     #Stop displaying video
    #     self.non_recording_thread.cancel()
    #
    #     #Go to measurement_result_page TODO:need to be able to pass the results somehow too (maybe via file?)
    #     print("going to next page")
    #     self.manager.current = "measurement_result_page"

        #self.resized_frame = cv2.resize(self.frame, (256, 256))
        #logger.info('cam image=%dx%d' % (self.resized_frame.shape[1], self.resized_frame.shape[0]))
        #fps_time = 0
        #Clock.schedule_interval(self.display_video_w_read, 1.0 / 30.0)
        # while True:
        #     self.ret, self.frame = self.cam.read()
        #     #self.display_video_w_read()
        #     self.resized_frame = cv2.resize(self.frame, (256, 256))
        #
        #
        #     logger.debug('image process+')
        #     # humans = e.inference(self.resized_frame)
        #     #
        #     # logger.debug('postprocess+')
        #     # self.resized_frame = TfPoseEstimator.draw_humans(self.resized_frame, humans, imgcopy=False)
        #     #
        #     # logger.debug('show+')
        #     # cv2.putText(self.resized_frame,
        #     #             "FPS: %f" % (1.0 / (time.time() - fps_time)),
        #     #             (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #     #             (0, 255, 0), 2)
        #     #
        #     # #cv2.imshow('tf-pose-estimation result', self.resized_frame)
        #     # fps_time = time.time()
        #     # if cv2.waitKey(1) == 27:
        #     #     break
        #     # logger.debug('finished+')
        #
        # cv2.destroyAllWindows()




    def adjust_recording_length(self, amount):
        if self.recording_length + amount > 25:
            self.ids.positive_button.background_color = (1, 0, 0)
        elif self.recording_length + amount < 1:
            self.ids.negative_button.background_color = (1, 0, 0)
        else:
            self.recording_length += amount
            self.ids.recording_length.text = str(self.recording_length)

    def return_button_background_color(self):
        self.ids.negative_button.background_color = (0, 0, 0)
        self.ids.positive_button.background_color = (0, 0, 0)