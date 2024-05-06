import os

import pygame.image

images = {} # The cache of images
images_dir = "pixel"
images_dir = "svg"

def load_image(path):
    filepath = "assets" + os.sep + images_dir + os.sep + path

    if not filepath in images:
        # If the image is not cached load it and add to the cache:
        try:
            image = pygame.image.load(filepath).convert_alpha()
            images[filepath] = image
            return image
        except Exception as e:
            print("Cant load image: " + filepath)
            raise e
    else:
        # Else just return the cached image:
        return images[filepath]

fonts = {}

def load_font(path, size):
    filepath = "assets" + os.sep + path
    key = filepath + str(size)
    if not key in fonts:
        font = pygame.font.Font(filepath, size)
        fonts[key] = font
        return font
    else:
        return fonts[key]


sounds = {}
def load_sound(path):
    filepath = "assets" + os.sep + path
    if not path in sounds:
        sound = pygame.mixer.Sound(filepath)
        sounds[filepath] = sound
        return sound
    else:
        return sounds[filepath]
