import pygame
import random

class Creature:
    def __init__(self, x: float, y: float, color, hp: int, sprite: pygame.Surface = None):
        self.x, self.y = x, y
        self.color = color
        self.max_hp = hp
        self.hp = hp
        self.r = 15
        self.cool = 0
        self.sprite = sprite

    def draw(self, surf: pygame.Surface):
        if self.sprite:
            rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(self.sprite, rect)
        else:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.r)
        for i in range(self.hp):
            pygame.draw.rect(surf, (255, 0, 0), (self.x - 10 + i * 8, self.y - self.r - 15, 6, 6))

    def move(self, dx: float, dy: float, walls):
        nx, ny = self.x + dx, self.y + dy
        for w in walls:
            if w.collidepoint(nx, ny):
                return
        self.x, self.y = nx, ny

class Enemy(Creature):
    def __init__(self, x: float, y: float, sprite: pygame.Surface = None):
        color = tuple(random.randint(50, 255) for _ in range(3))
        super().__init__(x, y, color, 3, sprite)
        self.dir = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

    def update(self, walls):
        if random.random() < 0.02:
            self.dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.dir.length():
                self.dir = self.dir.normalize()
        speed = 2
        if random.random() < 0.01:
            speed = 6
        self.move(self.dir.x * speed, self.dir.y * speed, walls)
