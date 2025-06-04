import pygame

class Button:
    def __init__(self, text: str, pos: tuple, font: pygame.font.Font):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(pos[0]-60, pos[1]-20, 120, 40)
        self.font = font

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, (180, 180, 180), self.rect)
        t = self.font.render(self.text, True, (0, 0, 0))
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, evt):
        return evt.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evt.pos)
