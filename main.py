import time
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivymd.app import MDApp
import measurement_page

Config.set('graphics', 'resizable', True)
kivy.require('2.1.0')

class past_measurements_page(BoxLayout, MDApp, Screen):
    pass

class measurement_result_page(BoxLayout, MDApp, Screen):
    pass

class settings_page(BoxLayout, MDApp, Screen):
    default_recording_length = int(open("storage/default_recording_length.txt", "r").read())

    def adjust_default_recording_length(self, amount):
        self.default_recording_length += amount
        self.ids.default_recording_length.text = str(self.default_recording_length)
        raw = open("storage/default_recording_length.txt", "r+")
        raw.seek(0)
        raw.truncate()
        raw.write(str(self.default_recording_length))

class help_page(BoxLayout, MDApp, Screen):
    pass

class main_page(BoxLayout, MDApp, Screen):
    current_movement = "Hip1"
    currmov_to_graph = {
        "Hip1": "graph1",
        "Hip2": "graph2",
        "Hip3": "graph3",
    }

    def toggle_movement(self, given_button):
        print("toggle button pressed", str(given_button.text))
        self.current_movement = given_button.text
        self.ids.central_graph.source = 'images/Graphs/' + str(self.currmov_to_graph[self.current_movement] + '.png')



class screenmanager(ScreenManager):
    pass

kv = Builder.load_file('screenmanager.kv')
kv.current = "main_page"

class Main(App):
    def __init__(self):
        App.__init__(self)

    def build(self):
        return kv

Main().run()
