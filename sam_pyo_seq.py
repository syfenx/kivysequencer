import kivy
kivy.require('1.10.0')  # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.splitter import Splitter
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.graphics import *
import random
from pyo import *

# s = Server(duplex=0)
# # scarlett device but may need pulseaudio -k to hear this
# # check for appropriate info in pa_list_devices()
# s.setInOutDevice(5)
# s.boot()
# s.start()
# # s.recordOptions(dur=10, filename="output_13.wav", fileformat=0, sampletype=1)
# # SAMPLE1
# snd_path1 = "sounds/kick1.wav"
# t1 = SndTable(snd_path1)
# # SAMPLE2
# snd_path2 = "sounds/snare2.wav"
# t2 = SndTable(snd_path2)
# # SAMPLE3
# snd_path3 = "sounds/hh2.wav"
# t3 = SndTable(snd_path3)

# # MASTER CLOCK
# m = Metro(.250).play()
# # PATTERN1
# tap = Iter(m.mix(1), choice=[1,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0])
# # PATTERN2
# tap2 = Iter(m.mix(1), choice=[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0])
# # PATTERN3
# tap3 = Iter(m.mix(1), choice=[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0])
# #PATTERN1
# trig = m * tap
# #PATTERN2
# trig2 = m * tap2
# #PATTERN3
# trig3 = m * tap3

# # Tracks 1 & 2 triggers
# track1 = TrigEnv(trig, table=t1, dur=.25, mul=.3)
# track2 = TrigEnv(trig2, table=t2, dur=.25, mul=.3)
# track3 = TrigEnv(trig3, table=t3, dur=.25, mul=.3)

# # MIXER
# mm = Mixer(outs=2, chnls=2, time=0.025)
# mm.addInput(voice=0, input=track1)
# mm.addInput(voice=1, input=track2)
# mm.addInput(voice=2, input=track3)
# mm.setAmp(vin=0, vout=1, amp=.8)
# mm.setAmp(vin=1, vout=1, amp=.8)
# mm.setAmp(vin=2, vout=1, amp=.8)

# # Master out
# mm.out()

# #MIXER OUTPUT FX
# # fx1 = Disto(mm[1], drive=1.90, slope=0.5, mul=.1).out()
# # fx2 = Freeverb(mm[1], size=5, damp=.9, bal=0.5, mul=.5).out()
# # lfo = Sine(freq=[.2,1.85], mul=.9, add=.9)
# # fx3 = Harmonizer(mm[1], transpo=lfo, feedback=.99, mul=.9).out()
# # fx4 = Delay(mm[1], delay=0.25, feedback=0.4, maxdelay=1, mul=1, add=0).out()
# # fx5 = FreqShift(mm[1], shift=lfo, mul=.9).out()
# pa_list_devices()
# s.gui(locals())

s = Server(sr=44100, duplex=0, audio='pa')
s.setInOutDevice(4)
s.boot()
s.start()

class MyAppRoot(FloatLayout):
    def __init__(self, **kwargs):
        self.octave = 5
        super(MyAppRoot, self).__init__(**kwargs)
       # self.server = Server(sr=44100, duplex=0, audio='jack').boot()
        # self.server.setInOutDevice(4)
        pa_list_devices()
        # self.server.start()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.MyButton = Button(text="btn1")
        self.MyButton2 = Button(text="btn2")
        self.lab = Label(text="thetext")
        self.layout = GridLayout(cols=2)
        self.splitter = Splitter()
        #self.splitter.min_size = 100
        #self.splitter.max_size = 250
        self.splitter.strip_size = '10pt'
        self.add_widget(self.layout)
        self.layout.add_widget(self.splitter)
        self.lab.bind(on_press=self.callback)
        #Window.bind(on_key_down=self.key_action)
        self.splitter.add_widget(self.MyButton)
        self.splitter.add_widget(self.MyButton2)
        # self.snd_path3 = "sounds/kick1.wav"
        #self.sf = SfPlayer('snare.wav', speed=[1, 0.995], loop=True, mul=0.4).out()

    def playsound(self, key, sample="sounds/cowbell2.wav"):
        # stereo playback with a slight shift between the two channels.
        if key == "a":
            speed = midiToTranspo(60.0 + self.octave)
            self.MyButton.text=key
        elif key == "w":
            speed = midiToTranspo(61.0 + self.octave)
        elif key == "r":
            speed = midiToTranspo(62.0 + self.octave)
        elif key == "f":
            speed = midiToTranspo(63.0 + self.octave)
        elif key == "s":
            speed = midiToTranspo(64.0 + self.octave)
        elif key == "t":
            speed = midiToTranspo(65.0 + self.octave)
        elif key == "g":
            speed = midiToTranspo(66.0 + self.octave)
        elif key == "d":
            speed = midiToTranspo(67.0 + self.octave)
        elif key == "j":
            speed = midiToTranspo(68.0 + self.octave)
        elif key == "h":
            speed = midiToTranspo(69.0 + self.octave)
        elif key == "l":
            speed = midiToTranspo(70.0 + self.octave)
        elif key == "n":
            speed = midiToTranspo(71.0 + self.octave)
        elif key == "e":
            speed = midiToTranspo(72.0 + self.octave)
        else:
            speed = midiToTranspo(60.0 + self.octave)
        self.sf = SfPlayer(sample, speed=[speed,speed], loop=False, mul=0.4).out()
        #self.sf.play()
        print('tried')

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.playsound(keycode[1])
        if keycode[1] == "z":
            self.octave -= 1
            print(60.0 + (self.octave * 10))
        if keycode[1] == "x":
            self.octave += 1
            print(60.0 + (self.octave * 10))
            return True

    def callback(self, instance):
        if instance.text == 'btn1':
            print('its btn1')
        if instance.text == 'arstsr':
            print('its label')
            self.lab.text = "it was clicked"


# def key_action(self, *args):
# k_modifier = list(args)[4]
# kb = list(args)[3]
# print("key:{} mod: {}".format(kb, k_modifier))
# if kb == "a":
# self.playsound()
class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        return MyAppRoot()

if __name__ == '__main__':
    MyApp().run()
