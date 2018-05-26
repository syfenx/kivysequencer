from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from random import randint, uniform
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from pyo import *

def paint_stress_test(width, height):
    # stress test
    for x in range(102333):
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
            Line(points=[0+start, height, 0+start, 0]).width=4
        else:
            Color(.2,.2,.2)
            # vertical line - normal width
            Line(points=[0+start, height, 0+start, 0])
        start+=space

        Color(.2,.2,.2)
        # horizontal line
        Line(points=[0, start, width, start])
    print("grid drawrwww")

class SeqGridWidget(Widget):
    def __init__(self, **kwargs):
        super(SeqGridWidget, self).__init__(**kwargs)

        # Change background color
        Window.clearcolor=get_color_from_hex("#444444")

        self.block_list = []
        self.inc = 0
        self.d=5.
        self.size_hint=(None,None)
        self.size=(11100,11100)
        self.width = self.size[0]
        self.height = self.size[1]
        self.ph = Line(points=[30,self.height,30, self.height])
        self.space = 32
        self.start = 0
        self.amt = self.width / self.space
        print(self.amt)
        self.drag = False
        self.selected_item = None

        self.playhead_increment = 0
        self.items = []

        # self.playhead = PlayHead(800)
        # Color(1, 0, 0)
        # self.playhead = Line(points=[0, 900, 0, 0])
        # self.playhead.width = 3

        print(get_color_from_hex("#ff0000"))
        Clock.schedule_interval(self.move_playhead, 0.01)

        with self.canvas:
            draw_grid(self.amt,self.start,self.width,self.height, self.space)
            # Change playhead color
            Color(0.25, 0.95, 0.87, 1)

        self.canvas.add(self.ph)

    # temporarily moves playhead on screen
    def move_playhead(self, dt=0):
        self.playhead_increment+=30
        # print("seq_widget " + str(self.playhead_increment))

        # if playhead reaches end of window width, loop back to beginning
        # if self.playhead_increment > Window.size[0]:
        #     self.playhead_increment=0
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
            # self.playhead.moveX(self.playhead_increment)

    def on_touch_down(self, touch):
        super(SeqGridWidget, self).on_touch_down(touch)

        blk = Rectangle(pos=(touch.x - self.d / 2, touch.y - self.d / 2), size=(5, 5))
        print("stopped here")
        # this doubles up when scanning blocks, make sure to check this
        # be sure to edit to allow inviduals ops, color, size, text, fn
        # effects list
        
        self.block_list.append(blk)
        self.canvas.add(blk)

        print("*"*20)
        print("Block list count: ", len(self.block_list))
        for item in self.block_list:
            print("Block pos", item.pos)
            print("Block size", item.size)
        print("*"*20)
        # for item in self.block_list:
        #     self.canvas.add(item)
        # self.canvas.add(self.block_list)
        with self.canvas:
            # paint_stress_test(self.width, self.height)
            # draw small pink rect
            Color(1, 0, 1)
            Rectangle(pos=(touch.x - self.d / 2, touch.y - self.d / 2), size=(5, 5))

            # the test can of course be simplified: a.pos[0] < touch.x < a.pos[0] + a.size[0] and a.pos[1] < touch.y < a.pos[1] + a.size[1]
            # just put a = self.a on the line before
            for box in self.items:
                if touch.x >=box.pos[0] and touch.x <= box.pos[0]+box.size[0]*2 and touch.y >=box.pos[1] and touch.y <= box.pos[1]+box.size[1]*2:
                # if touch.x >= posX and touch.x <=
                    self.drag = True
                    self.selected_item = box
                    print("selected item",self.selected_item)
                    print("in bounds")

            if self.drag == False:
                Color(1, uniform(0,1), 0)
                box_size = 64
                self.a=Rectangle(pos=(touch.x - box_size / 2, touch.y - box_size / 2), size=(box_size, box_size))
                # add to item list
                self.items.append(self.a)

                # add shape/rect to canvas
                self.canvas.add(self.a)

                # Label connected to audio block
                b = Label(text="Sound clip")
                b.pos = (touch.x-45, touch.y)
                self.add_widget(b)

    def on_touch_up(self,touch):
        self.drag = False

    def on_touch_move(self, touch):
        if self.drag == True:
            self.selected_item.pos = (touch.x - self.selected_item.size[0]/2, touch.y-self.selected_item.size[1]/2)
            print("drag " + str(self.selected_item.pos))
        else:
            self.drag = False

       
class SeqGridWidgetApp(App):
    def build(self):
        return SeqGridWidget()


if __name__ == '__main__':
    SeqGridWidgetApp().run()