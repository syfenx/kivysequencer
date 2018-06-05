from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from random import randint, uniform
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial
from kivy.graphics.instructions import InstructionGroup
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from pyo import *
import multiprocessing
import time
from aengine_thread import AudioItem
stress_test = False

def paint_stress_test(width, height):
    # stress test
    for x in range(1000):
        Rectangle(pos=(randint(1,width),randint(0, height)), size=(5, 5))

class PlayHead(Widget):
    def __init__(self, height, location=40):
        self.height = height
        self.playhead_line = Line(points=[location, self.height, location, 0])
        self.playhead_line.width = 2

    def moveX(self, increment):
        self.playhead_line.points = [30+increment,self.height,30+increment,0]
        Line.posX= (40)
        print("moveX called")

class GridLines(object):
    def __init__(self):
        self.lines = []
        self.space = 8
        self.snap_thresh = self.space -1
        self.start = 0
        # self.amt = screen_width / self.space
        # self.screen = screen
        # for x in range(0,int(self.amt)):
                # l = pygame.Rect(self.start,0,1,pygame.Surface.get_height(screen))
                # self.lines.append(l)
                # self.start+=self.space

    def drawlines(self):
      c = 4
      v = 16
      for x in range(0,len(self.lines)):
        if c==0:
            # pygame.draw.rect(self.screen, (44,44,44), self.lines[x], 2)
            c = 4
        if v == 0:
            pygame.draw.rect(self.screen, (44,44,44), self.lines[x], 4)
            v = 16
        else:
            pygame.draw.rect(self.screen, (29,29,29), self.lines[x], 1)
        c-=1
        v-=1

def draw_grid(amt, start, width, height, space):

    Color(1, 1, 1)
    for x in range(int(amt)):
        if x % 4 == 0:
            # every 4th line is darker
            # vertical line - thick width
            Color(.2,.2,.2)
            Line(points=[0+start, height, 0+start, 0]).width=2
        else:
            Color(.2,.2,.2)
            # vertical line - normal width
            Line(points=[0+start, height, 0+start, 0])
        start+=space

        Color(.2,.2,.2)
        # horizontal line
        Line(points=[0, start, width, start])

class SeqGridWidget(Widget):
    def __init__(self, **kwargs):
        super(SeqGridWidget, self).__init__(**kwargs)

        # Change main widget background color
        Window.clearcolor=get_color_from_hex("#444444")

        # main widget
        self.audio_items = []
        self.d=5.
        self.size_hint=(None,None)
        self.size=(11100,11100)
        self.width = self.size[0]
        self.height = self.size[1]

        # grid
        self.space = 64
        self.start = 0
        self.amt = self.width / self.space

        self.drag = False
        self.selected_item = None

        # Playhead
        self.ph = Line(points=[30,self.height,30, self.height])
        self.ph.width = 6
        self.inc = 0
        self.playhead_increment = 0
        self.isPlayheadAdjust = False

        # loop bars
        self.loop = False
        self.loops = InstructionGroup()

        self.items = []
        self.grid_lines_main = []

        with self.canvas:
            draw_grid(self.amt,self.start,self.width,self.height, self.space)

            # Change playhead color to blue
            Color(0.25, 0.95, 0.87, 1)
        self.canvas.add(self.ph)

        with self.canvas:
            # top grey horizontal bar
            # controls playhead skipping / looping markers
            Color(0.43, 0.43, 0.43, 1)
            Rectangle(pos=(0,self.height-20), size=(self.width, 20))


    def adjust_playhead(self, touch):
        if touch.y > (self.height-20):
            self.isPlayheadAdjust = True
            self.playhead_increment = touch.x - self.space * 2
            p = [touch.x, self.height, touch.x, 0]
            with self.canvas:
                self.ph.points = p
        else:
            self.isPlayheadAdjust = False

    # temporarily moves playhead on screen
    def move_playhead(self):
        self.playhead_increment += self.space

        # if playhead reaches end of window width, loop back to beginning
        # if self.playhead_increment > Window.size[0]:
        #     self.playhead_increment=0
        # self.size is for testing inside the widget, Window.size[0]
        # is normal use
        if self.playhead_increment > self.size[0]:
            self.playhead_increment=0
        
        p = [30+self.playhead_increment,self.height,30+self.playhead_increment,0]
        # print(p)
        with self.canvas:
            self.ph.width = 2
            self.ph.points = p
            # Line(points=p)
            # self.playhead.playhead_line
            # self.playhead.playhead_line.width=300
            # print(self.playhead.playhead_line)
            # self.playhead.moveX(self.playhead_incremen)
    def loop_func(self, loop):
        if loop:
                Color(0,1,1)
                loopL = Line(points=[30+20,self.height,30+20,0])
                loopR = Line(points=[30+70,self.height,30+70,0])
                handle_size=(20,20)
                top_padding = 20
                loopHandleL = Rectangle(pos=(loopL.points[0]-(handle_size[0]/2),self.height-top_padding), size=handle_size)
                loopHandleR = Rectangle(pos=(loopR.points[0]-(handle_size[0]/2),self.height-top_padding), size=handle_size)
                self.loops.add(loopL)
                self.loops.add(loopR)
                self.loops.add(loopHandleL)
                self.loops.add(loopHandleR)
                self.canvas.add(self.loops)
        else:
            # self.canvas.clear()
            # self.loops.clear()
            self.canvas.remove(self.loops)
            self.loops.clear() # self.canvas.clear()
    def show_audio_items(self):
        print("*"*20)
        print("Audio item count: ", len(self.audio_items))
        for item in self.audio_items:
            print("Block pos", item.shape.pos)
            print("Block size", item.shape.size)
        print("*"*20)
    def on_touch_down(self, touch):
        super(SeqGridWidget, self).on_touch_down(touch)
        self.show_audio_items()
        # if mouse is less than grid height-20, change pos of playhead
        # on touch down
        # if touch.y > (self.height-20):
        #     self.playhead_increment = touch.x - self.space*2
        # enables dragging of playhead
        self.adjust_playhead(touch)

        # for item in self.block_list:
        #     self.canvas.add(item)
        # self.canvas.add(self.block_list)
        with self.canvas:
            # the test can of course be simplified: a.pos[0] < touch.x < a.pos[0] + a.size[0] and a.pos[1] < touch.y < a.pos[1] + a.size[1]
            # just put a = self.a on the line before
            # if playhead is being moved, don't place a block/rect
            if self.isPlayheadAdjust == False:
                for box in self.audio_items:
                    if touch.x >=box.shape.pos[0] and touch.x <= box.shape.pos[0]+box.shape.size[0]*2 and touch.y >=box.shape.pos[1] and touch.y <= box.shape.pos[1]+box.shape.size[1]*2:
                        self.drag = True
                        self.selected_item = box
                        print("selected item",self.selected_item)
                        print("in bounds")
                        # self.audioitems.append([audioitemclass, audioitemshape])
                        # for audioitem in self.audioitems:
                        #     aitem = audioitem[0]
                        #     aitemshape = audioitem[1]

                if self.drag == False:
                    Color(1, uniform(0,1), 0)
                    box_size = self.space
                    ai = AudioItem("sounds/snare1.wav", 100, 100, 100, [touch.x - box_size/2, touch.y - box_size/2], [box_size, box_size])
                    # self.a=Rectangle(pos=(touch.x - box_size / 2, touch.y - box_size / 2), size=(box_size, box_size))
                    # add to item list
                    self.audio_items.append(ai)

                    # add shape/rect to canvas
                    # self.canvas.add(self.a)

                    # Label connected to audio block
                    # b = Label(text="Sound clip")
                    # b.pos = (touch.x-45, touch.y)
                    # self.add_widget(b)
                    

                if stress_test:
                    paint_stress_test(self.width, self.height)

    def on_touch_up(self, touch):
        self.drag = False

    def on_touch_move(self, touch):
        # if mouse is less than grid height-20, change pos of playhead
        # on touch drag
        # if touch.y > (self.height-20):
        #     self.playhead_increment = touch.x - self.space*2
        self.adjust_playhead(touch)

        if self.drag == True:
            self.selected_item.shape.pos = (touch.x - self.selected_item.shape.size[0]/2, touch.y-self.selected_item.shape.size[1]/2)
            self.selected_item.text.pos = (touch.x - self.selected_item.shape.size[0]/2, touch.y-self.selected_item.shape.size[1]/2)
            print("drag " + str(self.selected_item.shape.pos))
        else:
            self.drag = False

       
class SeqGridWidgetApp(App):
    def build(self):
        return SeqGridWidget()


if __name__ == '__main__':
    SeqGridWidgetApp().run()