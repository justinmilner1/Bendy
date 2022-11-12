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
import measurement_result_page
import past_measurements_page
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

Config.set('graphics', 'resizable', True)
kivy.require('2.1.0')

class loading_page(BoxLayout, MDApp, Screen):
    pass

class settings_page(BoxLayout, MDApp, Screen):
    default_recording_length = int(open("storage/default_recording_length.txt", "r").read())
    default_movement_type = open("storage/default_graph.txt", "r").read()
    internal_name_to_external_name = {
        "Hip_Abduction": "Hip Abduction",
        "Hip_Flexion": "Hip Flexion",
        "Hip_Internal_Rotation": "Hip Internal Rotation",
    }

    def on_enter(self):
        self.ids.main_dropdown_button.text = self.default_movement_type
        movements_list = ["Hip_Abduction", "Hip_Flexion", "Hip_Internal_Rotation"]

        dropdown = DropDown()
        for movement in movements_list:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(text=movement, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            # then add the button inside the dropdown
            dropdown.add_widget(btn)

        self.ids.main_dropdown_button.bind(on_release=dropdown.open)
        #dropdown.bind(on_select=lambda instance, x: setattr(self.ids.main_dropdown_button, 'text', x) ) #this should also save the value to default_grapht.txt
        dropdown.bind(on_select=lambda instance, x: self.change_default_movement_type(x)) #this should also save the value to default_grapht.txt

    def change_default_movement_type(self, x):
        setattr(self.ids.main_dropdown_button, 'text', x)
        raw = open("storage/default_graph.txt", "r+")
        raw.seek(0)
        raw.truncate()
        self.default_movement_type = x
        raw.write(str(self.default_movement_type))

    def adjust_default_recording_length(self, amount):
        max_recording_length = 25
        if self.default_recording_length + amount > max_recording_length:
            self.ids.positive_button.background_color = (1,0,0)
        elif self.default_recording_length + amount <= 0:
            self.ids.negative_button.background_color = (1,0,0)
        else:
            self.default_recording_length += amount
            self.ids.default_recording_length.text = str(self.default_recording_length)
            raw = open("storage/default_recording_length.txt", "r+")
            raw.seek(0)
            raw.truncate()
            raw.write(str(self.default_recording_length))



    def return_button_background_color(self):
        self.ids.negative_button.background_color = (0, 0, 0)
        self.ids.positive_button.background_color = (0, 0, 0)


class help_page(BoxLayout, MDApp, Screen):
    pass

class main_page(BoxLayout, MDApp, Screen):
    current_movement_type = "Hip Abduction"
    external_name_to_internal_name = {
        "Hip Abduction": "Hip_Abduction",
        "Hip Flexion": "Hip_Flexion",
        "Hip Internal Rotation": "Hip_Internal_Rotation",
    }
    internal_name_to_external_name = {
        "Hip_Abduction": "Hip Abduction",
        "Hip_Flexion": "Hip Flexion",
        "Hip_Internal_Rotation": "Hip Internal Rotation",
    }

    def on_pre_enter(self):
        '''
        Load the graph which was set as the default graph

        :return:
        '''
        default_graph = str(open("storage/default_graph.txt", "r").read())
        self.ids.central_graph.source = 'images/Graphs/' + default_graph + '.png'
        self.ids.go_to_past_measurements_button.text = "View past " + str(default_graph) + " measurements"
        self.ids.take_measurement_button.text = "Take new " + str(default_graph) + " measurement"


    def toggle_movement_type(self, given_button):
        #change movement_type
        self.current_movement_type = given_button.text
        internal_name = self.external_name_to_internal_name[self.current_movement_type]

        #change central graph
        self.ids.central_graph.source = 'images/Graphs/' + internal_name + '.png'

        #change take and view measurement button texts
        self.ids.go_to_past_measurements_button.text = "View past " + str(given_button.text) + " measurements"
        self.ids.take_measurement_button.text = "Take new " + str(given_button.text) + " measurement"


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
