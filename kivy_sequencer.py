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
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclelayout import RecycleLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.behaviors import DragBehavior
# from pyo import *
from kivy.graphics import Color
from kivy.graphics import (Rectangle, Ellipse, Line)
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
from kivy.clock import Clock
from functools import partial
from aengine import AudioEngine, AudioMixer, AudioItem
from seq_widget import MyPaintWidget

from kivy.effects.scroll import ScrollEffect

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
        # self.m = Metro(self.metro_val)
        # self.tf = TrigFunc(self.m, self.trigged)
        # drawing on canvas example
        # with self.canvas:
        #     Color(0, 1, 0, 1)
        #     Rectangle(pos=(0, 100), size=(400, 400))

        
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
        # print("trigged")
        app = App.get_running_app()
        self.inc += 1
        # print(self.parent.children[0].children[0].children[1].children)
        if self.inc == 16:
            self.inc = 0
        # for row in self.parent.children[0].children[0].children[1].children:

        # self.tracks[11].play()
        # if self.tracks is not None:
        #     for track in self.tracks:
        #         print(track)
        #         print(track.filename)
        # track.sample[]
            # mixer_panel_grid.add_widget(Button(text="hahaha"))
        # track.play()
        # for row in app.root.children[0].children[1].children:
            # self.iterate_buttons(row)
        for row in app.step_panel_grid.children:
            # print(row.children[0])
            for button in row.children[0].children[0].children:
                # print(button)
                # print("chil",row.children[0].children[0].children)
                # print(type(button))
                print(button.background_color)
                if type(button) is StepButton:
                    if button.step_id == str(self.inc):
                        if button.state == "down":
                            button.background_color = get_color_from_hex(
                                "#0fff22")
                            path = "sounds/" + button.parent.parent.parent.fn
                            # app.root.ae.playsound(path)
                            # self.tracks[self.inc].setfn(path)
                            # self.tracks[self.inc].sf.speed = uniform(0, 1)
                            # self.tracks[self.inc].play()
                                    # app.root.am.tracks[self.inc].play()
                            # for t in app.root.am.tracks:
                            #     if t.filename == path:
                            #         t.play()
                            # print(uniform(0,1))
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
        # self.parent.remove_widget(self)
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
        app = App.get_running_app()
        # for i in range(16):
        print("problem")

        # add to StepRowPanel
        # self.parent.children[1].add_widget(row)
        for a in range(25):
            row = StepRow()
            # but = StepButton()
            # row.fn = "fn " + str(i)
            row.fn = "New Track"
            for x in range(16):
                row.add_widget(
                    StepButton(step_id=str(x), id=f"but_{x}", text=f"{x}"))
            app.steprowpanel.add_widget(row)
    def button_play(self):
        app = App.get_running_app()
        print("play pressed")
        app.root.m.play()
    def button_stop(self):
        app = App.get_running_app()
        app.root.m.stop()



class Row(Button):
    # part of filename lister on the left
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
        for x in range(10):
            anothergrid.add_widget(Button(text="anothergrid", size_hint_x=1))

        # add anothergrid to mixer_panel_grid
        mixer_panel_grid.add_widget(anothergrid)

        # for j in range(TRACK_COUNT):
        #     mixer_panel_grid.add_widget(
        #         Button(
        #             text="MIXERPANEL " + str(j),
        #             height=200,
        #             width=150,
        #             size_hint=(None, 1)))

        # mixer_base holds mixer_panel_grid
        mixer_base = ScrollView(
            size_hint=(1, None),
            size=(200, 400),
            do_scroll_y=False,
            do_scroll_x=True)

        # Add mixer_panel_grid to mixer_base(Scrollview)
        mixer_base.add_widget(mixer_panel_grid)

        # self.steprow_base = RecycleView(
        #     # size_hint=(1,1)
        # )
        # # holds step rows
        # # global steprowpanel
        self.steprowpanel = StepRowPanel(
            cols=1, 
            size_hint=(1,1))
        
        # self.steprowpanel.bind(minimum_height=self.steprowpanel.setter('height'))
        # self.steprow_base.add_widget(self.steprowpanel)
        # self.steprowpanel = StepRowPanel()
        #################################################################################
        #################################################################################


        # recursion error on resize because I think this height/width is too high.
        # step_panel_grid = GridLayout(
        #     cols=1,size_hint=(None,None),height=20000,width=20000)
        # step_panel_grid.bind(minimum_width=step_panel_grid.setter('width'))

        step_base = ScrollView(
            size_hint=(1,1),
            do_scroll_y=True,
            do_scroll_x=True)
        step_base.bar_width=20
        step_base.scroll_type = ['bars']

    # scroll = ScrollView()
# scroll.effect_cls = DummyEffect
        step_base.effect_cls = DummyEffect
        # Add mixer_panel_grid to mixer_base(Scrollview)
        b = MyPaintWidget()

        # step_panel_grid.add_widget(b)
        step_base.add_widget(b)
        # LEFT OFF HERE
        print("This line is last attempt at grid, testing paintwidget")
        # step_base.add_widget(self.step_panel_grid)
        #################################################################################
        #################################################################################

        # mixer_base = ScrollView(
        #     size_hint=(1, None),
        #     size=(200, 400),
        #     do_scroll_y=False,
        #     do_scroll_x=True)
        # step_panel_scroll = StepPanelScroll(
        #     size_hint=(1,None),
        #     do_scroll_y=True
        # )
        # step_panel_main.size_hint_x = 1
        # step_panel_main.size_hint_y=None
        # a = GridLayout(cols=1,size_hint_y=None)
        
        # a.bind(minimum_height=a.setter('height'))
        # for x in range(0,22):
            # step_panel_main.data.insert(0, {'value': str(x)})
            # self.step_panel_grid.add_widget(StepRow())
        # step_panel_scroll.add_widget(a)

        # lists samples on left
        file_list = FilenameLister()
        file_list.size_hint_x = .13
        for x in range(0,100):
            file_list.data.insert(0, {'value': str(x)})

        sample_filename_list = []
        for file in os.listdir("sounds"):
            if file.endswith(".wav"):
                sample_filename_list.append(file)
                file_list.data.insert(0, {'value': file})
        sequencer_layout.add_widget(file_list)
        # sequencer_layout.add_widget(step_panel_main)
        sequencer_layout_grid.add_widget(transport)
        print(sample_filename_list)


        # RECYCLEVIEW
        # self.sp_grid_base = StepPanel_grid_base(cols=1)
        # self.sp_grid_base.add_widget(step_panel_scroll)
        
        sequencer_layout_grid.add_widget(step_base)
        # self.steppanel2.size_hint_y=1
        # self.steppanel2.viewclass = "StepRow"

        # self.steppanel2_grid = StepPanel_base_grid(cols=1)
        # self.steppanel2_grid.bind(minimum_height=self.steppanel2_grid.setter('height'))
        # self.steppanel2.size=(1000, 100)

        # RECYCLEBOXLAYOUT
        # self.step_recy_box = RecycleBoxLayout(
        #     size_hint=(1,None),
        #     spacing=50)

    # RecycleBoxLayout:
    #     default_size: None, dp(60)
    #     default_size_hint: 1, None
    #     size_hint_y: None
    #     height: self.minimum_height
    #     orientation: 'vertical'
    #     spacing: dp(30)
        # for x in range(0,100):
            # self.steppanel2.data.insert(0, {'value': str(x)})
            # self.steppanel2_grid.add_widget(StepRow())


        # self.steppanel2_grid.bind(minimum_height=self.steppanel2_grid.setter('height'))



#   RecycleBoxLayout:
#     default_size: None, dp(25)
#     default_size_hint: 1, None
#     size_hint_y: None
#     height: self.minimum_height
#     orientation: 'vertical'
#     spacing: dp(60)

        # for x in range(20):
        #     # self.step_recy_box.add_widget(Button(text="crap"))



        # Add multiple steps(StepRow) to steprowpanel
        # sequencer_layout_grid.add_widget(self.steprow_base)
        app = App.get_running_app()
        for i in range(TRACK_COUNT):
            row = StepRow(id="row_{}".format(i))
            # mp.add_widget(Button(text="MIXERPANEL",height=300,size_hint_y=None))
            # row.fn = "fn " + str(i)
            # append audioitem to tracks list

            # Add number of mixer panels per track added

            mixer_panel_grid.add_widget(
                Button(
                    text="MIXERPANEL \n" + str(sample_filename_list[i]),
                    height=200,
                    width=150,
                    size_hint=(None, 1)))
            # app.root.tracks.append(
            #     AudioItem("sounds/" + sample_filename_list[i], 0.3, 0, 0))

            row.fn = sample_filename_list[i]
            # self.steprowpanel.add_widget(row)
            for x in range(STEP_COUNT):
                row.add_widget(
                    StepButton(step_id=str(x), id=f"but_{x}", text=f"{x}"))
                # self.step_recy_box.add_widget(Button(text="crap"))

        # print list of tracks/samples in use
        # for track in self.tracks:
        #     print(track.filename)
            # track.play()
        sequencer_layout_grid.add_widget(mixer_base)
        sequencer_layout.add_widget(sequencer_layout_grid)
        # for item in self.steprowpanel.children:
        #     print(item.id)

        # b = MyPaintWidget()
        # print("MyPaintWidget added")
        # sequencer_layout_grid.add_widget(b)
        return sequencer_layout


seq_app = SequencerApp()
seq_app.run()
