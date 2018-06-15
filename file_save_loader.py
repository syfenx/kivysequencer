from xml.dom import minidom
import xml.etree.ElementTree as ET

from aengine_thread import AudioItem

ai = AudioItem("sounds/snare1.wav", 100, 100, 100, [20,20], [32, 32])

sample_audio_items = []
sample_audio_items.append(ai)
sample_audio_items.append(ai)
sample_audio_items.append(ai)

print(sample_audio_items)

def read_project_file(filename):
    tree = ET.parse('test2.xml')  
    root = tree.getroot()
        #filename
        #volume
        #pan
        #effects
        #velocity
        #posX
        #posY
        #sizeW
        #sizeH

    # all item attributes
    for elem in root:  
        for subelem in elem:
            # basic attributes to an audio item
            filename = subelem.attrib['filename']
            volume = subelem.attrib['volume']
            pan = subelem.attrib['pan']
            # effects = subelem.attrib['effects']
            velocity = subelem.attrib['velocity']
            posX = subelem.attrib['posX']
            posY = subelem.attrib['posY']
            sizeW = subelem.attrib['sizeW']
            sizeH = subelem.attrib['sizeH']

            print("filename", "[{}]".format(filename))
            print("posX", posX)
            print("posY", posY)

            # check if we have a sub element aka a list of effects
            if len(subelem) > 1:
                for item in subelem:
                    if item.tag == 'effect':
                        for k,v in item.attrib.items():
                            print("  {} {}".format(k,v))
                        print("  ----------")
            print("-"*20)


read_project_file("demo_project.xml")

def write_project_file(audioitems, filename):

    # create the file structure
    data = ET.Element('data')  
    items = ET.SubElement(data, 'items')  

    for item in audioitems:
        #filename
        #volume
        #pan
        #effects
        #velocity
        #posX
        #posY
        #sizeW
        #sizeH
        item1 = ET.SubElement(items, 'audioitem')
        item1.set('filename', str(item.filename))
        item1.set('volume', str(item.volume))
        item1.set('pan', str(item.pan))
        item1.set('effects', str(item.effects))
        # for item in effects
            # effect = ET.SubElement(item1, 'effect')
            # effect.set('type', 'reverb')  
            # effect.set('size', '0.3')  
            # effect.set('damp', '1.0')  
            # effect.set('bal', '0.4')  
        item1.set('velocity', str(item.velocity))
        item1.set('posX', str(item.pos[0]))
        item1.set('posY', str(item.pos[1]))

        item1.set('sizeW', str(item.size[0]))
        item1.set('sizeH', str(item.size[1]))

    # create a new XML file with the results
    xmlstr = minidom.parseString(ET.tostring(data)).toprettyxml(indent="   ", encoding='UTF-8')
    mydata = str(xmlstr.decode('UTF-8'))
    myfile = open(filename, "w")  
    myfile.write(mydata)  


write_project_file(sample_audio_items, "test2.xml")