import pygame

class Firefly:
    def __init__(self, config, path):
        self.config = config
        self.path = path  # Список координат [(x, y), ...]
        self.cell_size = config.cell_size
        self.images = [
            pygame.image.load(config.get_image_path(f"firefly_{i}.png")).convert_alpha()
            for i in range(3)
        ]
        self.animation_delay = config.firefly_animation_delay
        self.move_delay = config.firefly_move_delay  # Теперь берется из config.ini (замедлен!)
        self.animation_timer = 0.0
        self.move_timer = 0.0
        self.frame = 0
        self.index = 0  # Текущий индекс в маршруте
        self.waiting_for_player = False

    def update(self, dt, wait_for_player=None):
        if self.index >= len(self.path) - 1:
            self.waiting_for_player = True
            return

        if self.waiting_for_player:
            # Ждём, пока игрок дойдёт до точки
            if wait_for_player == self.path[-1]:
                # Можно добавить анимацию или звук, если нужно
                pass
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            self.animation_timer -= self.animation_delay
            self.frame = (self.frame + 1) % len(self.images)

        self.move_timer += dt
        if self.move_timer >= self.move_delay:
            self.move_timer -= self.move_delay
            if self.index < len(self.path) - 1:
                self.index += 1
                if self.index >= len(self.path) - 1:
                    self.waiting_for_player = True

    @property
    def pos(self):
        x, y = self.path[self.index]
        return x * self.cell_size, y * self.cell_size

    def draw(self, screen):
        img = self.images[self.frame]
        x, y = self.pos
        rect = img.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
        screen.blit(img, rect)
