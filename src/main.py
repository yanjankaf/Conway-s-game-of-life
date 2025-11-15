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


def update_board(point: set):
    new_points = point.copy()
    for i in range(0, (GRID_WIDTH**2 - 1)):
        if i in point:
            POINT_TYPE = "live"
        else:
            POINT_TYPE = "dead"

        col, row = point_to_grid_coordinate(i)

        potential = [
            (col - 1, row - 1),
            (col, row - 1),
            (col + 1, row - 1),
            (col - 1, row),
            (col + 1, row),
            (col - 1, row + 1),
            (col, row + 1),
            (col + 1, row + 1),
        ]

        neighbors = []

        for (
            c,
            r,
        ) in potential:
            p = grid_coordinate_to_point((c, r))
            if 0 <= p <= (GRID_WIDTH**2 - 1) and p in new_points:
                neighbors.append(p)

        if POINT_TYPE == "live":
            if len(neighbors) < 2 or len(neighbors) > 3:
                new_points.discard(i)
        else:
            if len(neighbors) == 3:
                new_points.add(i)

    return new_points


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

    positions = set(random.randint(0, (GRID_WIDTH**2 - 1)) for _ in range(125))

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    positions = set(
                        random.randint(0, (GRID_WIDTH**2 - 1)) for _ in range(125)
                    )

            if event.type == GENERATE_EVENT:
                positions = update_board(positions)
                global RED
                RED = (random.randint(0, 255), 0, 0)

        draw_grid(positions)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
