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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from pyo import *

from kivy.animation import Animation
import multiprocessing
import time
from random import randint
from aengine_thread import AudioItem
from helper_functions import Info, show_audio_items_stats
# from file_save_loader import write_project_file, read_project_file
from kivy.properties import NumericProperty
stress_test = False
import theme
# from kivy_sequencer import TimingBar
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


class Seq2(object):
    # for each tick check if audio item, check each audio item stats such as
    # velocity / note etc
    def __init__(self, ai):
        self.bpm = 120
        self.ai = ai
        self.tick = 0
        self.tickclock = 0
    def get_bpm_time(self):
        return self.bpm *0.0001
    def tickframe(self, ai, grid, playhead):
        self.tick+=0.125
        # self.tick+=self.bpm*0.001

        # print("bpm to dec", 125*0.0001)
        print("tick: ", self.tick)
        # for i in self.ai:
        #     i.play
        # self.ai[self.tick].play()
        # for item in App.get_running_app().root.sgr.audio_items:
        #     print(item.filename)
        # timingbar.ids.step.text
        # App.get_running_app().root.timingbar.step.text="s"

        fsec = self.tick/44100
        curr_min = fsec/60
        curr_msec = (fsec*1000)%1000
        curr_sec = fsec%60

        # print("{:.2f}:{:.2f}:{:.2f}".format(curr_min, curr_sec, curr_msec))
        tick = self.tick
        ticks_per_beat = grid.ticks_per_beat
        beats_per_bar = grid.beats_per_bar
        curr_bar = int(tick/(ticks_per_beat*beats_per_bar));
        curr_beat = int(tick/ticks_per_beat)%ticks_per_beat;
        curr_step = float(tick - int(tick)/ticks_per_beat*ticks_per_beat);

        # print("bar: {}, beat: {}, step: {}".format(curr_bar, curr_beat, curr_step))


        # tick = tick
        # self.ticks_per_beat
        hours = int(tick / 3600)
        mins = int((tick % 3600) / 60)
        secs = int(tick % 60)
        millis = int((tick * 1000) % 1000)

        # MIN / SEC / MSEC
        App.get_running_app().root.timingbar.ids.min.text=str(mins)
        App.get_running_app().root.timingbar.ids.sec.text=str(secs)
        App.get_running_app().root.timingbar.ids.msec.text=str(millis)
        # BAR / BEAT / STEP
        App.get_running_app().root.timingbar.ids.bar.text=str(curr_bar)
        App.get_running_app().root.timingbar.ids.beat.text=str(curr_beat)
        App.get_running_app().root.timingbar.ids.step.text=str(curr_step)

        #     print(self.lfo.get())
        # print(playhead.ph.pos[0])
        for item in ai:
            # print("tickframe item", item.shape.pos)
            if playhead.ph.points[0] == item.shape.pos[0]:
                # print("HIT A BLOCK")
                item.play()

class Side_Panel(FloatLayout):
    def __init__(self, **kwargs):
        super(Side_Panel, self).__init__(**kwargs)
        # anim = Animation(x=300, y=0, t='in_quad', duration=0.2)
        # anim.start(self)
    def on_touch_down(self, touch):
        pass
        # if self.pos[0] == -300:
        #     anim = Animation(x=0, y=0, t='in_quad', duration=0.2)
        #     anim.start(self)
        # else:
        #     anim = Animation(x=-300, y=0, t='in_quad', duration=0.2)
        #     anim.start(self)
        # for i in range(1,25):
        #     self.add_widget(Label(text="{}".format(i)))

class Selection_Box(object):
    def __init__(self, x, y, w, h):
        self.start = [0,0]
        self.r = Rectangle(pos=[x,y], size=[w,h])

class PlayHead(Widget):
    def __init__(self, height, start_location):
        #TODO playhead snapping to grid
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
            self.playhead_increment = touch.x
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

        # if self.playhead_increment > Window.size[0]:
        #     self.playhead_increment=0
        # repeat playhead for 16 beats
        if self.playhead_increment > (16*32)-1:
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

class GridLines(Widget):
    def __init__(self, width, **kwargs):
        # grid
        super(GridLines, self).__init__(**kwargs)
        self.width = width
        self.space = 32
        self.start = 0
        self.amt = (self.width / self.space) 
        self.main_lines = []
        self.beats_per_bar = 16
        self.ticks_per_beat = 8
        # self.instGroup = InstructionGroup()

        with self.canvas:
            Color(1,0,0,1)
            Rectangle(pos=(400,400),size=(10000,10000))
    def draw_grid(self, amt, start, width, height, space, audio_items, canvas):
        # the lines are drawn incorrectly, the horiz lines get drawn on top of
        # vertical lines

        # self.main_lines.clear()
        # lines that are added to main_lines could be put in
        # an InstructionGroup and edited later for line spacing

        # Draw horizontal lines on the bottom first
        self.main_lines.clear()
        startax = start
        for ax in range(int(amt)):
            Color(*theme.grid_line_tick_color)
            # Color(1,0,0,1)
            # horizontal line
            L = Line(points=[0, startax, width, startax])
            self.main_lines.append(L)
            startax+=space

        # Draw vertical lines on top of horizontal lines
        for x in range(int(amt)):
            if x % self.beats_per_bar == 0:
                # vertical line - thick width
                # Color(.2,.2,.2)
                Color(*theme.grid_bar_color)
                L = Line(points=[start*2, height, start*2, 0])
                L.width = 2.5
                self.main_lines.append(L)
            elif x % self.ticks_per_beat == 0:
                # vertical line - thick width
                Color(*theme.grid_bar_sep_color)
                L = Line(points=[start*2, height, start*2, 0])
                L.width = 2
                self.main_lines.append(L)
            else:
                Color(*theme.grid_line_tick_color)
                # vertical line - normal width
                L = Line(points=[start*2, height, start*2, 0])
                self.main_lines.append(L)
            start+=space
        
        print("mainlines len: ", len(self.main_lines))


        # this will redraw audio_items so they are not lost when redrawing grid
        for item in audio_items:
            Color(*item.color)
            canvas.add(item.shape)


    def get_grid_spacing(self):
        return self.space
    def set_grid_spacing(self, spacing):
        self.space = spacing
    def set_beats_per_bar(self, beats):
        with self.canvas:
            self.beats_per_bar = beats
            self.draw_grid(self.amt, 0, self.width, self.height, self.space, App.get_running_app().root.sgr.audio_items, self.canvas)
    def set_ticks_per_beat(self, ticks):
        self.ticks_per_beat = ticks

class SeqGridWidget(Widget):
    def __init__(self, **kwargs):
        super(SeqGridWidget, self).__init__(**kwargs)

        # handle keypresses
        Window.bind(on_key_down=self.key_action_down)
        Window.bind(on_key_up=self.key_action_up)

        # Change main widget background color
        Window.clearcolor=get_color_from_hex("#3c3c3c")

        # self.write_project_file = write_project_file
        # main widget
        self.audio_items = []
        self.size_hint=(None,None)
        self.size=(11000,11000)
        self.width = self.size[0]
        self.height = self.size[1]


        self.seq = Seq2(self.audio_items)
        # self.side_panel = Side_Panel()
        # self.add_widget(self.side_panel)

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
        self.old_shapes=[]
        self.oldpos = (0,0)
        # self.tf = TrigFunc(self.ae.m, partial(self.seq.tickframe, self.audio_items,self.grid,self.playhead))
        with self.canvas:
            self.grid.draw_grid(self.grid.amt,self.grid.start,self.width,self.height, self.grid.space, self.audio_items, self.canvas)


            # Change playhead color to pink
            Color(0.96, 0.52, 0.74)
        self.canvas.add(self.playhead.ph)

        with self.canvas:
            # top grey horizontal bar
            # controls playhead skipping / looping markers
            Color(*theme.playhead_bar_top)
            Rectangle(pos=(0,self.height-20), size=(self.width, 20))


        # Clock.schedule_interval(lambda dt: self.playhead.move_playhead(), 0.001)
        # Clock.schedule_interval(partial(self.playhead.move_playhead, self.grid.get_grid_spacing()), 0.250)
        bpm = 90
        seconds_in_tick = 1.0/(bpm/60.0*self.grid.ticks_per_beat)
        print("seconds_in_tick", seconds_in_tick)
        frames_per_pixel = seconds_in_tick*44100/self.grid.space
        print("seconds_in_tick", seconds_in_tick)
        t = self.seq.get_bpm_time()
        # time = 0.0125
        # time = 0.0125

        # MOVE THE PLAYHEAD AT EACH BEAT SIZE and change the 32 value based on grid zoom
        Clock.schedule_interval(partial(self.playhead.move_playhead, 8), seconds_in_tick)
        # Clock.schedule_interval(partial(self.playhead.move_playhead, 1), t)
        # print(seconds_in_tick)

        # Clock.schedule_interval(lambda dt: self.seq.tickframe(self.audio_items, self.grid), t)
        Clock.schedule_interval(lambda dt: self.seq.tickframe(self.audio_items, self.grid, self.playhead), seconds_in_tick)
        # Clock.schedule_interval(partial(self.seq.tickframe(), self.audio_items), 0.250)


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

            # self.grid.space*2 is so the snap works with the wider item size
            if touch.x > lineX and touch.x <= lineX + self.grid.space*2:
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

            sbX = self.sb.r.pos[0]
            sbY = self.sb.r.pos[1]

            sbW = self.sb.r.size[0]
            sbH = self.sb.r.size[1]

            # if x >= self.sb.r.pos[0] and x <= self.sb.r.pos[0]+self.sb.r.size[0] and \
            # y >= self.sb.r.pos[1] and y <= self.sb.r.pos[1]+self.sb.r.size[1]:
            if x >= sbX and x <= sbX + sbW and y <= sbY and y >= sbY + sbH:
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


        self.oldpos = touch.x, touch.y
        print("oldpos",self.oldpos)

        # add a copy of the old list of item locations
        # self.old_shapes.append(self.sel_items)
        self.old_shapes.clear()
        for item in self.sel_items:
            self.old_shapes.append(item)

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
                    app = App.get_running_app()
                    # if self.current_sound is not None:
                    ai = AudioItem(self.current_sound, 100, 100, 100, [touch.x - (box_size*2)/2, touch.y - box_size/2], [box_size*2, box_size])
                    # else:
                        # ai = AudioItem('sounds/snare1.wav', 100, 100, 100, [touch.x - box_size/2, touch.y - box_size/2], [box_size*2, box_size])
                    # add to audio_item list
                    self.audio_items.append(ai)
                    self.check_snap_to_grid(ai, touch)

                    # app = App.get_running_app()
                    # print(self.text)
                    # selectedsound = self.text
                    # print("sel", selectedsound)
                    # path = "sounds/" + selectedsound
                    # app.root.ae.playsound(path)

                    # print("Selected sound is: ", BASE_DIR + selectedsound)
                    # app.root.sgr.current_sound = BASE_DIR + selectedsound
            # debugging info / stress test
            show_audio_items_stats(self.audio_items)
            if stress_test:
                self.paint_stress_test(self.width, self.height)

    def on_touch_up(self, touch):
        self.drag = False

        # gather all items in selection rectangle, add to self.sel_items
        # self.sel_rect_check()

        # change selection box to false but keep selection in self.sel_items
        #self.sel_status = False
        if self.sb.r in self.canvas.children:
            self.canvas.remove(self.sb.r)

    
    def on_touch_move(self, touch):
        # if ctrl is held down, allow a selection box
        if self.sel_status:
            self.sel_rect_check()

        # self.old_shapes.clear()
            for c, item in enumerate(self.old_shapes):
            # self.old_shapes.append(item)
            # xOld, yOld = item.shape.pos[0]+touch.x, item.shape.pos[1]+touch.y
            # idx = self.old_shapes.index(item)
            # item.shape.pos = randint(touch.x,touch.x+20) + touch.x, touch.y
                posX, posY = item.shape.pos[0], item.shape.pos[1]
                # item.shape.pos = self.oldpos[0] + touch.x, self.oldpos[1] + touch.y
                item.shape.pos = (touch.x - posX) + self.oldpos[0], (touch.y - posY) + self.oldpos[1]
            print("Shape: x:{} y:{} | Touch: x:{} y:{}".format(posX, posY, touch.x, touch.y))

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

    def key_action_up(self, *args):
        print("key event up: {}".format(list(args)))
        if args[1] == 305:
            print("ctrl")
            self.sel_status = False
    space = 0
    def key_action_down(self, *args):
        # monitor keypresses
        key = args[3]
        print("key event down: {}".format(list(args)))
        if args[1] == 305:
            print("ctrl")
            self.sel_status = True

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
            self.grid.beats_per_bar+=4
            with self.canvas:
                self.canvas.clear()
                # update instruction group with lines then draw to canvas
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                self.grid.set_beats_per_bar(self.grid.beats_per_bar)
            # self.space+=1
        if key == '-':
            self.grid.beats_per_bar-=4
            with self.canvas:
                self.canvas.clear()
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                self.grid.set_beats_per_bar(self.grid.beats_per_bar)
                # self.space+=1
            # self.grid.set_grid_spacing(self.space)
            # self.space-=1
        if key == '0':
            with self.canvas:
                self.grid.ticks_per_beat+=1
                # self.grid.beats_per_bar+=self.grid.ticks_per_beat
                self.canvas.clear()
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                self.grid.set_ticks_per_beat(self.grid.ticks_per_beat)
                # self.grid.set_beats_per_bar(self.grid.beats_per_bar)
                print("0 was pressed")
        if key == '9':
            with self.canvas:
                self.grid.ticks_per_beat-=1
                # self.grid.beats_per_bar-=self.grid.ticks_per_beat
                self.canvas.clear()
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                self.grid.set_ticks_per_beat(self.grid.ticks_per_beat)
                # self.grid.set_beats_per_bar(self.grid.beats_per_bar)
                print("9 was pressed")
        if key == '7':
            with self.canvas:
                self.grid.space-=1
                # self.grid.beats_per_bar+=self.grid.ticks_per_beat
                self.canvas.clear()
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                # self.grid.set_ticks_per_beat(self.grid.ticks_per_beat)
                # self.grid.set_beats_per_bar(self.grid.beats_per_bar)
                print("0 was pressed")
        if key == '8':
            with self.canvas:
                self.grid.space+=1
                # self.grid.beats_per_bar-=self.grid.ticks_per_beat
                self.canvas.clear()
                self.grid.draw_grid(self.grid.amt, 0, self.width, self.height, self.grid.space, self.audio_items, self.canvas)
                # self.grid.set_ticks_per_beat(self.grid.ticks_per_beat)
                # self.grid.set_beats_per_bar(self.grid.beats_per_bar)
                print("9 was pressed")

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

# class MyKeyboardListener(Widget):

#     def __init__(self, **kwargs):
#         super(MyKeyboardListener, self).__init__(**kwargs)
#         self._keyboard = Window.request_keyboard(
#             self._keyboard_closed, self, 'text')
#         if self._keyboard.widget:
#             # If it exists, this widget is a VKeyboard object which you can use
#             # to change the keyboard layout.
#             pass
#         self._keyboard.bind(on_key_down=self._on_keyboard_down)

#     def _keyboard_closed(self):
#         print('My keyboard have been closed!')
#         self._keyboard.unbind(on_key_down=self._on_keyboard_down)
#         self._keyboard = None

#     def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#         print('The key', keycode, 'have been pressed')
#         print(' - text is %r' % text)
#         print(' - modifiers are %r' % modifiers)

#         # Keycode is composed of an integer + a string
#         # If we hit escape, release the keyboard
#         if keycode[1] == 'escape':
#             keyboard.release()

#         # Return True to accept the key. Otherwise, it will be used by
#         # the system.
#         return True


class SeqGridWidgetApp(App):
    def build(self):
        return SeqGridWidget()

    def on_stop(self):
        print("app was stopped here")
        # write_project_file(self.audio_)


if __name__ == '__main__':
    SeqGridWidgetApp().run()