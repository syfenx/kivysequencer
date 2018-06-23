import os
# os.environ['KIVY_WINDOW'] = 'sdl2'
# os.environ['KIVY_GL_BACKEND'] = 'sdl2'
# USES KIVYTEST36 VENV

# 1. install system dependencies for kivy
# 2. pip install Cython==0.27.3
# 3. pip install git+https://github.com/kivy/kivy.git@master

import kivy
kivy.require("1.10.0")
import time
from pyo import *
from random import sample
from random import uniform
from string import ascii_lowercase
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
# this is so seqgridwidget can be resized without crashing
# this does not affect the filebrowser scrolling when loading/saving a file
from scrollview_edit import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclelayout import RecycleLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color
from kivy.graphics import (Rectangle, Ellipse, Line)
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.write()
from kivy.core.window import Window
Window.size = (2000, 1500)
from kivy.clock import Clock
from functools import partial
from aengine import AudioEngine, AudioMixer, AudioItem
from file_dialog import *
from file_save_loader import FileSystem
# from aengine_thread import AudioEngine, AudioMixer, AudioItem
# for x in range(120000):
#     print("change back to aengine_thread")

from seq_widget_edit import SeqGridWidget
# for x in range(120000):
#     print("switched to seq_widget_edit")

APPNAME = "xSequencer"
BASE_DIR = "/sounds/"

INF = float('inf')
class NumericInput(GridLayout):
    value = NumericProperty(0)
    min = NumericProperty(-INF)
    max = NumericProperty(INF)
    step = NumericProperty(1)
    text = StringProperty()
    
class SequencerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SequencerLayout, self).__init__(**kwargs)
        self.ae = AudioEngine()
        self.am = AudioMixer()
        self.ae.start()
        # self.ae.run()
        self.bpm = 120
        self.ticks = 4 
        self.metro_val = (60000 / self.bpm / self.ticks) * 0.001
        self.sgr = SeqGridWidget()
        self.loop = False

        self.tracks = []  # PUT THIS IN AENGINE CLASS

        # self.m = Metro(self.metro_val).play()
        # for x in range(100):
        #     print("METRO IS DISABLED")
        
        # self.tf = TrigFunc(self.m, self.trigged)
        self.file_loader = FileLoader()
        self.file_system = FileSystem()

        self.inc = 0

        self.sample_filename_list = []
        for file in os.listdir("sounds"):
            if file.endswith(".wav"):
                self.sample_filename_list.append(file)
            # self.am.addTrack("sounds/" + file)
        print(self.sample_filename_list)
        # self.ae.record()
        # TrigFunc(self.ae.m, self.trigged)

    def trigged(self):
        # print('trigged')
        app = App.get_running_app()
        self.ae.playsound("sounds/kick2.wav")
        # self.ae.run()
        # app.root.Seqdget.move_playhead()
        self.sgr.move_playhead()
        # SeqGridWidget.move_playhead()
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
class Transport(BoxLayout):
    
    def button_about(self):
        print("about pressed")
        cont = GridLayout(cols=1)
        about_txt = "{appname} " \
        "blah blah blah" \
        "blah blah blah" \
        "blah blah blah" \
        "blah blah blah" \
        "rstrstsrt".format(appname=APPNAME)
        cont.add_widget(Label(text=about_txt))

        popup = Popup(title='About {}'.format(APPNAME),
            content=cont,
            size_hint=(None, None), size=(400, 400))
        popup.open()

    # Options audio output selector callback
    # this handles the dynamic buttons
    def audio_opts_button_callback(self, instance):
        print("but was clicked", instance.text)
        app = App.get_running_app()
        app.root.ae.set_output(4)

    def bpm_text(self, instance):
        print("text was entered")
        print(instance.text)
        app = App.get_running_app()
        app.root.m.setTime((60000 / int(instance.text) / 4) * 0.001)

    def button_loop(self, button):
        print("loop")
        app = App.get_running_app()
        # app.root.sgr.loop = True
        if button.state == "down":
            print("down")
            # app.root.sgr.loop = True
            app.root.sgr.loop_bars.loop_func(True)
        else:
            # app.root.sgr.loop = False
            app.root.sgr.loop_bars.loop_func(False)
            print("up")


    def button_open_project(self):
        print("project opened")
        app = App.get_running_app()
        app.root.file_loader.show_load()
        
    def button_save_project(self):
        print("project saved")
        app = App.get_running_app()
        app.root.file_loader.show_save()

    def button_options(self):
        print("options pressed")
        app = App.get_running_app()
        cont = GridLayout(cols=1)
        # retrieve audio outputs / soundcards from audioengine class
        out_list = app.root.ae.get_outputs()
        print(out_list)

        # combine out_list, add to output selector
        for x, y in zip(*out_list):
            # intentional error to remember where left off
            b = Button(id="{}".format(y), text="{} {}".format(x,y))
            b.bind(on_press=self.audio_opts_button_callback)
            cont.add_widget(b)
        for x in self.children:
            print(x)

        tp = TabbedPanel(do_default_tab=False)

        # audio tab
        th_audio = TabbedPanelItem(text="Audio")
        th_audio.content = GridLayout()
        th_audio.add_widget(cont)

        # files tab
        th_files = TabbedPanelItem(text="Files")
        th_files.add_widget(Button(text="files tab content"))
        tp.add_widget(th_audio)
        tp.add_widget(th_files)

        popup = Popup(title='Options',
            content=tp,
            size_hint=(None, None), size=(800, 800))
        popup.open()

    def button_play(self):
        print("play pressed")
        app = App.get_running_app()
        app.root.m.play()
    def button_stop(self):
        print("stop pressed")
        app = App.get_running_app()
        app.root.m.stop()


# Filename lister on left
class Row(Button):
    # button pressed
    def button_pressed(self):
        app = App.get_running_app()
        print(self.text)
        selectedsound = self.text
        print("sel", selectedsound)
        path = "sounds/" + selectedsound
        app.root.ae.playsound(path)

        print("Selected sound is: ", BASE_DIR + selectedsound)
        app.root.sgr.current_sound = BASE_DIR + selectedsound


class FilenameLister(RecycleView):
    pass

class StepPanelScroll(ScrollView):
    pass

class StepPanel_grid_base(GridLayout):
    def button_pressed(self, *args):
        print("buttonpressed")

class StepRowPanel(GridLayout):
    pass

class PlayheadControlBar(GridLayout):
    pass

class SequencerApp(App):
    def __init__(self, **kwargs):
        super(SequencerApp, self).__init__(**kwargs)

    def build(self):
        TRACK_COUNT = 26
        STEP_COUNT = 16
        self.title = APPNAME

        sequencer_layout = SequencerLayout()
        sequencer_layout_grid = GridLayout(cols=1, id="rowcontainer")
        transport = Transport()
        transport.size=(200,60)

        playhead_control_bar = PlayheadControlBar()

        # mixer_panel_grid
        mixer_panel_grid = GridLayout(
            rows=1, padding=10, spacing=10, size_hint=(None, 1))
        mixer_panel_grid.bind(minimum_width=mixer_panel_grid.setter('width'))

        # Vertical buttons in mixer_panel_grid
        anothergrid = GridLayout(cols=1,size_hint_x=None, width=200)
        anothergrid.bind(minimum_width=anothergrid.setter('width'))
        # for x in range(10):
        anothergrid.add_widget(Button(text="anothergrid", size_hint_x=1))
        anothergrid.add_widget(Label(text="anothergrid", size_hint_y=2))
            # anothergrid.add_widget(Label(text="anothergrid", size_hint_x=1))

        # add anothergrid to mixer_panel_grid
        mixer_panel_grid.add_widget(anothergrid)

        # mixer_base holds mixer_panel_grid
        mixer_base = ScrollView(
            size_hint=(1, None),
            size=(200, 400),
            do_scroll_y=False,
            do_scroll_x=True)

        # Add mixer_panel_grid to mixer_base (Scrollview)
        mixer_base.add_widget(mixer_panel_grid)
        
        step_base = ScrollView(
            size_hint=(1,1),
            do_scroll_y=True,
            do_scroll_x=True)
        step_base.bar_width=20
        step_base.scroll_type = ['bars']

        # Sequencer widget (seq_widget.py)
        # SeqWidgetObject = SeqGridWidget()
        SeqWidgetObject = sequencer_layout.sgr

        # Add sequencer widget to main panel (step_base)
        step_base.add_widget(SeqWidgetObject)

        # File name lister on left
        file_list = FilenameLister()
        file_list.size_hint_x = .13

        sample_filename_list = []
        for file in os.listdir("sounds"):
            if file.endswith(".wav"):
                sample_filename_list.append(file)
                file_list.data.insert(0, {'value': file})
        sequencer_layout.add_widget(file_list)
        sequencer_layout_grid.add_widget(transport)
        # sequencer_layout_grid.add_widget(playhead_control_bar)

        sequencer_layout_grid.add_widget(step_base)

        app = App.get_running_app()
        for i in range(TRACK_COUNT):

            # Add number of mixer panels per track added
            # mixer_panel_grid.add_widget(anothergrid)
            mixer_panel_grid.add_widget(
                Button(
                    text="MIXERPANEL \n" + str(sample_filename_list[i]),
                    height=220,
                    width=150,
                    size_hint_x=None))
            
            mixer_panel_grid.add_widget(BoxLayout())

        sequencer_layout_grid.add_widget(mixer_base)
        sequencer_layout.add_widget(sequencer_layout_grid)

        return sequencer_layout

seq_app = SequencerApp()
seq_app.run()