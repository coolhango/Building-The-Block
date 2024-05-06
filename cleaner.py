from assets import load_image
from constants import Layer
from iso import Sprite
from vectors import vec3



class Cleaner:

    FLOOR_CLEAN_TIME = 2000
    STATUS_ALREADY_CLEANING = 0
    STATUS_CLEAN = 1
    STATUS_CLEAN_STARTED = 2
    STATUS_CLEAN_ENDED = 3

    def __init__(self, building, view):
        self.building = building
        self.view = view
        self.cleaning = False
        self.rollers_sprite = Sprite(load_image("building/rollers.png"))
        self.rollers_sprite.set_layer(Layer.OBJECTS_LAYER)
        self.platform_sprite = Sprite(load_image("building/cleaner_platform.png"))
        self.platform_sprite.set_layer(Layer.OBJECTS_LAYER)
        self.lines_sprites = []
        self.floors_idx_queue = []
        self.current_floor_index = -1
        self.clean_time = 0
        self.listener = None

    def set_listener(self, listener):
        self.listener = listener

    def clean(self):
        if self.cleaning: return Cleaner.STATUS_ALREADY_CLEANING

        building = self.building
        indices = building.get_dirty_floors_idx()
        if len(indices) == 0: return Cleaner.STATUS_CLEAN

        self.cleaning = True
        height = self.calc_building_height()
        self.rollers_sprite.set_location(vec3(3, 4.8, height))
        self.view.add_sprite(self.rollers_sprite)

        self.floors_idx_queue = sorted(indices[:])
        self.view.add_sprite(self.platform_sprite)
        if len(self.floors_idx_queue) > 0:
            self.current_floor_index = self.floors_idx_queue.pop()
            self.relocate_platform()

        return Cleaner.STATUS_CLEAN_STARTED

    def calc_building_height(self):
        building = self.building
        height = building.level
        return height

    def update(self, clock):
        if self.cleaning:
            self.clean_time += clock.get_time()
            if self.clean_time > Cleaner.FLOOR_CLEAN_TIME:
                self.building.set_floor_clean(self.current_floor_index)
                if len(self.floors_idx_queue) > 0:
                    self.current_floor_index = self.floors_idx_queue.pop()
                    self.relocate_platform()
                else:
                    self.end_clean()
                self.clean_time = 0

    def relocate_platform(self):
        height = self.current_floor_index
        self.platform_sprite.set_location(vec3(3, 4.8, height))
        for sprite in self.lines_sprites:
            self.view.remove_sprite(sprite)
        self.lines_sprites.clear()

        building_height = self.calc_building_height()
        lines_image = load_image("building/cleaner_ropes.png")
        for y in range(height + 1, building_height + 1):
            sprite = Sprite(lines_image)
            sprite.set_layer(Layer.OBJECTS_LAYER)
            sprite.set_location(vec3(3,4.8, y))
            self.lines_sprites.append(sprite)
            self.view.add_sprite(sprite)


    def end_clean(self):
        self.view.remove_sprite(self.rollers_sprite)
        for sprite in self.lines_sprites:
            self.view.remove_sprite(sprite)
        self.view.remove_sprite(self.platform_sprite)
        self.cleaning = False
        self.listener.state_changed(Cleaner.STATUS_CLEAN_ENDED)


class CleanerStateListener:

    def state_changed(self, state):
        pass