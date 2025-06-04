import pygame
import random
from collections import deque

from entities import Creature, Enemy
from ui import Button
from dungeon import generate_walls

pygame.init()

WIDTH_OPTIONS = [600, 800, 1000]
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

TITLE, SETTINGS, HELP, CHARACTER_SELECT, GAME = range(5)
state = TITLE
selected_size = WIDTH_OPTIONS[0]
sound_on = True

characters = [
    {"name": "Explorer", "color": (200, 200, 50), "hp": 5},
    {"name": "Mage", "color": (100, 50, 200), "hp": 4},
    {"name": "Knight", "color": (50, 200, 200), "hp": 6},
]
char_index = 0
player = None

screen = pygame.display.set_mode((selected_size, selected_size))
pygame.display.set_caption("BECAVE")

walls = generate_walls(selected_size)

captured = deque(maxlen=3)
particles = []

def reset_game():
    global player, enemies, captured, walls
    player = Creature(60, 60, characters[char_index]['color'], characters[char_index]['hp'])
    enemies = [Enemy(random.randint(100, selected_size-100), random.randint(100, selected_size-100)) for _ in range(5)]
    walls = generate_walls(selected_size)
    captured.clear()
    particles.clear()

help_text = ["WASD 로 이동", "d 키: 공격", "c 키: 포획", "s 키: 소환"]

sizes_buttons = []

start_btn = Button("START", (selected_size//2, selected_size-80), FONT)
back_btn = Button("BACK", (80, selected_size-50), FONT)
title_buttons = [start_btn, Button("SETTINGS", (selected_size//2, selected_size-140), FONT), Button("HELP", (selected_size//2, selected_size-200), FONT)]
for _ in WIDTH_OPTIONS:
    sizes_buttons.append(pygame.Rect(0,0,0,0))

reset_game()

running = True
while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False
        if state == TITLE:
            if any(b.clicked(evt) for b in title_buttons):
                if title_buttons[0].clicked(evt):
                    state = CHARACTER_SELECT
                elif title_buttons[1].clicked(evt):
                    state = SETTINGS
                elif title_buttons[2].clicked(evt):
                    state = HELP
        elif state == HELP:
            if back_btn.clicked(evt):
                state = TITLE
        elif state == SETTINGS:
            if back_btn.clicked(evt):
                screen = pygame.display.set_mode((selected_size, selected_size))
                state = TITLE
            if evt.type == pygame.MOUSEBUTTONDOWN:
                for i, r in enumerate(sizes_buttons):
                    if r.collidepoint(evt.pos):
                        selected_size = WIDTH_OPTIONS[i]
        elif state == CHARACTER_SELECT:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    char_index = (char_index - 1) % len(characters)
                elif evt.key == pygame.K_RIGHT:
                    char_index = (char_index + 1) % len(characters)
                elif evt.key in (pygame.K_RETURN, pygame.K_SPACE):
                    reset_game(); state = GAME
        elif state == GAME:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_c:
                    for e in enemies:
                        if pygame.Vector2(e.x-player.x, e.y-player.y).length() < 50 and e.hp <= 1:
                            captured.append(e); enemies.remove(e)
                            break
                elif evt.key == pygame.K_s and captured:
                    summ = captured.popleft()
                    enemies.append(summ)
                elif evt.key == pygame.K_d:
                    if player.cool <= 0:
                        near = min(enemies, key=lambda e: pygame.Vector2(e.x-player.x, e.y-player.y).length(), default=None)
                        if near and pygame.Vector2(near.x-player.x, near.y-player.y).length() < 60:
                            near.hp -= 1; player.cool = 20
                            if near.hp <= 0:
                                enemies.remove(near)
                                particles.append({'x':near.x,'y':near.y,'r':10,'color':(255,255,0)})
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE and state != TITLE:
            state = TITLE

    keys = pygame.key.get_pressed()
    if state == GAME:
        dx = dy = 0
        if keys[pygame.K_w]: dy = -3
        if keys[pygame.K_s]: dy = 3
        if keys[pygame.K_a]: dx = -3
        if keys[pygame.K_d]: dx += 3
        player.move(dx, dy, walls)
        if player.cool > 0: player.cool -= 1
        for e in enemies:
            e.update(walls)
            if pygame.Vector2(e.x-player.x, e.y-player.y).length() < player.r + e.r:
                player.hp = max(0, player.hp-1)
                vec = pygame.Vector2(player.x-e.x, player.y-e.y)
                if vec.length():
                    vec = vec.normalize()*10
                    player.move(vec.x, vec.y, walls)

    screen.fill((20,20,20))
    if state == TITLE:
        pygame.draw.rect(screen, (30,30,40), screen.get_rect())
        title = pygame.font.SysFont(None, 72).render("BECAVE", True, (255,255,255))
        screen.blit(title, title.get_rect(midtop=(selected_size//2, 40)))
        for b in title_buttons:
            b.draw(screen)
    elif state == HELP:
        screen.fill((50,50,60))
        y = 80
        for line in help_text:
            t = FONT.render(line, True, (255,255,255))
            screen.blit(t, (50, y)); y += 40
        back_btn.draw(screen)
    elif state == SETTINGS:
        screen.fill((60,60,70))
        y = 80
        t = FONT.render("화면 크기", True, (255,255,255))
        screen.blit(t, (50, y)); y += 40
        for i, opt in enumerate(WIDTH_OPTIONS):
            rect = pygame.Rect(60+i*110, y, 100, 40)
            pygame.draw.rect(screen, (180,180,180), rect)
            tx = FONT.render(str(opt), True, (0,0,0))
            screen.blit(tx, tx.get_rect(center=rect.center))
            sizes_buttons[i] = rect
        y += 80
        snd = FONT.render(f"사운드: {'ON' if sound_on else 'OFF'}", True, (255,255,255))
        screen.blit(snd, (50, y))
        back_btn.draw(screen)
    elif state == CHARACTER_SELECT:
        screen.fill((40,40,50))
        for i, ch in enumerate(characters):
            idx = (char_index+i-1) % len(characters)
            scale = 1.2 if i == 1 else 0.8
            c = characters[idx]
            x = selected_size//2 + (i-1)*200
            pygame.draw.circle(screen, c['color'], (x, selected_size//2), int(40*scale))
            name = FONT.render(c['name'], True, (255,255,255))
            screen.blit(name, name.get_rect(center=(x, selected_size//2+70)))
        start_btn.draw(screen)
    elif state == GAME:
        for w in walls:
            pygame.draw.rect(screen, (100,100,100), w)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)
        for i, c in enumerate(captured):
            pygame.draw.circle(screen, c.color, (selected_size-30, selected_size-30-i*30), 10)
        for p in list(particles):
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['r'])
            p['r'] -= 1
            if p['r'] <= 0:
                particles.remove(p)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
