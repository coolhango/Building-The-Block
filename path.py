import pygame
from constants import *
from heading import *
from vectors import *
from iso import *


class Path(Sprite):
    '''
    A path that has a beginning (start) and ending (end)
    and has any number of subsequent paths.
    '''
    def __init__(self, start, end, heading = Heading.NORTH):
        Sprite.__init__(self, None, vec2(0,0))
        self.heading = heading
        self.start = start
        self.end = end

    def draw(self, view):
        start_pos = view.project(self.start)
        end_pos   = view.project(self.end)
        pygame.draw.line(view.window, (255,0,0), (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
