import time
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
import csv

class past_measurements_page(BoxLayout, MDApp, Screen):

    layout = None

    def on_pre_enter(self, *args):
        '''
        Loop through each entry in past_results.csv
            Create an object (widget?) for each measurement/image pair and add it to the screen
        '''
        #self.layout = GridLayout(cols=2, spacing=10)

        #self.layout.bind(minimum_height=self.layout.setter('height'))
        with open('./storage/past_results.csv', 'r') as past_results_file:
            datareader = csv.reader(past_results_file)
            for row in datareader:
                print("row: ", row)
                measurement_object = BoxLayout(orientation="vertical", padding='4dp')

                image = Image(source=row[3], size_hint=(1,1))
                measurement_object.add_widget(image)

                angle_button = Button(text=row[1], size_hint_y=.1)
                measurement_object.add_widget(angle_button)

                datetime_button = Button(text=row[2], size_hint_y=.1)
                measurement_object.add_widget(datetime_button)

                self.ids.vertical_box_layout.add_widget(measurement_object)
                #self.layout.add_widget(measurement_object)

        #self.ids.vertical_box_layout.add_widget(self.layout)

    def leave(self, *args):
        if self.layout:
            self.ids.vertical_box_layout.remove_widget(self.layout)
        #self.ids.vertical_box_layout.clear_widgets()
        self.layout = None
        self.manager.current = "main_page"