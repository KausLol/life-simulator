import random
import pygame

# Conway's Game of Life Simulator
# This program simulates Conway's Game of Life, a cellular automaton devised by John Conway.
# Rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

pygame.init()

black = (0, 0, 0)
grey = (176, 175, 182)
white = (255, 255, 255)

# window and tile size
width, height = 900, 900
tile_size = 10

grid_width = width // tile_size
grid_height = height // tile_size

fps = 60

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


# main code
def main():
    running = True
    playing = False
    count = 0  # a counter to control the update frequency
    update_freq = 6  # determines how often the grid is updated

    # a set to store positions of live cells
    positions = set()

    while running:
        clock.tick(fps)  # limits frame rate to 60

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)  # updates cell states

        # window caption
        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            # exits the program
            if event.type == pygame.QUIT:
                running = False

            # toggles the state of a cell
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // tile_size
                row = y // tile_size
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                # plays or pauses the simulation
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # clears the grid
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                # generates random live cells
                if event.key == pygame.K_x:
                    positions = gen(random.randrange(8, 18) * grid_width)

        screen.fill(white)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


# draws the grid lines and live cells
def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * tile_size, row * tile_size)
        pygame.draw.rect(screen, black, (*top_left, tile_size, tile_size))

    for row in range(grid_height):
        pygame.draw.line(screen, grey, (0, row * tile_size), (width, row * tile_size))

    for col in range(grid_width):
        pygame.draw.line(screen, grey, (col * tile_size, 0), (col * tile_size, height))


# calculates the next generation of cells
def adjust_grid(positions):
    all_neighbours = set()
    new_positions = set()

    for position in positions:
        neighbours = get_neighbours(position)
        all_neighbours.update(neighbours)

        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbours:
        neighbours = get_neighbours(position)
        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 3:
            new_positions.add(position)

    return new_positions


# returns a list of neighbouring cells for a given cell
def get_neighbours(pos):
    x, y = pos
    neighbours = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > grid_width:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > grid_height:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbours.append((x + dx, y + dy))

    return neighbours


# generates a random initial population of cells
def gen(num):
    return set(
        [
            (random.randrange(0, grid_height), random.randrange(0, grid_width))
            for _ in range(num)
        ]
    )


if __name__ == "__main__":
    main()
