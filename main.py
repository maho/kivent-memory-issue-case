""" memory testcase """

from random import randint

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

from kivent_core.managers.resource_managers import texture_manager

texture_manager.load_atlas('assets/atlas.atlas')
#texture_manager.load_atlas('assets/singleatlas.atlas')

class TestGame(Widget):
    def __init__(self, **kwargs):
        self.entities = []
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['renderer', 'position'],
            callback=self.init_game)

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.draw_some_stuff()

    def draw_some_stuff(self):
        for x in range(5):
            for y in range(5):
                create_component_dict = {
                    'position': (100+x*100, 100+y*100),
                    }
                components_list = ['position', 'renderer']

                create_component_dict['renderer'] = {
                    'size': (100, 100),
                    'render': True,
                    'texture': "texture-%s"%((x+y)%7)
                }
                Logger.debug("create_component_dict=%r", create_component_dict)
                self.entities.append(self.gameworld.init_entity(create_component_dict, components_list))

        Clock.schedule_interval(self.change_texture, 0.1)

    def change_texture(self, dt):
        for i, x in enumerate(self.entities):
            new_texture = "texture-%s"%randint(0,6)
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
