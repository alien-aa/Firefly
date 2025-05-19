import pygame

from core.level import Level
from entities.player import Player
from entities.firefly import Firefly

class Game:
    MENU = 0
    GAME = 1
    END = 2

    def __init__(self, config):
        self.config = config
        self.width, self.height = config.screen_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.current_state = self.MENU
        self.current_level = config.initial_level
        self.total_levels = config.total_levels
        self._load_resources()
        self._init_game_objects()

    def _load_resources(self):
        self.menu_music = pygame.mixer.Sound(self.config.get_sound_path("menu.ogg"))
        self.game_music = pygame.mixer.Sound(self.config.get_sound_path("game.ogg"))
        # Use fonts from config if available, else fallback to default pygame font
        try:
            self.title_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 74)
            self.text_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 36)
            self.control_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 24)
        except Exception:
            self.title_font = pygame.font.SysFont("arial", 74)
            self.text_font = pygame.font.SysFont("arial", 36)
            self.control_font = pygame.font.SysFont("arial", 24)

    def _init_game_objects(self):
        self.level = None
        self.player = None
        self.firefly = None

    def _init_level(self):
        self.level = Level(self.config, self.current_level)
        self.player = Player(self.config, *self.level.player_start)
        self.firefly = Firefly(self.config, self.level.firefly_path)
        self.current_state = self.GAME

    def _handle_menu_events(self, event):
        if event.key == pygame.K_RETURN:
            self.menu_music.stop()
            self.game_music.play(-1)
            self._init_level()

    def _handle_game_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game_music.stop()
            self.menu_music.play(-1)
            self.current_state = self.MENU

    def _check_level_completion(self):
        # Уровень завершён, если игрок достиг последней точки пути светлячка
        if self.firefly.path and (self.player.grid_x, self.player.grid_y) == self.firefly.path[-1]:
            if self.current_level < self.total_levels:
                self.current_level += 1
                self._init_level()
            else:
                self.game_music.stop()
                self.menu_music.play(-1)
                self.current_state = self.END

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.current_state == self.MENU:
                    self._handle_menu_events(event)
                elif self.current_state == self.GAME:
                    self._handle_game_events(event)
                elif self.current_state == self.END and event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self, dt):
        if self.current_state == self.GAME:
            self.firefly.update(dt, wait_for_player=(self.player.grid_x, self.player.grid_y))
            self.player.update(dt, self.level.get_walls())
            self._check_level_completion()

    def draw(self):
        self.screen.fill(self.config.colors['background'])
        if self.current_state == self.MENU:
            self._draw_menu()
        elif self.current_state == self.GAME:
            self._draw_game(show_player=True)
        elif self.current_state == self.END:
            self._draw_end()
        pygame.display.flip()

    def _draw_menu(self):
        title = self.title_font.render("Firefly", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(title, title_rect)

        prompt = self.text_font.render("Press ENTER to start", True, (200, 200, 200))
        prompt_rect = prompt.get_rect(center=(self.width // 2, self.height * 2 // 3))
        self.screen.blit(prompt, prompt_rect)

        # Controls
        controls = [
            "W/S/A/D - move",
            "ESC - exit to menu",
            "Follow the firefly!"
        ]
        y = self.height - 80
        for line in controls:
            surf = self.control_font.render(line, True, (180, 180, 180))
            rect = surf.get_rect(center=(self.width // 2, y))
            self.screen.blit(surf, rect)
            y += 28

    def _draw_game(self, show_player=True):
        self.level.draw(self.screen)
        if show_player:
            self.player.draw(self.screen)
        self.firefly.draw(self.screen)

    def _draw_end(self):
        text = self.title_font.render("The End", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        self.menu_music.play(-1)
        running = True
        while running:
            dt = self.clock.tick(self.config.fps) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
