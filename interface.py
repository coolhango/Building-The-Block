import pygame.font

from cleaner import Cleaner, CleanerStateListener
from graph import Graph
from vectors import vec2
import assets
import gui


class Interface(CleanerStateListener):

    def __init__(self, main):
        self.main = main

        self.upgrade_cost_txt = None
        self.upgrade_button_controls = []
        self.create_upgrade_button()

        self.helipad_button_controls = []
        self.create_helipad_button()

        self.clean_button_controls = []
        self.create_clean_button()

        self.rent_slider_controls = []
        self.rent_amount_text = None
        self.rent_slider = None
        self.status_bar = None
        self.create_rent_slider()

        self.contentment_gauge_controls = []
        self.contentment_icon = None
        self.contentment_happy_icon = assets.load_image("happy.png")
        self.contentment_indifferent_icon = assets.load_image("indifferent.png")
        self.contentment_unhappy_icon = assets.load_image("unhappy.png")
        self.contentment_very_unhappy_icon = assets.load_image("very_unhappy.png")
        self.create_contentment_gauge()

        self.date_gauge_controls = []
        self.date_month_txt = None
        self.date_day_txt = None
        self.create_date_gauge()

        self.funds_gauge_txt = None
        self.funds_gauge_controls = []
        self.create_funds_gauge()

        self.graph_mode_indicator = None
        self.graph_controls = []
        self.create_graph_controls()
        self.graph_button_controls = []
        self.create_graph_button()
        self.graph_visible = False
        self.create_graph()

        self.create_status_bar()

    def display(self):
        self.display_upgrade_button()
        self.display_helipad_button()
        self.display_clean_button()
        self.display_rent_slider()
        self.display_contentment_gauge()
        self.display_date_gauge()
        self.display_graph_button()
        self.display_funds_gauge()

    def create_upgrade_button(self):
        thegui = self.main.gui
        world = self.main.world

        w, h = thegui.get_size()
        y = 260

        font = assets.load_font("Teko-Bold.ttf", 24)
        upgrade_text = gui.Text("Upgrade", font)
        upgrade_text.set_position(vec2(10, h - y + 10))
        self.upgrade_button_controls.append(upgrade_text)

        upgrade_button = gui.Button(assets.load_image("upgrade_button.png"), self.upgrade)
        upgrade_button.set_position(vec2(0, h - y))
        self.upgrade_button_controls.append(upgrade_button)

        font2 = assets.load_font("Teko-Bold.ttf", 16)
        upgrade_cost_str = "$" + str(world.building.get_upgrade_cost())
        upgrade_cost_txt = gui.Text(upgrade_cost_str, font2, (255, 255, 255))
        upgrade_cost_txt.set_position(vec2(20, h - y + 35))
        self.upgrade_cost_txt = upgrade_cost_txt
        self.upgrade_button_controls.append(upgrade_cost_txt)

        upgrade_cost_bg = gui.ImageWidget(assets.load_image("upgrade_cost_bg.png"))
        upgrade_cost_bg.set_position(vec2(0, h - y + 30))
        self.upgrade_button_controls.append(upgrade_cost_bg)

    def display_upgrade_button(self):
        for control in self.upgrade_button_controls:
            self.main.gui.add_widget(control)

    def hide_upgrade_button(self):
        for widget in self.upgrade_button_controls:
            self.main.gui.remove_widget(widget)

    def create_helipad_button(self):
        thegui = self.main.gui
        world = self.main.world

        w, h = thegui.get_size()
        y = 200

        font = assets.load_font("Teko-Bold.ttf", 24)
        helipad_text = gui.Text("Helipad", font)
        helipad_text.set_position(vec2(10, h - y + 10))
        self.helipad_button_controls.append(helipad_text)

        helipad_button = gui.Button(assets.load_image("helipad_button.png"), self.build_helipad)
        helipad_button.set_position(vec2(0, h - y))
        self.helipad_button_controls.append(helipad_button)

        font2 = assets.load_font("Teko-Bold.ttf", 16)
        helipad_cost_str = "$" + str(5000)
        helipad_cost_txt = gui.Text(helipad_cost_str, font2, (255, 255, 255))
        helipad_cost_txt.set_position(vec2(20, h - y + 35))
        self.helipad_button_controls.append(helipad_cost_txt)

        helipad_cost_bg = gui.ImageWidget(assets.load_image("upgrade_cost_bg.png"))
        helipad_cost_bg.set_position(vec2(0, h - y + 30))
        self.helipad_button_controls.append(helipad_cost_bg)

    def display_helipad_button(self):
        for control in self.helipad_button_controls:
            self.main.gui.add_widget(control)

    def hide_helipad_button(self):
        for widget in self.helipad_button_controls:
            self.main.gui.remove_widget(widget)

    def create_clean_button(self):
        thegui = self.main.gui
        world = self.main.world

        w, h = thegui.get_size()
        y = 140

        font = assets.load_font("Teko-Bold.ttf", 24)
        clean_text = gui.Text("Clean", font)
        clean_text.set_position(vec2(10, h - y + 10))
        self.clean_button_controls.append(clean_text)

        clean_button = gui.Button(assets.load_image("clean_button.png"), self.clean)
        clean_button.set_position(vec2(0, h - y))
        self.clean_button_controls.append(clean_button)

        font2 = assets.load_font("Teko-Bold.ttf", 16)
        clean_cost_str = "$" + str(world.building.get_upgrade_cost())
        clean_cost_txt = gui.Text(clean_cost_str, font2, (255, 255, 255))
        clean_cost_txt.set_position(vec2(20, h - y + 35))
        self.clean_button_controls.append(clean_cost_txt)

        clean_cost_bg = gui.ImageWidget(assets.load_image("upgrade_cost_bg.png"))
        clean_cost_bg.set_position(vec2(0, h - y + 30))
        self.clean_button_controls.append(clean_cost_bg)

    def display_clean_button(self):
        for control in self.clean_button_controls:
            self.main.gui.add_widget(control)

    def hide_clean_button(self):
        for control in self.clean_button_controls:
            self.main.gui.remove_widget(control)

    def create_rent_slider(self):
        thegui = self.main.gui
        w, h = thegui.get_size()

        font = assets.load_font("Teko-Regular.ttf", 16)
        self.rent_amount_text = gui.Text("Rent: $1000", font)
        self.rent_amount_text.set_position(vec2(10, h - 56))
        self.rent_slider_controls.append(self.rent_amount_text)

        rail_img = assets.load_image("slider_rail.png")
        knob_img = assets.load_image("slider_knob.png")

        self.rent_slider = gui.Slider(rail_img, knob_img, self.rent_changed)
        self.rent_slider.set_position(vec2(70, h - 60))
        self.rent_slider_controls.append(self.rent_slider)

        rent_slider_bg = gui.ImageWidget(assets.load_image("rent_slider_bg.png"))
        rent_slider_bg.set_position(vec2(0, h - 64))
        self.rent_slider_controls.append(rent_slider_bg)

    def display_rent_slider(self):
        for control in self.rent_slider_controls:
            self.main.gui.add_widget(control)

    def create_contentment_gauge(self):
        thegui = self.main.gui

        w, h = thegui.get_size()

        font = assets.load_font("Teko-Regular.ttf", 16)
        contentment_txt = gui.Text("Contentment", font)
        contentment_txt.set_position(vec2(600 - 74, h - 114))
        self.contentment_gauge_controls.append(contentment_txt)

        self.contentment_icon = gui.ImageWidget(assets.load_image("happy.png"))
        self.contentment_icon.set_position(vec2(600 - 54, h - 96))
        self.contentment_gauge_controls.append(self.contentment_icon)

        contentment_bg = gui.ImageWidget(assets.load_image("contentment_bg.png"))
        contentment_bg.set_position(vec2(600 - 146, h - 116))
        self.contentment_gauge_controls.append(contentment_bg)

    def display_contentment_gauge(self):
        for control in self.contentment_gauge_controls:
            self.main.gui.add_widget(control)

    def create_date_gauge(self):
        # Create the date gauge, that is in the lower right corner, above the funds gauge
        thegui = self.main.gui

        w, h = thegui.get_size()

        date_font = assets.load_font("Teko-Regular.ttf", 14)

        self.date_month_txt = gui.Text("Month: 1", date_font)
        self.date_month_txt.set_position(vec2(600 - 50, h - 62))
        self.date_gauge_controls.append(self.date_month_txt)

        self.date_day_txt = gui.Text("Day: 1", date_font)
        self.date_day_txt.set_position(vec2(600 - 45, h - 48))
        self.date_gauge_controls.append((self.date_day_txt))

        date_bg_img = assets.load_image("date_bg.png")
        date_bg_widget = gui.ImageWidget(date_bg_img)
        date_bg_widget.set_position(vec2(600 - 146, h - 65))
        self.date_gauge_controls.append(date_bg_widget)

    def display_date_gauge(self):
        for control in self.date_gauge_controls:
            self.main.gui.add_widget(control)

    def create_funds_gauge(self):
        # Create the funds gauge, that is in the lower right corner
        thegui = self.main.gui
        player = self.main.player

        w, h = thegui.get_size()

        font = assets.load_font("Teko-Bold.ttf", 16)
        funds = player.get_funds()
        self.funds_gauge_txt = gui.Text("Funds: $" + str(funds), font, (255, 255, 255))
        self.funds_gauge_txt.set_position(vec2(600 - 134, h - 22))
        self.funds_gauge_controls.append(self.funds_gauge_txt)

        funds_gauge_bg = gui.ImageWidget(assets.load_image("funds_gauge_bg.png"))
        funds_gauge_bg.set_position(vec2(600 - 173, h - 31))
        self.funds_gauge_controls.append(funds_gauge_bg)

    def display_funds_gauge(self):
        for control in self.funds_gauge_controls:
            self.main.gui.add_widget(control)

    def create_status_bar(self):
        thegui = self.main.gui
        self.status_bar = StatusBar(thegui)

    def create_graph_button(self):
        # Create the funds gauge, that is in the lower right corner
        thegui = self.main.gui
        player = self.main.player

        w, h = thegui.get_size()

        self.graph_button = gui.Button(assets.load_image("graph.png"), self.toggle_graph)
        self.graph_button.set_position(vec2(w - 30, h - 26))

    def display_graph_button(self):
        thegui = self.main.gui
        thegui.add_widget(self.graph_button)

    def create_graph(self):
        self.graph = Graph(self.main.gui, self.main.player)

    def display_graph(self):
        self.graph.display()
        thegui = self.main.gui
        for control in self.graph_controls:
            thegui.add_widget(control)

    def hide_graph(self):
        self.graph.hide()
        thegui = self.main.gui
        for control in self.graph_controls:
            thegui.remove_widget(control)

    def toggle_graph(self):
        if not self.graph_visible:
            self.display_graph()
        else:
            self.hide_graph()
        self.graph_visible = not self.graph_visible

    def create_graph_controls(self):
        font = assets.load_font("Teko-Bold.ttf", 20)
        thegui = self.main.gui
        w, h = thegui.get_size()
        x = 400
        y = h - 270

        funds_button = gui.Button(assets.load_image("graph_mode_funds.png"), self.set_graph_mode_funds)
        funds_button.set_position(vec2(x, y))
        funds_text = gui.Text("Funds", font, (0,0,0))
        funds_text.set_position(vec2(x + 45, y + 4))
        self.graph_controls.append(funds_text)
        self.graph_controls.append(funds_button)

        self.graph_mode_indicator = gui.Button(assets.load_image("graph_mode_indicator.png"))
        self.graph_mode_indicator.set_position(vec2(x-34, y + 4))
        self.graph_controls.append(self.graph_mode_indicator)

        y += 30
        income_button = gui.Button(assets.load_image("graph_mode_income.png"), self.set_graph_mode_income)
        income_button.set_position(vec2(x, y))
        income_text = gui.Text("Income", font, (0, 0, 0))
        income_text.set_position(vec2(x + 39, y + 4))
        self.graph_controls.append(income_text)
        self.graph_controls.append(income_button)

        y += 30
        contentment_button = gui.Button(assets.load_image("graph_mode_contentment.png"), self.set_graph_mode_contentment)
        contentment_button.set_position(vec2(x, y))
        contentment_text = gui.Text("Contentment", font, (0, 0, 0))
        contentment_text.set_position(vec2(x + 25, y + 4))
        self.graph_controls.append(contentment_text)
        self.graph_controls.append(contentment_button)



    def set_graph_mode_funds(self):
        self.graph.set_mode(Graph.FUNDS)
        thegui = self.main.gui
        w, h = thegui.get_size()
        x = 400
        y = h - 270
        self.graph_mode_indicator.set_position(vec2(x - 34, y + 4))

    def set_graph_mode_income(self):
        self.graph.set_mode(Graph.INCOME)
        thegui = self.main.gui
        w, h = thegui.get_size()
        x = 400
        y = h - 240
        self.graph_mode_indicator.set_position(vec2(x - 34, y + 4))

    def set_graph_mode_contentment(self):
        self.graph.set_mode(Graph.CONTENTMENT)
        thegui = self.main.gui
        w, h = thegui.get_size()
        x = 400
        y = h - 210
        self.graph_mode_indicator.set_position(vec2(x - 34, y + 4))

    def upgrade(self):
        '''
        Upgrade the main building
        '''
        world = self.main.world
        player = self.main.player

        cost = world.building.get_upgrade_cost()
        if world.building.can_upgrade():
            if player.draw_funds(cost):
                world.building.upgrade()
                if world.building.has_helipad():
                    world.building.destroy_helipad()
                    self.display_helipad_button()

                self.update_funds_gauge()

                cost = world.building.get_upgrade_cost()
                self.upgrade_cost_txt.set_text("$" + str(cost))
            else:
                self.status_bar.show_message("Insufficient funds")

        if not world.building.can_upgrade():
            self.hide_upgrade_button()

    def build_helipad(self):
        buiding = self.main.world.building
        player = self.main.player
        cost = buiding.get_helipad_cost()

        if player.draw_funds(cost) and not buiding.has_helipad():
            buiding.make_helipad()
            self.hide_helipad_button()
        elif buiding.has_helipad():
            self.status_bar.show_message("Already built")
            self.hide_helipad_button()
        else:
            self.status_bar.show_message("Insufficient funds")

    def clean(self):
        building = self.main.world.building
        player = self.main.player
        if player.draw_funds(1000):
            status = building.clean()
            if status == Cleaner.STATUS_CLEAN:
                self.status_bar.show_message("Building already clean")
            if status == Cleaner.STATUS_ALREADY_CLEANING:
                self.status_bar.show_message("Building is being cleaned")
            if status == Cleaner.STATUS_CLEAN_STARTED:
                self.hide_clean_button()
                cleaner = building.get_cleaner()
                cleaner.set_listener(self)

    def state_changed(self, state):
        if state == Cleaner.STATUS_CLEAN_ENDED:
            self.display_clean_button()

    def rent_changed(self, percentage):
        building = self.main.world.building

        rent = int(percentage / 100 * 2000)
        self.rent_amount_text.set_text("Rent: $" + str(rent))

        building.set_rent(rent)

    def update(self, clock):
        self.update_funds_gauge()
        self.status_bar.update(clock)
        self.update_contentment()
        self.update_date_gauge(clock)

    def update_funds_gauge(self):
        player = self.main.player
        funds = player.get_funds()
        self.funds_gauge_txt.set_text("Funds: $" + str(funds))

    def update_date_gauge(self, clock):
        world = self.main.world
        month = world.get_month()
        day = world.get_day()

        self.date_month_txt.set_text("Month: " + str(month))
        self.date_day_txt.set_text("Day: " + str(day))

    def update_contentment(self):
        building = self.main.world.building
        contentment = building.get_contentment()
        if contentment >= 0 and contentment < 20:
            self.contentment_icon.set_image(self.contentment_very_unhappy_icon)
        elif contentment >= 20 and contentment < 40:
            self.contentment_icon.set_image(self.contentment_unhappy_icon)
        elif contentment >=40 and contentment < 70:
            self.contentment_icon.set_image(self.contentment_indifferent_icon)
        elif contentment >= 70 and contentment <= 100:
            self.contentment_icon.set_image(self.contentment_happy_icon)

    def get_status_bar(self):
        return self.status_bar


class StatusBar:

    def __init__(self, thegui):
        self.gui = thegui

        w, h = thegui.get_size()

        background_img = assets.load_image("status_bar_bg.png")
        self.background = gui.ImageWidget(background_img)
        self.background.set_position(vec2(0, h - 20))

        font = assets.load_font("Teko-Regular.ttf", 18)
        self.text = gui.Text("Status bar", font)
        self.text.set_position(vec2(10, h - 18))

        self.message = None
        self.time = 0
        self.timeout = 0

    def display(self):
        self.gui.add_widget(self.text)
        self.gui.add_widget(self.background)

    def hide(self):
        self.gui.remove_widget(self.text)
        self.gui.remove_widget(self.background)

    def update(self, clock):
        if self.message is not None:
            if self.time > self.timeout:
                self.message = None
                self.hide()
            self.time += clock.get_time()



    def show_message(self, message):
        if self.message is None:
            self.message = message
            self.time = 0
            self.timeout = len(message) * 100
            self.text.set_text(message)
            self.display()
