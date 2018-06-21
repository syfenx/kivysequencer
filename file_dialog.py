# from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from file_save_loader import FileSystem

import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class FileLoader(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    audioitems = ObjectProperty(None)
    def __init__(self):
        self.filesystem = FileSystem()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename, audioitems, can):
        path = os.path.join(path, filename[0])
        print("load from: ", path)
        self.filesystem.read_project_file(audioitems, path, can)
        self.dismiss_popup()

    def save(self, path, filename, audioitems):
        path = os.path.join(path, filename)
        print("save path: ", path)
        print("save audio items count: ", len(audioitems))
        self.filesystem.write_project_file(audioitems, path)
        self.dismiss_popup()
        
Factory.register('Root', cls=FileLoader)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)