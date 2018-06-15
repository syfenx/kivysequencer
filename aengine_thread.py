from pyo import *
import multiprocessing
import random
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from random import uniform

# class AudioEngine(object):
class AudioEngine(multiprocessing.Process):
    def __init__(self, pitch=5):
        # self.s = self.engine
        # self.start(
        super(AudioEngine, self).__init__()
        self.daemon = True
        self.sr = 44100
        self.nchnls = 2
        self.buffersize = 512
        self.duplex = 0
        self.pitch = pitch
        # self.engine = Server(sr=self.sr, nchnls=self.nchnls, buffersize=self.buffersize, duplex=self.duplex)
        #jack_control stop - don't
        #jackd -d alsa -d hw:USB -P -p 1024 -r 44100 - don't
        #in qjackctl start jack - yes, wait for system outputs to show
        # open sequencer

        # self.engine.setInOutDevice(5)
        # self.m = Metro(.125)
    # def start(self):
    #     self.engine.boot()
    #     # self.engine.setJackAuto(False, False) 
    #     self.engine.start()
    #     print("Engine started - Sample Rate: {sr} - Channels: {chan} - Buffer Size: {buf} - Duplex: {dup}".format(sr=self.sr,chan=self.nchnls,buf=self.buffersize,dup=self.duplex))
    def run(self):
        self.server = Server(audio="jack")
        self.server.deactivateMidi()
        self.server.boot().start()
        
        # 200 randomized band-limited square wave oscillators.
        self.amp = Fader(fadein=5, mul=0.01).play()
        lo, hi = midiToHz((self.pitch - 0.1, self.pitch + 0.1))
        self.fr = Randi(lo, hi, [random.uniform(.2, .4) for i in range(200)])
        self.sh = Randi(0.1, 0.9, [random.uniform(.2, .4) for i in range(200)])
        # self.osc = LFO(self.fr, sharp=self.sh, type=2, mul=self.amp).out()

        # self.sf = SfPlayer("sounds/snare1.wav", mul=0.3).mix(2).out()
        self.sf = SfPlayer("sounds/snare1.wav", mul=0.3).stop()
        self.sf2 = self.sf.mix(2).out()

        for x in range(5):
            self.sf.play()
            # self.sf.play()
            # SfPlayer("sounds/snare1.wav", mul=0.3).mix(2).out()
            time.sleep(0.1)
        # time.sleep(30) # Play for 30 seconds.
        # self.server.stop()

    def record(self):
        self.engine.recordOptions(dur=100, filename="output_13.wav", fileformat=0, sampletype=1)
        self.engine.recstart()
    def get_outputs(self):
        outs = pa_get_output_devices()
        return outs
    def set_output(self, device_number):
        self.engine.setInOutDevice(int(device_number))
        self.sf = SfPlayer("sounds/kick1.wav", mul=0.3).mix(2).out()

    def start_metro(self):
        self.m.play()

    def stop_metro(self):
        self.m.stop()

    # def playsound(self, filename):
    #     self.sf = SfPlayer(filename, mul=0.3)
    #     self.sf.mix(2).out()
    #     print("soundplayed")
    def playsound(self, filename):
        self.sf = SfPlayer(filename, mul=0.3).mix(2).out()
        # self.sf = self.sf.mix(2).out()
        print("soundplayed")

class AudioItem(Widget):
    def __init__(self, filename, volume, pan, velocity, pos, size):
        print("init audioitem")
        super(AudioItem, self).__init__()
        self.filename = filename
        self.volume = volume
        self.pan = pan
        self.effects = []
        self.velocity = velocity
        self.pos = pos
        self.size = size
        print("sound might fail here because aengine doesn't have server booted")
        # self.sf = SfPlayer(self.filename, mul=0.3).stop()
        # self.sf2 = self.sf.mix(2).out()

        Color(0.4, uniform(0.3,1), uniform(0.3,1))
        # Color(0.4, 0.52, 0.74)
        # print(p.rgb)
        # self.size = (50,40)
        self.shape = Rectangle(pos=self.pos, size=self.size)
        # self.text = Label(text="{}".format(filename[7:]))
        # self.add_widget(Label(text="testlabel"))
        # self.text.pos = (self.shape.pos[0], self.shape.pos[1])
    def play(self):
        self.sf.play()
    def setfn(self, path):
        self.sf.setPath(path)

class AudioMixer(object):
    def __init__(self):
        print("mixer started")
        self.tracks = []

    def addTrack(self, fn):
        self.fn = fn 
        self.tracks.append(AudioItem(self.fn, 0, 0, 0))
        print("added {} to mixer, total tracks = {}".format(self.fn, len(self.tracks)))



if __name__ == '__main__':
    p1 = AudioEngine(48) 
    p1.start()
    p1.join()

    # time.sleep(5)
    # p1.playsound("sounds/kick1.wav")
    # time.sleep(5)
    # p2.playsound("sounds/kick1.wav")
    # time.sleep(5)
    # p3.playsound("sounds/kick1.wav")