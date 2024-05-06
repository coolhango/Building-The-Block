import pygame
import assets
import player
import iso
import gui
import world
import interface
from tkinter import *

# The main game class that is intantiated on startup.
class Game:

    def __init__(self, w, h):
        # Screen setup
        pygame.init()
        self.window = pygame.display.set_mode((w, h))
        pygame.display.set_caption("SREM")
        pygame.display.set_icon(assets.load_image("icon.png"))
        # The onscreen display objects creation:
        self.view = iso.View(self.window)
        self.gui = gui.Gui(self.window)
        # Player control object
        self.player = player.Player(self)
        # World creation
        self.world = world.World(self)
        self.world.display()
        # Interface creation
        self.interface = interface.Interface(self)
        self.interface.display()
        # Utilities
        self.done = False  # A flag for the game loop indicating if the game is done playing.
        self.clock = pygame.time.Clock() # Clock to control the framerate

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                else:
                    self.gui.on_event(event)

            self.update(self.clock)
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def update(self, clock):
        self.world.update(clock)
        self.interface.update(clock)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.view.draw()
        self.gui.draw()


def display_startup_dropdown():
    tk = Tk()
    tk.title("SREM")
    tk.geometry("300x120")
    tk.wm_iconphoto(False, PhotoImage(file="assets/pixel/icon.png"))

    screen_options = [
        "600x600",
        "600x700",
        "600x800"
    ]

    label = Label(tk, text="Select window size:")
    label.pack()

    selected_size = StringVar()
    selected_size.set("600x800")

    screen_dropdown = OptionMenu(tk, selected_size, *screen_options)
    screen_dropdown.pack()


    style_options = ["Pixelated", "Vector"]

    label = Label(tk, text="Select graphical style")
    label.pack()

    selected_style = StringVar()
    selected_style.set("Vector")

    style_dropdown = OptionMenu(tk, selected_style, *style_options)
    style_dropdown.pack()

    def start():
        size_str = selected_size.get()
        w = int(size_str.split("x")[0])
        h = int(size_str.split("x")[1])

        style_str = selected_style.get()
        if style_str == "Pixelated":
            assets.images_dir = "pixel"
        elif style_str == "Vector":
            assets.images_dir = "svg"

        tk.withdraw()
        tk.quit()
        game = Game(w, h)
        game.loop()

    ok_button = Button(tk, text="OK", command=start)
    ok_button.pack()
    tk.mainloop()


if __name__ == "__main__":
    display_startup_dropdown()
