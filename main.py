""" memory testcase """
import logging
import sys


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

from kivent_core.managers.resource_managers import texture_manager

NUMINROW=15
RECTSIZE=int(800/NUMINROW)
#how many textures should should be simultaneously on screen
NUMTEXTURES_USED = 6
USE_SINGLEATLAS = False

if len(sys.argv) >= 3:
    NUMTEXTURES_USED = int(sys.argv[1])
    USE_SINGLEATLAS = int(sys.argv[2])

if not USE_SINGLEATLAS:
    texture_manager.load_atlas('assets/atlas.atlas')
else:
    texture_manager.load_atlas('assets/singleatlas.atlas')



def rr(l):
    tl = []
    while True:
        if not tl:
            tl = l[:]
        yield tl.pop(0)

truefalse = rr([False, True])


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
                self.entities.append(self.gameworld.init_entity(create_component_dict, components_list))

        Clock.schedule_interval(self.change_texture, 0.05)

    def change_texture(self, dt):
        #if truefalse.next():
        #    return
        self.i += 1
        textures_available = [x%7 for x in range(self.i%7, self.i%7+NUMTEXTURES_USED)]
        numavail = len(textures_available)

        for i, x in enumerate(self.entities):
            new_texture_num = textures_available[(i + self.i)%numavail]

            new_texture = "texture-%s"%new_texture_num

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
    Logger.setLevel(logging.DEBUG)
    main()
