import random

from cleaner import Cleaner
from constants import *
from assets import *
from iso import *
from vectors import *


class Building:
    def __init__(self, view):
        self.view = view
        self.sprites = []
        self.level = 1
        self.helipad = None
        self.rent = 1000
        self.contentment = 100

        self.abandon_timeout = 0
        self.abandon_time = 0
        self.comeback_timeout = 0
        self.comeback_time = 0
        self.abandoned_floors_idx = [] # Array of indexes of abandoned floors

        self.dirty_time = 0 # The time since last appearance of new dirty floor
        self.dirty_timeout = 40000 # A new dirty floor will appear every 40 seconds (40 000 ms)
        self.dirty_floors_idx = [] # Array of indexes of dirty floors
        self.cleaner = Cleaner(self, self.view)

        self.make_sprites()

    def display(self):
        self.add_to_view()

    def add_to_view(self):
        for sprite in self.sprites:
            self.view.add_sprite(sprite)

    def remove_from_view(self):
        for sprite in self.sprites:
            self.view.remove_sprite(sprite)

    def can_upgrade(self):
        return self.level < Gameplay.MAX_BUILDING_LEVEL

    def upgrade(self):
        if not self.level < Gameplay.MAX_BUILDING_LEVEL:
            return False
        self.level += 1
        self.remove_from_view()
        self.sprites.clear()
        self.make_sprites()
        self.add_to_view()
        return True

    def make_sprites(self):
        self.add_foundation()
        self.add_base()
        y = self.add_floors()
        self.add_roof(y)

    def add_foundation(self):
        foundation_spr = Sprite(load_image("building/foundation.png"))
        foundation_spr.set_location(vec3(3, 3, 0))
        self.sprites.append(foundation_spr)

    def add_base(self):
        base_spr = Sprite(load_image("building/base.png"))
        base_spr.set_layer(Layer.OBJECTS_LAYER)
        base_spr.set_location(vec3(3, 3, 0))
        self.sprites.append(base_spr)

    def add_floors(self):
        y = 0
        for y in range(1, self.level):
            if y in self.abandoned_floors_idx:
                floor_img = load_image("building/abandoned_floor.png")
            elif y in self.dirty_floors_idx:
                floor_img = load_image("building/dirty_floor.png")
            else:
                floor_img = load_image("building/floor.png")
            floor_spr = Sprite(floor_img)
            floor_spr.set_layer(Layer.OBJECTS_LAYER)
            floor_spr.set_location(vec3(3, 3, y))
            self.sprites.append(floor_spr)
        return y

    def add_roof(self, y):
        roof_spr = Sprite(load_image("building/roof.png"))
        roof_spr.set_layer(Layer.OBJECTS_LAYER)
        roof_spr.set_location(vec3(3, 3, y + 1))
        self.sprites.append(roof_spr)

    def make_helipad(self):
        y = self.level
        self.helipad = Sprite(load_image("building/helipad.png"))
        self.helipad.set_layer(Layer.OBJECTS_LAYER)
        self.helipad.set_location(vec3(3, 3, y + 0.01))
        self.view.add_sprite(self.helipad)

    def destroy_helipad(self):
        self.view.remove_sprite(self.helipad)
        self.helipad = None

    def has_helipad(self):
        return self.helipad is not None

    def get_upgrade_cost(self):
        return self.level * 1000

    @staticmethod
    def get_helipad_cost():
        return 5000

    def get_level(self):
        return self.level

    def set_rent(self, rent):
        # Set the per floor rent drawn every month
        self.rent = rent

    def get_rent(self):
        ''' Get the per floor rent'''
        return self.rent

    def get_total_rent(self):
        ''' Get the total rent for a month, from every floor. '''
        total_rent = 0
        for floor_idx in range(0, self.level):
            base_rent = self.get_rent()
            rent = base_rent
            if floor_idx in self.dirty_floors_idx:
                rent *= 0.5
            if floor_idx in self.abandoned_floors_idx:
                rent = 0
            total_rent += rent
        has_helipad = self.has_helipad()
        if has_helipad:
            total_rent += total_rent * 0.5
        return total_rent

    def update_contentment(self):
        rent = self.get_rent()
        contentment = self.get_contentment()

        relative_rent = rent - 1000
        contentment += -(relative_rent / 50)

        self.set_contentment(int(contentment))

    def set_contentment(self, contentment):
        if contentment > 100:
            contentment = 100
        elif contentment < 0:
            contentment = 0
        self.contentment = contentment
        if contentment >= 70:
            self.abandon_time = 0
            self.abandon_timeout = 0
            self.comeback_timeout = 40000
        else:
            self.comeback_timeout = 0
            self.comeback_time = 0

        if 70 > contentment >= 40:
            self.abandon_timeout = 20000
        elif 40 > contentment >= 20:
            self.abandon_timeout = 10000
        elif contentment < 20:
            self.abandon_timeout = 5000

    def get_contentment(self):
        return self.contentment

    def clean(self):
        return self.cleaner.clean()

    def get_dirty_floors_idx(self):
        return self.dirty_floors_idx

    def get_cleaner(self):
        return self.cleaner

    def update(self, clock):
        if self.abandon_timeout > 0:
            self.abandon_time += clock.get_time()
            if self.abandon_time > self.abandon_timeout:
                self.abandon_time = 0
                self.make_abandoned_floor()

        if self.comeback_timeout > 0:
            self.comeback_time += clock.get_time()
            if self.comeback_time > self.comeback_timeout:
                self.comeback_time = 0
                self.remove_abandoned_floor()

        self.dirty_time += clock.get_time()
        if self.dirty_time > self.dirty_timeout:
            self.make_dirty_floor()
            self.dirty_time = 0

        self.cleaner.update(clock)

    def make_abandoned_floor(self):
        candidate_floors = []
        for floor_idx in range(1, self.level):
            if not floor_idx in self.abandoned_floors_idx:
                candidate_floors.append(floor_idx)

        if len(candidate_floors) > 0:
            idx = random.choice(candidate_floors)
            self.abandoned_floors_idx.append(idx)
            self.remake_floors()

    def remove_abandoned_floor(self):
        if len(self.abandoned_floors_idx) > 0:
            self.abandoned_floors_idx.pop()
            self.remake_floors()

    def make_dirty_floor(self):
        candidate_floors = []
        for floor_idx in range(1, self.level):
            if not floor_idx in self.dirty_floors_idx:
                candidate_floors.append(floor_idx)

        if len(candidate_floors) > 0:
            idx = random.choice(candidate_floors)
            self.dirty_floors_idx.append(idx)
            self.remake_floors()

    def set_floor_clean(self, index):
        if index in self.dirty_floors_idx:
            self.dirty_floors_idx.remove(index)
            self.remake_floors()

    def remake_floors(self):
        self.remove_from_view()
        self.sprites.clear()
        self.make_sprites()
        self.add_to_view()


