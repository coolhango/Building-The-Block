import pygame

from gui import Widget


class Graph(Widget):

    INCOME = 0
    FUNDS = 1
    CONTENTMENT = 2

    def __init__(self, thegui, player):
        Widget.__init__(self)
        player.add_monthly_listener(self)
        self.thegui = thegui
        self.income_history = History()
        self.funds_history = History()
        self.contentment_history = History()
        self.mode = Graph.FUNDS
        self.font = pygame.font.SysFont("Arial",10)

    def set_mode(self, mode):
        self.mode = mode

    def display(self):
        self.thegui.add_widget(self)

    def hide(self):
        self.thegui.remove_widget(self)


    def on_month_end(self, month, funds, income, contentment):
        self.funds_history.add_value(funds)
        self.income_history.add_value(income)
        self.contentment_history.add_value(contentment)
        pass


    def draw(self, screen):
        w, h = self.thegui.get_size()

        canvas_width = w - 40
        canvas_height = h - 40 - 260

        surf = pygame.Surface((canvas_width, canvas_height))
        surf.fill((255,255,255))

        margin_left = (w - canvas_width) / 2
        margin_top = 20

        screen.blit(surf, (margin_left,margin_top))
        pygame.draw.rect(screen, (90, 90, 90), (20 , 20, canvas_width, canvas_height), 2)

        padding = 40
        graph_top_left = (margin_left + padding, margin_top + padding)
        graph_bottom_right = (margin_left + canvas_width - padding, margin_top + canvas_height -  padding)
        graph_bottom_left = (graph_top_left[0], graph_bottom_right[1])
        graph_dimensions = (graph_bottom_right[0] - graph_top_left[0], graph_bottom_right[1] - graph_top_left[0])

        axes_start = (graph_top_left[0], graph_bottom_right[1])
        x_axis_end = graph_bottom_right
        y_axis_end = graph_top_left

        pygame.draw.line(screen, (255, 0, 0), axes_start, x_axis_end)
        pygame.draw.line(screen, (0, 255, 0), axes_start, y_axis_end)

        if self.mode == Graph.INCOME:
            history = self.income_history
        elif self.mode == Graph.FUNDS:
            history = self.funds_history
        elif self.mode == Graph.CONTENTMENT:
            history = self.contentment_history

        length = history.get_length()
        if length == 0:
            length = 1

        # Draw the X axis months of the graph
        month_length = (graph_dimensions[0]) / length # Length of a single month on the x axis
        skip = length // 10
        for index in range(0, length + 1, skip + 1):
            month = index
            month_surf = self.font.render(str(month), True, (0,0,0))
            x = graph_bottom_left[0] + index * month_length
            y = graph_bottom_right[1]
            screen.blit(month_surf, (x, y))

        # Draw the "month" caption
        month_label = self.font.render("Month", True, (0,0,0))
        x = (graph_bottom_left[0] + graph_bottom_right[0]) / 2
        y = graph_bottom_left[1] + 10
        screen.blit(month_label, (x, y))

        # Draw the horizontal lines of the graph
        highest = history.get_highest()
        lowest  = history.get_lowest()

        if lowest == 0 and highest == 0:
            highest = 10

        def map(x, a, b, c, d):
            y = (x - a) / (b - a) * (d - c) + c
            return y


        for step in range(0, 11):
            value = step * (highest - lowest) / 10
            y = map(value, lowest, highest, graph_bottom_left[1], graph_top_left[1])

            start_x = graph_bottom_left[0]
            start_y = y
            end_x = graph_bottom_right[0]
            end_y = y

            pygame.draw.line(screen,(0,0,0), (start_x, start_y), (end_x, end_y))

            rounded_val = round(value)
            value_surf = self.font.render(str(rounded_val), True, (0,0,0))
            screen.blit(value_surf, (graph_bottom_left[0] - 34, y - 5))

        # Draw the graph lines
        current_point = previous_point = None
        pixels_per_unit = graph_dimensions[1] / (highest - lowest)
        for index, value in enumerate(history.get_values()):
            x = graph_bottom_left[0] + index * month_length
            y = graph_bottom_left[1] - pixels_per_unit * value

            current_point = (x, y)
            if previous_point is None:
                previous_point = current_point
                continue
            else:
                pygame.draw.aaline(screen,(255,0,0), current_point, previous_point)
                previous_point = current_point


class History:

    def __init__(self):
        self.values = [0]

    def add_value(self, value):
        self.values.append(value)

    def get_value(self, index):
        return self.values[index]

    def get_length(self):
        return len(self.values)

    def get_highest(self):
        if self.get_length() == 0: return 0
        return max(self.values)

    def get_lowest(self):
        if self.get_length() == 0: return 0
        return min(self.values)

    def get_values(self):
        return self.values

