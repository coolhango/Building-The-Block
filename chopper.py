import random
from iso import *
from assets import *
from path import *
from vectors import vec2, vec3
from constants import *


class Chopper(Sprite):

    MODE_INVISIBLE = -1
    MODE_APPROACHING = 0
    MODE_LANDING = 1
    MODE_HALT = 2
    MODE_STARTING = 3
    MODE_LEAVING = 4

    def __init__(self, world):
        Sprite.__init__(self, load_image("chopper/chopper0001.png"))
        self.world = world
        self.frames = []
        for i in range(1,5):
            frame_path = "chopper/chopper000" + str(i) + ".png"
            frame = load_image(frame_path)
            self.frames.append(frame)
        self.curr_frame = 0
        self.set_location(vec3(3, 3, 17))
        self.set_layer(Layer.OBJECTS_LAYER)

        self.random_display_countdown = random.randint(1000, 2000)
        self.mode = Chopper.MODE_INVISIBLE
        self.time = 0

    def update(self, clock):
        self.curr_frame += 1
        self.curr_frame %= 4
        self.set_image(self.frames[self.curr_frame])

        if self.mode == Chopper.MODE_INVISIBLE:
            self.random_display_countdown -= clock.get_time()
            if self.random_display_countdown < 0:
                building = self.world.building
                if building.has_helipad():
                    view = self.world.main.view
                    view.add_sprite(self)
                    self.is_visible = True
                    self.mode = Chopper.MODE_APPROACHING

        if self.mode == Chopper.MODE_APPROACHING:
            path = Path(vec3(-5, 3, 17), vec3(3,3,17))
            itpl = self.time / 3000
            loc = path.start.lerp(path.end, itpl)
            self.set_location(loc)

            self.time += clock.get_time()
            if self.time > 3000:
                self.mode = Chopper.MODE_LANDING
                self.time = 0

        if self.mode == Chopper.MODE_LANDING:
            building = self.world.building
            target_z = building.get_level()
            path = Path(vec3(3,3,17), vec3(3,3, target_z + 0.02))
            itpl = self.time / 3000
            loc = path.start.lerp(path.end, itpl)
            self.set_location(loc)

            self.time += clock.get_time()
            if self.time > 3000:
                self.mode = Chopper.MODE_HALT
                self.time = 0

        if self.mode == Chopper.MODE_HALT:
            self.time += clock.get_time()
            if self.time > 3000:
                chopper_start_sound = load_sound("chopper.wav")
                chopper_start_sound.play()
                self.mode = Chopper.MODE_STARTING
                self.time = 0

        if self.mode == Chopper.MODE_STARTING:
            building = self.world.building
            start_z = building.get_level()
            path = Path(vec3(3, 3, start_z + 0.02), vec3(3, 3, 17))
            itpl = self.time / 3000
            loc = path.start.lerp(path.end, itpl)
            self.set_location(loc)

            self.time += clock.get_time()
            if self.time > 3000:
                self.mode = Chopper.MODE_LEAVING
                self.time = 0

        if self.mode == Chopper.MODE_LEAVING:
            path = Path(vec3(3, 3, 17), vec3(20, 3, 17))
            itpl = self.time / 3000
            loc = path.start.lerp(path.end, itpl)
            self.set_location(loc)

            self.time += clock.get_time()
            if self.time > 3000:
                self.mode = Chopper.MODE_INVISIBLE
                self.random_display_countdown = random.randint(15000, 40000)
                self.time = 0