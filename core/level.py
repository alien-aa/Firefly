import pygame
import os

class Level:
    def __init__(self, config, level_num):
        self.config = config
        self.cell_size = config.cell_size
        self.level_num = level_num
        self.level_map = []
        self.walls = []
        self.floors = []
        self.player_start = (1, 1)
        self.firefly_path = []
        self.firefly_end = None
        self.wall_image = pygame.image.load(config.get_image_path("wall.png")).convert_alpha()
        self.floor_image = pygame.image.load(config.get_image_path("floor.png")).convert_alpha()
        self._load_level()
        self._parse_level()

    def _load_level(self):
        level_path = self.config.get_level_path(self.level_num)
        with open(level_path, 'r') as f:
            self.level_map = [line.rstrip('\n') for line in f]

    def _parse_level(self):
        self.walls = []
        self.floors = []
        self.player_start = None
        self.firefly_path = []
        self.firefly_end = None

        for y, row in enumerate(self.level_map):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.walls.append((x, y))
                else:
                    self.floors.append((x, y))
                if cell == 'P':
                    self.player_start = (x, y)
                elif cell == 'F':
                    self.firefly_end = (x, y)
        if self.player_start and self.firefly_end:
            x, y = self.player_start
            path = []
            visited = set()
            start_found = False
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx = x + dx
                ny = y + dy
                if 0 <= ny < len(self.level_map) and 0 <= nx < len(self.level_map[ny]):
                    if self.level_map[ny][nx] in ['r', 'l', 'u', 'd']:
                        x, y = nx, ny
                        start_found = True
                        break
            if not start_found:
                return
            while True:
                if (x, y) == self.firefly_end:
                    path.append((x, y))
                    break
                if (x < 0 or y < 0 or y >= len(self.level_map) or x >= len(self.level_map[y])):
                    break
                cell = self.level_map[y][x]
                if (x, y) in visited:
                    break
                visited.add((x, y))
                path.append((x, y))
                if cell == 'r':
                    x += 1
                elif cell == 'l':
                    x -= 1
                elif cell == 'u':
                    y -= 1
                elif cell == 'd':
                    y += 1
                elif cell == '_':
                    if len(path) >= 2:
                        prev_x, prev_y = path[-2]
                        dx = x - prev_x
                        dy = y - prev_y
                        x += dx
                        y += dy
                    else:
                        break
                else:
                    break
            self.firefly_path = path

    def draw(self, screen):
        for x, y in self.floors:
            screen.blit(self.floor_image, (x * self.cell_size, y * self.cell_size))
        for x, y in self.walls:
            screen.blit(self.wall_image, (x * self.cell_size, y * self.cell_size))

    def get_walls(self):
        return self.walls.copy()