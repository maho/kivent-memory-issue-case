""" memory testcase """

import logging
from random import randint
import sys

formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(levelname)s][%(message)s]", "%H:%M:%S")
console = logging.StreamHandler() 
console.setFormatter(formatter)
sys._kivy_logging_handler = console

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

from kivent_core.managers.resource_managers import texture_manager

if 1:
    texture_manager.load_atlas('assets/atlas.atlas')
else:
    texture_manager.load_atlas('assets/singleatlas.atlas')

NUMINROW=17
RECTSIZE=int(800/NUMINROW)

class TestGame(Widget):
    def __init__(self, **kwargs):
        self.entities = []
        self.i = 0
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()

    def draw_some_stuff(self):
        for x in range(NUMINROW):
            for y in range(NUMINROW):
                create_component_dict = {
                    'position': (RECTSIZE/2 + x*RECTSIZE, RECTSIZE/2 + y*RECTSIZE),
                    }
                components_list = ['position', 'renderer']

                create_component_dict['renderer'] = {
                    'size': (RECTSIZE, RECTSIZE),
                    'render': True,
                    'texture': "texture-%s"%((x+y)%7),
                    'copy': True
                }
                Logger.debug("create_component_dict=%r", create_component_dict)
                self.entities.append(self.gameworld.init_entity(create_component_dict, components_list))

        Clock.schedule_interval(self.change_texture, 0.1)

    def change_texture(self, dt):
        self.i += 1
        for i, x in enumerate(self.entities):
            #new_texture = "texture-%s"%((i + self.i)%7)
            #new_texture = "texture-%s"%((i + self.i)%7)
            new_texture = "texture-%s"%((self.i)%7)

            self.gameworld.entities[x].renderer.texture_key = new_texture


    def setup_states(self):
        self.gameworld.add_state(state_name='main',
            systems_added=['renderer'],
            systems_removed=[], systems_paused=[],
            systems_unpaused=['renderer'],
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'

class YourAppNameApp(App):
    """ app """
    def build(self):
        Window.clearcolor = (0, 0, 0, 1.)

def main():
    YourAppNameApp().run()

if __name__ == '__main__':
    main()
