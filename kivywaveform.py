from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from itertools import islice
from kivy.uix.gridlayout import GridLayout


from pyo import *

import random
from random import uniform
import math
import time

s = Server(duplex=0)
s.setInOutDevice(4)
s.boot()
s.start()
def downsample_to_proportion(rows, proportion=1):
    print("List is downsampled")
    return list(islice(rows, 0, len(rows), int(1/proportion)))

snd_path1 = "sounds/kick1.wav"
snd_path1 = "sounds/long_sample.wav"

t1 = SndTable(snd_path1)
t1_vals = downsample_to_proportion(t1.getTable(), 0.01)
# t1_vals = t1.getTable()
# 1.getTable()
# print(t1.getTable())


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.fun()
        self.size_hint = (None, None)
        self.height = 200
        self.width = 200

        with self.canvas:
            # WIDGET BOUNDING BOX
            Color(1,0,0)
            cc =Rectangle(pos=(self.width/2, self.height/2), size=(self.width,self.height))

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 0, 0)
            d = 30.
            # SHOW WHERE MOUSE CLICK IS
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            self.fun()

            # c = (uniform(0.1,1.0), 0,0.3)
            # Bounding box (red) size
            w_width, w_height = self.width, self.height
            
            # gray box size
            Color(.3,.3,.3)
            rect_size_x, rect_size_y =  150, 150
            b = Rectangle(pos=(w_width - rect_size_x / 2, w_height - rect_size_y  / 2),
            size=(rect_size_x, rect_size_y))

        # size = 250
        amplitude = rect_size_y / 2
        points = []
        print("vals in sample list", len(t1_vals))
        for x in range(0, len(t1_vals)):
            # print('hey'
            y = math.sin(t1_vals[x] * math.pi / (0.1*180)) * amplitude
            points.append(x*2 / w_width + w_width-rect_size_x/2)
            points.append(y + w_height )

            # original points append
            # points.append(x + w_width - rect_size_x / 2)
            # points.append(y + w_height - rect_size_y / 2)
        #  now points should be of form [x0, y0, x1, y1, ...]
        # not [(x0, y0), ...]
        with self.canvas:
            Color(0,1,0)
            Line(points=points)


    # def fun(self,zoom=.1):
        # pass
        # t1 = time.time()
        # global c
        # remove the old shapes.
        # for item in c.find_all():
            # c.delete(item)
            # print()
        # for item in t1_vals:
        #     print(item)
        # calculate a random amplitude
        # a = Button(text="")
        # a.pos = (touch.x - d / 2, touch.y - d /2)
        # self.add_widget(a)

        print("vals in sample list", len(t1_vals))

                    # unedited

        # size=50
        # amplitude = 5 * int(size) / 2
        # points = []
        # for x in range(0, len(t1_vals)):
        #     # print('hey')
        #     y = math.sin(t1_vals[x] * math.pi / (0.02*180)) * amplitude + int(size) / 2
        #     # this was edited, it centers on mouse click.
        #     points.append(x+touch.x/2-touch.x/2)
        #     points.append(y+touch.y/2+touch.y/2)


        #  now points should be of form [x0, y0, x1, y1, ...]
        # not [(x0, y0), ...]
            # print(points)
        # with self.canvas:
            # Color(1, 1, 0)
            # Line(points=points)

    def fun(self):
        # size=50
        # amplitude = 5 * int(size) / 2
        # points = []
        # for x in range(0, len(t1_vals)):
        #     # print('hey')
        #     y = math.sin(t1_vals[x] * math.pi / (0.02*180)) * amplitude + int(size) / 2
        #     # this was edited, it centers on mouse click.
        #     points.append(x+touch.x/2-touch.x/2)
        #     points.append(y+touch.y/2+touch.y/2)

            print("selfsize", self.size[0], self.size[1])
            # Line(points=points)


                    # unedited


class MyPaintApp(App):

    def build(self):
        layout = GridLayout(cols=1)
        layout.add_widget(MyPaintWidget())
        return layout
        # return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()