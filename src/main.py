import pygame
import random

pygame.init()


BLACK = (255, 255, 12)
WHITE = (255, 255, 255)
RED = (random.randint(0, 255), 0, 0)

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's game of life")

clock = pygame.time.Clock()

GENERATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATE_EVENT, 1000)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


CELL_COLOR = ()


def grid_coordinate_to_point(coordinate):
    col, row = coordinate
    return row * GRID_WIDTH + col


def point_to_grid_coordinate(point):
    return (point % GRID_WIDTH, point // GRID_WIDTH)


def update_board(live_points: set):
    new_live = set()
    total_cells = GRID_WIDTH * GRID_HEIGHT

    for i in range(total_cells):
        col, row = point_to_grid_coordinate(i)
        alive = i in live_points

        # list neighbours
        neighbors = []
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if dc == 0 and dr == 0:
                    continue
                nc = col + dc
                nr = row + dr
                if 0 <= nc < GRID_WIDTH and 0 <= nr < GRID_HEIGHT:
                    p = grid_coordinate_to_point((nc, nr))
                    if p in live_points:
                        neighbors.append(p)

        count = len(neighbors)

        if alive:
            if 2 <= count <= 3:
                new_live.add(i)
        else:
            if count == 3:
                new_live.add(i)

    return new_live


def draw_grid(positions):

    for pos in positions:

        posCol, posRow = point_to_grid_coordinate(pos)
        top_left = (posCol * TILE_SIZE, posRow * TILE_SIZE)
        pygame.draw.rect(
            screen, RED, (*top_left, TILE_SIZE, TILE_SIZE), border_radius=20
        )

    for row in range(GRID_HEIGHT):
        pygame.draw.line(
            screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE), 1
        )

    for col in range(GRID_WIDTH):
        pygame.draw.line(
            screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT), 1
        )


def main():
    running = True
    playing = True
    positions = set(random.randint(0, (GRID_WIDTH**2 - 1)) for _ in range(125))

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE

                point = grid_coordinate_to_point((col, row))
                if point in positions:
                    positions.remove(point)
                else:
                    positions.add(point)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    positions = set(
                        random.randint(0, (GRID_WIDTH**2 - 1)) for _ in range(125)
                    )
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()

            if event.type == GENERATE_EVENT and playing:
                positions = update_board(positions)
                global RED
                RED = (random.randint(0, 255), 0, 0)

        draw_grid(positions)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
