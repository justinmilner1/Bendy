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

class measurement_page(BoxLayout, MDApp, Screen):

    recording_length =  int(open("storage/default_recording_length.txt", "r").read())
    ret = None
    frame = None

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        print("ids: ", self.ids)

    def load_video(self, *args):
        self.ret, self.frame = self.capture.read()

        buffer = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.main_video.texture = texture

    def adjust_recording_length(self, amount):
        self.recording_length += amount
        self.ids.recording_length.text = str(self.recording_length)

    def start_recording(self):
        print("starting recording")
