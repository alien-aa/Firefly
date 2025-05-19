import pygame

class Player:
    def __init__(self, config, grid_x, grid_y):
        self.config = config
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = config.cell_size
        self.color = config.colors['player']
        self.move_timer = 0.0

    def update(self, dt, walls):
        """Update player position based on held keys and move cooldown."""
        self.move_timer += dt

        if self.move_timer >= self.config.move_cooldown:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            # Запрет диагонального движения: приоритет W/S над A/D
            if keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_s]:
                dy = 1
            elif keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_d]:
                dx = 1

            if dx != 0 or dy != 0:
                if self.move(dx, dy, walls):
                    self.move_timer = 0.0

    def move(self, dx, dy, walls):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if (new_x, new_y) not in walls:
            self.grid_x = new_x
            self.grid_y = new_y
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.grid_x * self.cell_size,
             self.grid_y * self.cell_size,
             self.cell_size,
             self.cell_size)
        )
