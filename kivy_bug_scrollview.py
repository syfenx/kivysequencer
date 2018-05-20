import kivy
kivy.require("1.10.0")
from kivy.app import App

from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from random import randint
from kivy.graphics import Color, Ellipse

# Steps to reproduce error
# Window opens, move scrollbars, resize window, maximize
# ** It might not happen right away.

class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)

        self.size_hint=(None,None)
        self.size=(5000,5000)
        with self.canvas:
            Color(1, 1, 0)
            for x in range(5000):
                Ellipse(pos=(randint(0,self.size[0]),randint(0,self.size[1])), size=(5, 5))


class BaseLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BaseLayout, self).__init__(**kwargs)


class BaseApp(App):
    def __init__(self, **kwargs):
        super(BaseApp, self).__init__(**kwargs)

    def build(self):
        base_layout = BaseLayout()

        step_base = ScrollView(
            size_hint=(1,1),
            do_scroll_y=True,
            do_scroll_x=True)
        step_base.bar_width=20
        step_base.scroll_type = ['bars']

        paint_widget = MyPaintWidget()
        step_base.add_widget(paint_widget)

        return step_base

base_app = BaseApp()
base_app.run()