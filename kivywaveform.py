from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from itertools import islice
from kivy.uix.gridlayout import GridLayout

from pyo import *

import random
from random import uniform
import math
import time

s = Server(audio="jack")
s.setInOutDevice(4)
s.boot()
s.start()


def downsample_to_proportion(rows, proportion=1):
    print("List is downsampled")
    return list(islice(rows, 0, len(rows), int(1 / proportion)))


snd_path1 = "sounds/kick1.wav"
snd_path1 = "sounds/long_sample.wav"

t1 = SndTable(snd_path1)
# t1_vals = downsample_to_proportion(t1.getTable(), 0.01)
t1_vals = t1.getTable()


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        # self.fun()
        self.size_hint = (None, None)
        self.height = 200
        self.width = 200

    def trigged(self):
        print("trig")

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 0, 0)
            d = 30.
            # SHOW WHERE MOUSE CLICK IS
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

        self.w_width, self.w_height = self.width, self.height
        self.rect_size_x, self.rect_size_y = 150, 150

        amplitude = self.rect_size_y / 2
        points = []
        print("vals in sample list", len(t1_vals))
        for x in range(0, len(t1_vals)):
            waveform_height = 12.0
            zoom = 0.55  # 0.1 is taller peaks, 0.9 is squashed
            y = math.sin(t1_vals[x] * math.pi /
                         (zoom * 180)) * amplitude * waveform_height
            points.append(x + self.w_width)
            points.append(y + self.w_height)

        print(sum(points) / len(points))

        with self.canvas:
            # DRAW RECT
            Color(.3, .3, .3)
            b = Rectangle(
                pos=(self.w_width - self.rect_size_x / 2,
                     self.w_height - self.rect_size_y / 2),
                size=(self.rect_size_x + self.w_width,
                      self.rect_size_y + self.w_height))
            #DRAW WAVEFORM
            c = get_color_from_hex("#AA8CC5")
            Color(*c)
            Line(points=points)

        print("vals in sample list", len(t1_vals))


class MyPaintApp(App):
    def build(self):
        layout = GridLayout(cols=1)
        layout.add_widget(MyPaintWidget())
        return layout
        # return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()