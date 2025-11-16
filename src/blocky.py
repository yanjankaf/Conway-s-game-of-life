import pygame
import random

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OB_COLOR = (3, 190, 252)
PLAYER_COLOR = (255, 0, 0)

WIDTH, HEIGHT = 900, 400

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(100, 250, 50, 50)

gravity = 0.6
vy = 0
ground = 300

obstacles = []
spawn_timer = 0
speed = 6

min_gap = 200
max_gap = 400
next_gap = random.randint(min_gap, max_gap)


running = True

while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if (
                e.key == pygame.K_UP or e.key == pygame.K_SPACE
            ) and player.bottom == ground:
                vy = -12

    vy += gravity
    player.y += vy

    if player.bottom >= ground:
        player.bottom = ground
        vy = 0

    if len(obstacles) == 0:
        distance = WIDTH
    else:
        distance = WIDTH - obstacles[-1].right

    if distance >= next_gap:
        w = random.randint(30, 60)
        h = random.randint(40, 80)
        obstacles.append(pygame.Rect(WIDTH, ground - h, w, h))
        next_spawn_x = random.randint(min_gap, max_gap)

    for ob in obstacles[:]:
        ob.x -= speed
        if player.colliderect(ob):
            print("hit")
            running = False

        if ob.right < 0:
            obstacles.remove(ob)

    win.fill(WHITE)
    pygame.draw.line(win, BLACK, (0, 300), (WIDTH, 300), 2)
    pygame.draw.rect(win, PLAYER_COLOR, player)
    for ob in obstacles:
        pygame.draw.rect(win, OB_COLOR, ob)

    pygame.display.update()

pygame.quit()
