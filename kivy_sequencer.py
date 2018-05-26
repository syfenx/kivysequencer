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
from random import sample
from random import uniform
from string import ascii_lowercase
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
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
from seq_widget import SeqGridWidget

from kivy.effects.scroll import ScrollEffect

APPNAME = "xSequencer"

class DummyEffect(ScrollEffect):
    pass

class SequencerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SequencerLayout, self).__init__(**kwargs)
        self.ae = AudioEngine()
        self.am = AudioMixer()
        self.ae.start()
        self.metro_val = .125
        print("remember to play the metro")

        self.tracks = []  # PUT THIS IN AENGINE CLASS

        self.inc = 0

        self.sample_filename_list = []
        for file in os.listdir("sounds"):
            if file.endswith(".wav"):
                self.sample_filename_list.append(file)
            # self.am.addTrack("sounds/" + file)
        print(self.sample_filename_list)
        # self.ae.record()

    def trigged(self):
        app = App.get_running_app()
        self.inc += 1

        if self.inc == 16:
            self.inc = 0

        for row in app.step_panel_grid.children:
            for button in row.children[0].children[0].children:
                print(button.background_color)
                if type(button) is StepButton:
                    if button.step_id == str(self.inc):
                        if button.state == "down":
                            button.background_color = get_color_from_hex(
                                "#0fff22")
                            path = "sounds/" + button.parent.parent.parent.fn
                    else:
                        button.background_color = (.33, .33, .33, 1)


class StepRow(BoxLayout):
    # def __init__(self, **kwargs):
    #     super(StepRow, self).__init__(**kwargs)
    #     app = App.get_running_app()
    #     print("track added")
    #     for x in range(10):
    #         # self.add_widget(ToggleButton(text="hey", size_hint=(0.5,0.9)))
    #         self.add_widget(StepButton(step_id=str(x), id=f"but_{x}", text=f"{x}"))

    def button_pressed(self):
        app = App.get_running_app()
        print("track was added by button")
        app.root.am.addTrack("sounds/snare1.wav")
        mixer_panel_grid.add_widget(
            Button(
                text="MIXERPANEL \n" + str("dynamicadd"),
                height=200,
                width=150,
                size_hint=(None, 1)))

    def slider_change(self, val):
        app = App.get_running_app()
        # app.root.mm.setAmp(vin=1, vout=1, amp=val)
        app.root.metro_val = val
        app.root.m.setTime(val)
        print(val)
        

class BeatRow(StepRow):
    pass


class Transport(BoxLayout):
    def button_add_track(self):
        # app = App.get_running_app()
        # for i in range(16):
        print("Add track button")

        # # add to StepRowPanel
        # for a in range(25):
        #     row = StepRow()
        #     # but = StepButton()
        #     # row.fn = "fn " + str(i)
        #     row.fn = "New Track"
        #     for x in range(16):
        #         row.add_widget(
        #             StepButton(step_id=str(x), id=f"but_{x}", text=f"{x}"))
        #     app.steprowpanel.add_widget(row)

    def button_about(self):
        print("about pressed")
        cont = GridLayout(cols=1)
        about_txt = "{appname} was developed for fun in my spare time" \
        "blah blah blah" \
        "blah blah blah" \
        "blah blah blah" \
        "blah blah blah" \
        "rstrstsrt".format(appname=APPNAME)
        cont.add_widget(Label(text=about_txt))

        popup = Popup(title='About {}'.format(APPNAME),
            content=cont,
            size_hint=(None, None), size=(1400, 1400))
        popup.open()

    # Options audio output selector callback
    # this handles the dynamic buttons
    def callback(self, instance):
        print("but was clicked", instance.text)
        intentional error to remember where left off

    def button_options(self):
        print("options pressed")
        app = App.get_running_app()
        cont = GridLayout(cols=1)
        # retrieve audio outputs / soundcards from audioengine class
        out_list = app.root.ae.get_outputs()
        print(out_list)

        # combine out_list, add to output selector
        for x, y in zip(*out_list):
            intentional error to remember where left off
            b = Button(id="{}".format(y), text="{} {}".format(x,y))
            b.bind(on_press=self.callback)
            cont.add_widget(b)
        for x in self.children:
            print(x)

        popup = Popup(title='Sound Options',
            content=cont,
            size_hint=(None, None), size=(400, 400))
        popup.open()

    def button_play(self):
        print("play pressed")
        # app.root.m.play()
    def button_stop(self):
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


class FilenameLister(RecycleView):
    pass

class StepPanelScroll(ScrollView):
    pass

class StepPanel_grid_base(GridLayout):
    def button_pressed(self, *args):
        print("buttonpressed")

class StepRowPanel(GridLayout):
    pass

class StepButton(ToggleButton):
    step_id = StringProperty('')
    pat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    background_color_normal = ListProperty([1, 1, 1, 0.5])

    def button_pressed(self, *args):
        print('State ' + self.state)
        print('Text ' + self.text)
        path = "sounds/" + "snare1.wav"
        # print(self.parent.fn)
        if self.state == "down":
            self.background_color_normal = ""
            # self.background_color = (1, 0, 0, 1)
            self.background_color = get_color_from_hex("#ff0f7f")
            # self.pat[int(self.step_id)] = 1
        else:
            self.background_color_normal = ""
            # self.pat[int(self.step_id)] = 0
            # App.get_running_app().root.playsound(path)
            self.background_color = get_color_from_hex("#333333")
        print(self.parent.id, self.pat)

    def change_color_back(self, button, *args):
        button.background_color = (0, 1, 0, 1)


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

        # Add test buttons to top transport panel
        for x in range(3):
            transport.add_widget(Button(text=f"testing {x}"))

        # mixer_panel_grid
        global mixer_panel_grid
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
        SeqWidgetObject = SeqGridWidget()

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

        sequencer_layout_grid.add_widget(step_base)

        app = App.get_running_app()
        for i in range(TRACK_COUNT):
            row = StepRow(id="row_{}".format(i))

            # Add number of mixer panels per track added
            # mixer_panel_grid.add_widget(anothergrid)
            mixer_panel_grid.add_widget(
                Button(
                    text="MIXERPANEL \n" + str(sample_filename_list[i]),
                    height=220,
                    width=150,
                    size_hint_x=None))
            
            mixer_panel_grid.add_widget(BoxLayout())
            # mixer_panel_grid.add_widget(Button(text="2nd button", height=100, size_hint_y=.2))
            # mixer_panel_grid.add_widget(Slider(size_hint=(None,None), max=100, value=4, orientation='vertical'))

            row.fn = sample_filename_list[i]
            for x in range(STEP_COUNT):
                row.add_widget(
                    StepButton(step_id=str(x), id=f"but_{x}", text=f"{x}"))

        sequencer_layout_grid.add_widget(mixer_base)
        sequencer_layout.add_widget(sequencer_layout_grid)

        return sequencer_layout


seq_app = SequencerApp()
seq_app.run()