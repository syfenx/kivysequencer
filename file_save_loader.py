from xml.dom import minidom
import xml.etree.ElementTree as ET  

def read_project_file(filename):
    tree = ET.parse('demo_project2.xml')  
    root = tree.getroot()

    posX = root[0][1].attrib['posX']
    posY = root[0][1].attrib['posY']

    # all item attributes
    print('\nAll attributes:\n')  
    for elem in root:  
        for subelem in elem:
            # basic attributes to an audio item
            name = subelem.attrib['name']
            posX = subelem.attrib['posX']
            posY = subelem.attrib['posY']

            print("name", "[{}]".format(name))
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

def write_project_file(filename):
    # create the file structure
    data = ET.Element('data')  
    items = ET.SubElement(data, 'items')  

    item1 = ET.SubElement(items, 'audioitem')  
    item1.set('name','coolsnare')  
    item1.set('posX','27')  
    item1.set('posY','80')  
    fn = ET.SubElement(item1, 'filename')
    fn.set('path', '/sounds/snare1.wav')  
    effect = ET.SubElement(item1, 'effect')
    effect.set('type', 'reverb')  
    effect.set('size', '0.3')  
    effect.set('damp', '1.0')  
    effect.set('bal', '0.4')  

    item2 = ET.SubElement(items, 'audioitem')  
    item2.set('name','kick2')  
    item1.set('posX','44')  
    item1.set('posY','74')  
    fn = ET.SubElement(item2, 'filename')
    fn.set('path', '/sounds/kick2.wav')  

    # create a new XML file with the results
    xmlstr = minidom.parseString(ET.tostring(data)).toprettyxml(indent="   ", encoding='UTF-8')
    mydata = str(xmlstr.decode('UTF-8'))
    myfile = open(filename, "w")  
    myfile.write(mydata)  


write_project_file("test2.xml")