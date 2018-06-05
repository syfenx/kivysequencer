# import pyo as p
from pyo import *
import multiprocessing as mp
#s = Server(sr=44100, nchnls=2, buffersize=512, duplex=0).boot()
# s = Server(duplex=0)
# s.boot()
# s.start()
#

output = mp.Queue()

class AudioEngine(object):
    def __init__(self):
        # self.s = self.engine
        # self.start(
        self.sr = 44100
        self.nchnls = 2
        self.buffersize = 512
        self.duplex = 0
        # self.engine = Server(sr=self.sr, nchnls=self.nchnls, buffersize=self.buffersize, duplex=self.duplex)
        self.engine = Server(audio="jack")
        # self.engine.setInOutDevice(5)
        # self.m = Metro(.125)
    def start(self):
        self.engine.boot()
        # self.engine.setJackAuto(False, False) 
        self.engine.start()
        print("Engine started - Sample Rate: {sr} - Channels: {chan} - Buffer Size: {buf} - Duplex: {dup}".format(sr=self.sr,chan=self.nchnls,buf=self.buffersize,dup=self.duplex))
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

class AudioItem(object):
    def __init__(self, filename, volume, pan, vel):
        self.filename = filename
        self.volume = volume
        self.pan = pan
        self.fx = []
        self.vel = vel
        self.sf = SfPlayer(self.filename, mul=0.3).stop()
        self.sf2 = self.sf.mix(2).out()
    def play(self):
        self.sf.play()
        # print("played audioitem")
        # self.a = Trig()
        # self.env = HannTable()
        # self.tenv = TrigEnv(self.sf, table=self.env, dur=5, mul=.3)
        # self.tenv.out()
        # self.n = Noise(self.tenv).out()
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
    def __init__(self, filename, volume, pan, vel):
        self.filename = filename
        self.volume = volume
        self.pan = pan
        self.fx = []
        self.vel = vel
        self.sf = SfPlayer(self.filename, mul=0.3).stop()
        self.sf2 = self.sf.mix(2).out()
    def play(self):
        self.sf.play()
        # print("played audioitem")
        # self.a = Trig()
        # self.env = HannTable()
        # self.tenv = TrigEnv(self.sf, table=self.env, dur=5, mul=.3)
        # self.tenv.out()
        # self.n = Noise(self.tenv).out()
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
