import pygame


class ColorButton:
    def __init__(self, color_id, rect, dim_color, bright_color):
        self.color_id = color_id
        self.rect = rect
        self.dim_color = dim_color
        self.bright_color = bright_color
        self.is_lit = False

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, surface):
        if self.is_lit:
            pygame.draw.rect(surface, self.bright_color, self.rect, border_radius=14)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, width=6, border_radius=14)
            pygame.draw.circle(surface, (255, 255, 255), self.rect.center, 16)
        else:
            pygame.draw.rect(surface, self.dim_color, self.rect, border_radius=14)
            pygame.draw.rect(surface, (70, 75, 85), self.rect, width=3, border_radius=14)