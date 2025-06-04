import pygame
import random

def generate_walls(width: int):
    walls = []
    tile_size = 40
    for _ in range(15):
        x = random.randint(0, width - tile_size)
        y = random.randint(0, width - tile_size)
        walls.append(pygame.Rect(x, y, tile_size, tile_size))
    return walls
