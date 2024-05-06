import random
import pygame
from building import *
from car import *
from chopper import *
from constants import *
from vectors import *
from path import *

class World:
    '''
    The world class, where everything visible in the view belongs.
    '''
    def __init__(self, main):
        self.main = main
        self.month = 1 # The current world month
        self.day = 1   # The current world day
        self.time = 0  # The time used to update month and day
        self.paths = []
        self.cars  = []
        self.spawn_time = 0 # Car spawn time
        self.chopper = Chopper(self)

        self.create_building()
        self.create_ground()
        self.create_parks()
        self.create_parking()
        self.create_factory()
        self.create_paths()

    def display(self):
        view = self.main.view
        view.add_sprite(self.roads)
        self.building.display()
        view.add_sprite(self.factory)
        view.add_sprite(self.park1)
        view.add_sprite(self.park2)
        view.add_sprite(self.parking)

    def create_ground(self):
        '''
        Create ground - thst is - the terrain and the roads.
        '''
        view = self.main.view
        self.terrain = Sprite(load_image("terrain.png"))
        self.terrain.set_layer(Layer.TERRAIN_LAYER)
        view.add_sprite(self.terrain)
        self.roads = Sprite(load_image("roads.png"))
        self.roads.set_layer(Layer.OVERLAYS_LAYER)

    def create_building(self):
        '''
        Create the main building, the Real Estate
        '''
        view = self.main.view

        self.building = Building(view)

    def create_factory(self):
        '''
        Create the factory in the top-right corner of the screen
        '''
        view = self.main.view
        self.factory = Sprite(load_image("factory.png"))
        self.factory.set_layer(Layer.OBJECTS_LAYER)
        self.factory.set_location(vec3(-3.05, -9, 0))

    def create_parks(self):
        '''
        Create parks in the bottom left side of the screen
        '''
        view = self.main.view

        self.park1 = Sprite(load_image("park1.png"))
        self.park1.set_layer(Layer.OBJECTS_LAYER)
        self.park1.set_location(vec3(9, 9, 0))

        self.park2 = Sprite(load_image("park2.png"))
        self.park2.set_layer(Layer.OBJECTS_LAYER)
        self.park2.set_location(vec3(3.1, 9, 0))

    def create_parking(self):
        view = self.main.view

        self.parking = Sprite(load_image("parking.png"))
        self.parking.set_layer(Layer.OVERLAYS_LAYER)
        self.parking.set_location(vec3(3, -3, 0))

    def create_paths(self):
        '''
        Create paths that the cars will use to travel.
        '''
        # Bottom row
        path = Path(vec3(6.25, 15), vec3(6.25, -12.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(5.75, -12.5), vec3(5.75, 15),  Heading.SOUTH)
        self.paths.append(path)

        # Middle row
        path = Path(vec3(0.25, 10), vec3(0.25, -12.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(-0.25, -12.5), vec3(-0.25, 10), Heading.SOUTH)
        self.paths.append(path)

        # Top row
        path = Path(vec3(-5.75, 6), vec3(-5.75, -16.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(-6.25, -16.5), vec3(-6.25, 6), Heading.SOUTH)
        self.paths.append(path)

    def update(self, clock):
        if self.time > Gameplay.MILLIS_PER_DAY:
            self.day += 1
            if self.day > 30:
                self.month += 1
                self.day = 1
            self.time = self.time - Gameplay.MILLIS_PER_DAY
            if self.day == 30:
                player = self.main.player
                self.on_day(self.month, self.day)
                player.on_day(self.month, self.day)

        self.time += clock.get_time()

        self.spawn_cars(clock)
        self.update_cars(clock)
        self.building.update(clock)
        self.chopper.update(clock)

    def on_day(self, month, day):
        if day == 30:
            self.building.update_contentment()

    def get_month(self):
        return self.month

    def get_day(self):
        return self.day

    def spawn_cars(self, clock):
        '''
        Spawn cars if their number is below certain threshold.
        '''
        view = self.main.view

        max_cars = self.building.get_level() * 2
        if len(self.cars) <  max_cars:
            if self.spawn_time > 500:
                path = random.choice(self.paths)
                car = Car(path)
                self.cars.append(car)
                view.add_sprite(car)
                self.spawn_time = 0

        self.spawn_time += clock.get_time()

    def update_cars(self, clock):
        '''
        Update all the cars - animate their driving animation.
        '''
        for car in self.cars:
            keep_car = car.update(clock)
            if keep_car == False:
                self.cars.remove(car)

