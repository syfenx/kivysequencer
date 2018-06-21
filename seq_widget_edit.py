from kivy.config import Config
# disables red dots on right click
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

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
from helper_functions import Info, show_audio_items_stats
# from file_save_loader import write_project_file, read_project_file
from kivy.properties import NumericProperty
stress_test = False

#TODO: select sound from sound palette
#TODO: loop bar dragging
#TODO: snap to grid lines - done
#TODO: play sounds from thread
#TODO: audio mixer
#TODO: effects
#TODO: synth sounds
#TODO: waveform view
#TODO: zoom gridlines
#TODO: alt for sound pallette left slide out for sound selection
#TODO: mouse - paint or single add block for both add/delete
#TODO: check for filetype when loading a project, error handle this
#TODO: grid zooming, pattern / song mode
#TODO: piano roll with velocity


class Selection_Box(object):
    def __init__(self, x, y, w, h):
        self.start = [0,0]
        self.r = Rectangle(pos=[x,y], size=[w,h])

class PlayHead(Widget):
    def __init__(self, height, start_location):
        # self.playhead_line = Line(points=[location, self.height, location, 0])
        # self.playhead_line.width = 6
        # Playhead
        b = NumericProperty(0)
        self.height = height
        self.ph = Line(points=[start_location, self.height, start_location, self.height])
        self.ph.width = 6
        self.inc = 0
        self.playhead_increment = 0
        self.isPlayheadAdjust = False

    def adjust_playhead(self, touch, grid):
        if touch.y > (self.height-20):
            self.isPlayheadAdjust = True
            self.playhead_increment = touch.x - grid.space * 2
            p = [touch.x, self.height, touch.x, 0]
            # with self.canvas:
            self.ph.points = p
        else:
            self.isPlayheadAdjust = False

    # temporarily moves playhead on screen
    def move_playhead(self, space_amount, dt):
        """
        moves playhead at x spacing amount
        """
        self.playhead_increment += space_amount

        # if playhead reaches end of window width, loop back to beginning
        # if self.playhead_increment > Window.size[0]:
        #     self.playhead_increment=0
        # self.size is for testing inside the widget, Window.size[0]
        # is normal use

        if self.playhead_increment > Window.size[0]:
            self.playhead_increment=0
        
        p = [self.playhead_increment, self.height, self.playhead_increment, 0]
        self.ph.width = 2
        self.ph.points = p

class LoopBars(object):
    def __init__(self, width, height, canvas):
        self.width = width
        self.height = height
        self.start = 0

        self.canvas = canvas

        self.loop = False
        self.loops = InstructionGroup()

    def loop_func(self, loop):
        if loop:
                loopL = Line(points=[30+20,self.height,30+20,0])
                loopR = Line(points=[30+70,self.height,30+70,0])
                handle_size=(20,20)
                top_padding = 20
                loopHandleL = Rectangle(pos=(loopL.points[0]-(handle_size[0]/2),self.height-top_padding), size=handle_size)
                loopHandleR = Rectangle(pos=(loopR.points[0]-(handle_size[0]/2),self.height-top_padding), size=handle_size)
                self.loops.add(Color(0,1,1))
                self.loops.add(loopL)
                self.loops.add(Color(1,0,1))
                self.loops.add(loopR)
                self.loops.add(loopHandleL)
                self.loops.add(loopHandleR)
                self.canvas.add(self.loops)
        else:
            self.canvas.remove(self.loops)
            self.loops.clear() 

    def drag_loop_bar(self, loop):
        # only move loop line if dragged by handle
        pass

class GridLines(object):
    def __init__(self, width):
        # grid
        self.width = width
        self.space = 32
        self.start = 0
        self.amt = (self.width / self.space) 
        self.main_lines = []

        self.instGroup = InstructionGroup()

    def draw_grid(self, amt, start, width, height, space):
        self.main_lines.clear()
        Color(1, 1, 1)
        # lines that are added to main_lines could be put in
        # an InstructionGroup and edited later for line spacing
        for x in range(int(amt)):
            if x % 4 == 0:
                # every 4th line is darker
                # vertical line - thick width
                Color(.2,.2,.2)
                L = Line(points=[0+start, height, 0+start, 0])
                L.width = 2
                self.main_lines.append(L)
            else:
                Color(.2,.2,.2)
                # vertical line - normal width
                L = Line(points=[0+start, height, 0+start, 0])
                self.main_lines.append(L)
            start+=space

            Color(.2,.2,.2)
            # horizontal line
            L = Line(points=[0, start, width, start])
            self.main_lines.append(L)
    def get_grid_spacing(self):
        return self.space
    def set_grid_spacing(self, spacing):
        self.space = spacing

class SeqGridWidget(Widget):
    def __init__(self, **kwargs):
        super(SeqGridWidget, self).__init__(**kwargs)

        # handle keypresses
        Window.bind(on_key_down=self.key_action)

        # Change main widget background color
        Window.clearcolor=get_color_from_hex("#444444")


        # self.write_project_file = write_project_file
        # main widget
        self.audio_items = []
        self.size_hint=(None,None)
        self.size=(11100,11100)
        self.width = self.size[0]
        self.height = self.size[1]


        self.drag = False
        self.selected_item = None

        # Playhead
        self.playhead = PlayHead(self.height, 230)
        # self.ph = Line(points=[30,self.height,30, self.height])
        # self.ph.width = 6
        # self.inc = 0
        # self.playhead_increment = 0
        # self.isPlayheadAdjust = False

        # loop bars
        self.loop_bars = LoopBars(self.width, self.height, self.canvas)

        # selection box
        self.sb = Selection_Box(0,0,50,50)

        # sel_items contains the current selected item group
        # (a list of audio_items)
        self.sel_items = []
        self.sel_status = False
        self.grid = GridLines(self.width)

        # current sound selected in left hand browser
        self.current_sound = ""

        with self.canvas:
            self.grid.draw_grid(self.grid.amt,self.grid.start,self.width,self.height, self.grid.space)

            # Change playhead color to pink
            Color(0.96, 0.52, 0.74)
        self.canvas.add(self.playhead.ph)

        with self.canvas:
            # top grey horizontal bar
            # controls playhead skipping / looping markers
            Color(0.43, 0.43, 0.43, 1)
            Rectangle(pos=(0,self.height-20), size=(self.width, 20))


        # Clock.schedule_interval(lambda dt: self.playhead.move_playhead(), 0.001)
        Clock.schedule_interval(partial(self.playhead.move_playhead, self.grid.get_grid_spacing()), 0.250)




    def check_click(self, touch, box, button_type):
        # checks that we're in bounds when a button/rect is pressed
        # check for right or left buttons
        res = touch.x >=box.shape.pos[0] and touch.x <= box.shape.pos[0]+box.shape.size[0] \
        and touch.y >=box.shape.pos[1] and touch.y <= box.shape.pos[1]+box.shape.size[1] and \
        touch.button == button_type
        return res

    def delete_audio_item(self, touch, box, button):
        if self.check_click(touch, box, button):
            print("{} click".format(button))
            self.selected_item = box
            idx = self.audio_items.index(self.selected_item)
            self.remove_widget(self.audio_items[idx])
            # remove audio item (shape)
            self.canvas.remove(self.audio_items[idx].shape)
            # remove audio item
            self.audio_items.remove(self.audio_items[idx])


    def check_snap_to_grid(self, item, touch):
        for line in self.grid.main_lines:
            lineX = line.points[0]
            lineY = line.points[1]
            selShapeX = item.shape.pos[0]
            selShapeY = item.shape.pos[1]

            if touch.x > lineX and touch.x <= lineX + self.grid.space:
                item.shape.pos = [lineX, selShapeY]
                # set_pos updates the actual shape coords so we can
                # see it when saving the file
                item.set_pos(lineX, selShapeY)

            if touch.y > lineY and touch.y <= lineY + self.grid.space:
                item.shape.pos = [selShapeX, lineY]
                # set_pos updates the actual shape coords so we can
                # see it when saving the file
                item.set_pos(selShapeX, lineY)

    def sel_rect_check(self):
        self.sel_items.clear()
        for item in self.audio_items:
            # print(item.shape)
            x = item.shape.pos[0]
            y = item.shape.pos[1]
            if x > self.sb.r.pos[0] and x <= self.sb.r.pos[0]+self.sb.r.size[0]:
                print("shape within selection bounds", item)
                # clear list to remove selection unless shift is down etc
                # self.sel_items.clear()
                self.sel_items.append(item)

        print(self.sel_items)

    def on_touch_down(self, touch):
        super(SeqGridWidget, self).on_touch_down(touch)
        if touch.button == 'left':
            print("startvalue", self.sb.start)
            self.sb.start = touch.x, touch.y
            print(self.sb.start)

        # if ctrl is down
        if self.sel_status == True:
            # if rect not in canvas
            if self.sb.r not in self.canvas.children:
                c = get_color_from_hex("#5745f722")
                self.sb.r.pos = [touch.x, 0]
                # add color, add shape of rect
                self.canvas.add(Color(*c))
                self.canvas.add(self.sb.r)

        # enables dragging of playhead
        self.playhead.adjust_playhead(touch, self.grid)

        # if playhead is being moved, don't place a block/rect
        if self.playhead.isPlayheadAdjust == False:
            for box in self.audio_items:
                # delete item if right clicked on
                self.delete_audio_item(touch, box, 'right')

                if self.check_click(touch, box, 'left'):
                    self.drag = True
                    self.selected_item = box
                    print("selected item (in bounds, left click)",self.selected_item)

            # if not dragging and not right button, add new audio item
            if self.drag == False and touch.button != 'right' and self.sel_status == False:
                with self.canvas:
                    box_size = self.grid.space
                    ai = AudioItem(self.current_sound, 100, 100, 100, [touch.x - box_size/2, touch.y - box_size/2], [box_size, box_size])
                    # add to audio_item list
                    self.audio_items.append(ai)
                    self.check_snap_to_grid(ai, touch)

            # debugging info / stress test
            show_audio_items_stats(self.audio_items)
            if stress_test:
                self.paint_stress_test(self.width, self.height)

    def on_touch_up(self, touch):
        self.drag = False

        # gather all items in selection rectangle, add to self.sel_items
        self.sel_rect_check()

        # change selection box to false but keep selection in self.sel_items
        self.sel_status = False
        if self.sb.r in self.canvas.children:
            self.canvas.remove(self.sb.r)

    def on_touch_move(self, touch):
        # if right click is held down and dragged, delete items
        for box in self.audio_items:
            self.delete_audio_item(touch, box, 'right')

        # create selection box
        if self.sel_status == True:
            x, y = self.sb.start[0], self.sb.start[1]
            self.sb.r.pos = [x,y]
            self.sb.r.size = [touch.x-x,touch.y-y]

        # enables mouse to grab playhead to move it
        self.playhead.adjust_playhead(touch, self.grid)

        if self.drag == True:
            # drag selected item while snapping to grid
            self.selected_item.shape.pos = (touch.x - self.selected_item.shape.size[0]/2, touch.y-self.selected_item.shape.size[1]/2)
            #print("drag " + str(self.selected_item.shape.pos))
            self.check_snap_to_grid(self.selected_item, touch)
        else:
            self.drag = False

    space = 0
    def key_action(self, *args):
        # monitor keypresses
        key = args[3]
        print("key event: {}".format(list(args)))
        if args[1] == 305:
            print("ctrl")
            self.sel_status = True
        else:
            self.sel_status = False

        # if [s] is pressed, save the project file
        if key == 's':
            # write_project_file(self.audio_items, 'proj.xml')
            # print("Project saved...")
            print("disabled shortcut")
        if key == 'q':
            # read_project_file(self.audio_items, 'lol-project.xml', self.canvas)
            # print("Project loaded...")
            print("disabled shortcut")


        if key == '=':
            print("increase grid")
            with self.canvas:
                self.canvas.clear()
                # update instruction group with lines then draw to canvas
                self.grid.draw_grid(100, 0, self.width, self.height, self.space)
                print("self.size[0] is: ", self.size[0])
            self.grid.set_grid_spacing(self.space)
            self.space+=1
        if key == '-':
            with self.canvas:
                self.canvas.clear()
                self.grid.draw_grid(100, 0, self.width, self.height, self.space)
            self.grid.set_grid_spacing(self.space)
            self.space-=1

    def draw_grid(self, amt, start, width, height, space):
            print("decrease grid")
            # Rectangle(pos=[30,30], size=[400,400])
    
    def paint_stress_test(self, width, height):
        # stress test with snapping blocks
        info = Info()
        with self.canvas:
            for x in range(2000):
                rw, rh = randint(0, width), randint(0, height)
                info.x, info.y = rw, rh
                print(info.x, info.y)
                box_size = self.grid.space
                ai = AudioItem("sounds/snare1.wav", 100, 100, 100, [rw - box_size/2, rh - box_size/2], [box_size, box_size])
                # add to audio_item list
                self.audio_items.append(ai)
                self.check_snap_to_grid(ai, info)
       
class SeqGridWidgetApp(App):
    def build(self):
        return SeqGridWidget()

    def on_stop(self):
        print("app was stopped here")
        # write_project_file(self.audio_)


if __name__ == '__main__':
    SeqGridWidgetApp().run()