import pygame

class Player:
    def __init__(self, config, grid_x, grid_y):
        self.config = config
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = config.cell_size
        self.images = [
            pygame.image.load(config.get_image_path(f"player_{i}.png")).convert_alpha()
            for i in range(2)
        ]
        self.animation_delay = 0.18
        self.animation_timer = 0.0
        self.frame = 0
        self.move_timer = 0.0
        self.last_direction = (1, 0)
        self.last_position = (grid_x, grid_y)
        # Грузим изображение пола для очистки предыдущей позиции
        self.floor_image = pygame.image.load(config.get_image_path("floor.png")).convert_alpha()

    def update(self, dt, walls):
        self.move_timer += dt
        self.animation_timer += dt
        # Сохраняем предыдущую позицию
        self.last_position = (self.grid_x, self.grid_y)

        if self.animation_timer >= self.animation_delay:
            self.animation_timer -= self.animation_delay
            self.frame = (self.frame + 1) % 2

        if self.move_timer >= self.config.move_cooldown:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
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
                    self.last_direction = (dx, dy)
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
        img = self.images[self.frame]
        if self.last_direction[0] < 0:
            img = pygame.transform.flip(img, True, False)
        # Очищаем предыдущую позицию
        lx, ly = self.last_position
        screen.blit(self.floor_image, (lx * self.cell_size, ly * self.cell_size))
        # Рисуем новую позицию
        x = self.grid_x * self.cell_size
        y = self.grid_y * self.cell_size
        screen.blit(img, (x, y))
