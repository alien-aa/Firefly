import pygame

class Firefly:
    def __init__(self, config, path):
        self.config = config
        self.path = path or []
        self.cell_size = config.cell_size
        self.images = [
            pygame.image.load(config.get_image_path(f"firefly_{i}.png")).convert_alpha()
            for i in range(4)
        ]
        self.animation_delay = config.firefly_animation_delay
        self.move_delay = config.firefly_move_delay
        self.animation_timer = 0.0
        self.move_timer = 0.0
        self.frame = 0
        self.index = 0
        self.waiting_for_player = False
        self.last_pos = None
        self.floor_image = pygame.image.load(config.get_image_path("floor.png")).convert_alpha()

    def update(self, dt, wait_for_player=None):
        self.last_pos = self.pos

        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            self.animation_timer -= self.animation_delay
            self.frame = (self.frame + 1) % 4

        if not self.path:
            return

        if self.index >= len(self.path) - 1:
            self.waiting_for_player = True
            return

        self.move_timer += dt
        if self.move_timer >= self.move_delay:
            self.move_timer -= self.move_delay
            if self.index < len(self.path) - 1:
                self.index += 1

    @property
    def pos(self):
        if not self.path:
            return (0, 0)
        x, y = self.path[self.index]
        return x * self.cell_size, y * self.cell_size

    def draw(self, screen):
        if self.last_pos:
            lx, ly = self.last_pos
            screen.blit(self.floor_image, (lx, ly))
        if self.path and self.index < len(self.path):
            img = self.images[self.frame]
            x, y = self.pos
            rect = img.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
            screen.blit(img, rect)
