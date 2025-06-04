import pygame

class Button:
    def __init__(self, text: str, pos: tuple, font: pygame.font.Font,
                 base_color=(180, 180, 180), hover_color=(220, 220, 220)):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(pos[0]-60, pos[1]-20, 120, 40)
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, surf: pygame.Surface, hovered: bool = False):
        color = self.hover_color if hovered else self.base_color
        pygame.draw.rect(surf, color, self.rect)
        t = self.font.render(self.text, True, (0, 0, 0))
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, evt):
        return evt.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evt.pos)

    def hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
