class Info(object):
    # dummy class for stress test to work
    x = 0
    y = 0

def show_audio_items_stats(audio_items):
    print("*"*20)
    for item in audio_items:
        print("Block pos", item.shape.pos)
        print("Block size", item.shape.size)
    print("Audio item count: ", len(audio_items))
    print("*"*20)

# # piano roll attempts
#     self.start = 0
#     self.spc = 30
#     self.sizeH = 32
#     for x in range(200):
#         Color(1,1,1)
#         Rectangle(pos=[0,0 + self.start],size=[60,self.sizeH])
#         Color(0,0,0)
#         Rectangle(pos=[0,0 + self.start + 10],size=[40,self.sizeH])
#         self.start+=self.spc