
        #######################################################
        # MIXER TESTING
        #######################################################
        # self.a = SfPlayer("sounds/kick2.wav", loop=False, mul=.3)
        # self.b = SfPlayer("sounds/snare1.wav", loop=False, mul=.1)

        # SAMPLE1
        self.snd_path1 = "sounds/kick2.wav"
        self.t1 = SndTable(self.snd_path1)
        # SAMPLE2
        self.snd_path2 = "sounds/snare2.wav"
        self.t2 = SndTable(self.snd_path2)

        # MIXER
        self.mm = Mixer(outs=100, chnls=2, time=0.1)

        #MIXER OUTPUT FX
        self.fx1 = Disto(self.mm[0], drive=.9, slope=.9, mul=.1).out()
        self.fx2 = Freeverb(self.mm[1], size=1, damp=.7, bal=0.5, mul=.5).out()
        self.fx3 = Harmonizer(self.mm[2], transpo=1, feedback=.75, mul=.5).out()

        # MASTER CLOCK
        self.m = Metro(.125).play()
        # PATTERN1
        self.tap = Iter(self.m.mix(1), choice=[1,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0])
        # PATTERN2
        self.tap2 = Iter(self.m.mix(1), choice=[1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0])

        #PATTERN1
        self.trig = self.m * self.tap
        #PATTERN2
        self.trig2 = self.m * self.tap2

        # env = CosTable([(0,0),(100,1),(1000,.3),(8192,0)])
        # Tracks 1 & 2 triggers
        self.track1 = TrigEnv(self.trig, table=self.t1, dur=.25, mul=.3)
        self.track2 = TrigEnv(self.trig2, table=self.t2, dur=.25, mul=.3)

        # Add Tracks 1 & 2 to mixer
        self.mm.addInput(voice=0, input=self.track1)
        self.mm.addInput(voice=1, input=self.track2)
        # Set Tracks 1 & 2 volume
        self.mm.setAmp(vin=0, vout=1, amp=.8)
        self.mm.setAmp(vin=1, vout=1, amp=.8)
        # Master out
        self.mm.out()

        s.recstart()

        # amp = TrigEnv(self.trig, table=env, dur=.2, mul=.3).out()
        # self.mm.out()
        print(self.mm.getChannels())
        # self.mm.play()
        #######################################################
        # MIXER TESTING
        #######################################################
