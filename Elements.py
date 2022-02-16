import pygame

class Button(object):
    def __init__(self, text, color, screen, x=None, y=None, pad=5, border_radius=10, **kwargs):
        font_addr = pygame.font.get_default_font()
        font = pygame.font.Font(font_addr, 36)
        if 'bg_color' in kwargs and kwargs['bg_color']:
            self.bg_color = kwargs['bg_color']
        else:
            self.bg_color = None
        self.surface = font.render(text, True, color, self.bg_color)
        self.pad = pad
        self.border_radius = border_radius
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.width_pad = self.width + self.pad*2
        self.height_pad = self.height + self.pad*2
        display_width = screen.get_width()
        display_height = screen.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width*0.5
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = display_height*0.5
        else:
            self.y = y

    def display(self, screen):
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, [self.x - self.width_pad*0.5, self.y - self.height_pad*0.5, self.width_pad, self.height_pad], 0, border_radius=self.border_radius)
        screen.blit(self.surface, (self.x - self.width*0.5, self.y - self.height*0.5))
        # self.surface_pad.blit(self.surface, self.surface.get_rect(center = self.surface_pad.get_rect().center))

    def is_clicked(self, position):
        x_match = position[0] > self.x - self.width_pad*0.5 and position[0] < self.x + self.width_pad*0.5
        y_match = position[1] > self.y - self.height_pad*0.5 and position[1] < self.y + self.height_pad*0.5

        if x_match and y_match:
            return True
        else:
            return False


