import pygame
import random

pygame.init()
W, H = 500, 600
win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

player = pygame.Rect(W//2 - 25, H - 60, 50, 50)
blocks = []
speed = 5
score = 0

running = True
while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 1
    if keys[pygame.K_RIGHT] and player.x < W - player.width:
        player.x += 1

    # spawn new blocks
    if random.random() < 0.02:
        blocks.append(pygame.Rect(random.randint(0, W-40), -40, 40, 40))

    # move blocks
    for b in blocks[:]:
        b.y += speed
        if b.y > H:
            blocks.remove(b)
            score += 1

        if player.colliderect(b):
            running = False

    win.fill((20, 20, 20))
    pygame.draw.rect(win, (0, 200, 255), player)
    for b in blocks:
        pygame.draw.rect(win, (255, 60, 60), b)

    pygame.display.flip()

pygame.quit()
print("Score:", score)
