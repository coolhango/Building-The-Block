from assets import *


class Player:

    def __init__(self, main):
        self.main = main
        self.funds = 10000
        self.income_sound = load_sound("money_collect.wav")
        self.monthly_listeners = []

    def add_monthly_listener(self, listener):
        self.monthly_listeners.append(listener)

    def draw_funds(self, amount):
        if self.funds - amount < 0:
            return False
        else:
            self.funds = self.funds - amount
            return True

    def get_funds(self):
        return self.funds

    def on_day(self, month, day):
        if day == 30:
            self.month_end(month)

    def month_end(self, month):
        income = self.draw_rent()
        contentment = self.main.world.building.get_contentment()
        for monthly_listener in self.monthly_listeners:
            monthly_listener.on_month_end(month, self.funds, income, contentment)


    def draw_rent(self):
        building = self.main.world.building
        income = building.get_total_rent()
        self.funds += income

        status_bar = self.main.interface.get_status_bar()
        status_bar.show_message("Income: $" + str(income))

        self.income_sound.play()
        return income
