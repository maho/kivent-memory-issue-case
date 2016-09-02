from functools import partial

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

from random import randint, choice
import kivent_core
from kivent_core.gameworld import GameWorld
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.renderers import Renderer
from kivent_core.managers.resource_managers import texture_manager
from kivy.properties import StringProperty
from os.path import dirname, join, abspath

texture_manager.load_atlas('assets/background_objects.atlas')

class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.load_models()
        self.draw_some_stuff()

    def load_models(self):
        model_manager = self.gameworld.model_manager
        model_manager.load_textured_rectangle('vertex_format_4f', 7., 7.,
            'star1', 'star1-4')
        model_manager.load_textured_rectangle('vertex_format_4f', 10., 10.,
            'star1', 'star1-4-2')

    def draw_some_stuff(self):
        init_entity = self.gameworld.init_entity

        mapx = 800
        mapy = 400

        for w, h, x, y, delay in [(mapx, 20, mapx/2, 0, 1.0),
                           (mapx, 20, mapx/2, mapy, 2.0),
                           (mapx/2, 20, mapx/2, mapy/2, 3.0),
                           ]:
            def _fn( w, h, x, y, dt):
                create_component_dict = {
                    'position': (x, y),
                    }
                components_list = ['position', 'renderer']

                create_component_dict['renderer'] = {
                    'size': (w, h),
                    'render': True,
                    'texture': 'asteroid1'
                }
                Logger.debug("create_component_dict=%r", create_component_dict)
                self.gameworld.init_entity(create_component_dict, components_list)
            Clock.schedule_once(partial(_fn, w, h, x, y), delay)


    def setup_states(self):
        self.gameworld.add_state(state_name='main',
            systems_added=['renderer'],
            systems_removed=[], systems_paused=[],
            systems_unpaused=['renderer'],
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'

class DebugPanel(Widget):
    fps = StringProperty(None)

    def __init__(self, **kwargs):
        super(DebugPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.update_fps)

    def update_fps(self,dt):
        self.fps = str(int(Clock.get_fps()))
        Clock.schedule_once(self.update_fps, .05)

class YourAppNameApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1.)

if __name__ == '__main__':
    YourAppNameApp().run()
