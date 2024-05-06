import random
from iso import *
from constants import *
from heading import *
from assets import *



class Car(Sprite):
    '''
    Car class for cars travelling the screen.
    '''
    def __init__(self, path):
        Sprite.__init__(self, self.get_random_car_image(path.heading))
        self.path = path
        self.interpolator = 0
        self.set_location(path.start)
        self.layer = Layer.OBJECTS_LAYER

    def get_random_car_image(self, heading):
        '''
        Get a random car image for vehicles to vary.
        '''
        options = ["car_1_red", "dodge", "peterbilt", "van", "car_1_blue", "impreza"]
        heading_str = "north" if heading == Heading.NORTH else "south"
        car_name = random.choice(options)
        img_name = car_name + "_" + heading_str + ".png"
        return load_image("cars/" + img_name)

    def update(self, clock):
        '''
        Update the car position by interpolating the vehicle path, and play the sound of a car randomly
        '''
        rnd = random.randint(0,11000)
        if rnd == 0 or rnd == 1:
            car_sound = load_sound(f"car_{rnd + 1}.wav")
            car_sound.play()

        loc = self.path.start.lerp(self.path.end, self.interpolator)
        distance = self.path.start.distance(self.path.end)
        self.set_location(loc)
        self.interpolator += (0.01 / distance) * (clock.get_time() / 30)
        if self.interpolator < 1:
            return True
        else:
            return False
