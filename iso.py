from functools import cmp_to_key

from vectors import *


HTW = 36
HTH = 18
VSTEP = 26

class View:

    def __init__(self, window):
        self.window = window
        self.sprites = []


    def project(self, location: vec3) -> vec2:
        x = (location.x - location.y) * HTW
        y = (location.x + location.y) * HTH - location.z * VSTEP

        w, h = self.window.get_size()

        x += w / 2
        y += h / 2

        return vec2(x, y)


    def add_sprite(self, sprite):
        if not sprite in self.sprites:
            self.sprites.append(sprite)


    def remove_sprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)


    def draw(self):
        self.sort_sprites()

        for sprite in self.sprites:
            sprite.draw(self)


    def sort_sprites(self):
        self.sprites.sort(key=cmp_to_key(self.compare_sprites))


    def compare_sprites(self, sprite1, sprite2):
        if sprite1.layer != sprite2.layer:
            return sprite1.layer - sprite2.layer
        else:
            spr1_loc = sprite1.get_location()
            spr2_loc = sprite2.get_location()

            sum1 = spr1_loc.x + spr1_loc.y + spr1_loc.z
            sum2 = spr2_loc.x + spr2_loc.y + spr2_loc.z

            return sum1 - sum2


class Sprite:

    def __init__(self, image, anchor=None):
        """ 
        Create isometric sprite providing the image
        of the sprite and optionally the image anchoring point.
        If the anchoring point argument is missing, then the
        sprite's anchoring point is set to the middle of the image.
        """
        self.image = image
        self.location = vec3(0, 0, 0)
        self.layer = 0
        if anchor is None:
            w, h = self.image.get_size()
            self.anchor = vec2(w / 2, h / 2)
        else:
            self.anchor = anchor


    def draw(self, view: View):
        if self.image is None: return

        pos = view.project(self.location)
        draw_x = pos.x - self.anchor.x
        draw_y = pos.y - self.anchor.y

        view.window.blit(self.image, (draw_x, draw_y))


    def set_location(self, location):
        self.location = location


    def get_location(self):
        return self.location


    def set_layer(self, layer):
        self.layer = layer


    def set_image(self, image):
        self.image = image