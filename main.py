""" memory testcase """

from itertools import cycle
from random import choice

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

from kivent_core.managers.resource_managers import texture_manager

texture_manager.load_atlas('assets/onetwo.atlas')

class TestGame(Widget):
    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()

    def draw_some_stuff(self):
        create_component_dict = {
            'position': (200, 200),
            }
        components_list = ['position', 'renderer']

        create_component_dict['renderer'] = {
            'size': (500, 500),
            'render': True,
            'texture': 'one'
        }
        Logger.debug("create_component_dict=%r", create_component_dict)
        self.entity_id = self.gameworld.init_entity(create_component_dict, components_list)
        self.available_textures = cycle(['one', 'two'])

        Clock.schedule_interval(self.change_texture, 0.1)

    def change_texture(self, dt):
        self.gameworld.entities[self.entity_id].renderer.texture_key = self.available_textures.next()


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

if __name__ == '__main__':
    YourAppNameApp().run()
