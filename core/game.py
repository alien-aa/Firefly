import pygame

from core.level import Level
from entities.player import Player
from entities.firefly import Firefly


class Game:
    MENU = 0
    GAME = 1
    SLIDESHOW = 3
    END = 2

    def __init__(self, config):
        self.config = config
        self.width, self.height = config.screen_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.current_state = self.MENU
        self.current_level = config.initial_level
        self.total_levels = config.total_levels

        self.slideshow_slides = [
            {"speaker": "Firefly", "text": "*shining*", "color": (255, 255, 255)},
            {"speaker": "Player", "text": "What's there? I think I see a light. Is this the way out?",
             "color": (255, 255, 255)},
            {"speaker": "Firefly", "text": "* Opens the door carefully *",
             "color": (255, 255, 255)},
            {"speaker": "Firefly", "text": "Go to the light and don't touch the doors.",
             "color": (255, 255, 255)},
            {"speaker": "Player", "text": "You are my light.", "color": (255, 255, 150)}
        ]

        self.current_slide = 0
        self.slide_background = None
        self.continue_prompt = None

        self._load_resources()
        self._init_game_objects()
        self._init_light_masks()

    def _load_resources(self):
        self.menu_music = pygame.mixer.Sound(self.config.get_sound_path("menu.ogg"))
        self.game_music = pygame.mixer.Sound(self.config.get_sound_path("game.ogg"))

        try:
            self.menu_background_img = pygame.image.load(self.config.get_image_path("menu.png")).convert()
            self.menu_background = self._prepare_background_image(self.menu_background_img)
        except Exception as e:
            print(f"Error loading menu background: {e}")
            self.menu_background = pygame.Surface((self.width, self.height))
            self.menu_background.fill((0, 0, 0))

        try:
            self.end_background_img = pygame.image.load(self.config.get_image_path("end.png")).convert()
            self.end_background = self._prepare_background_image(self.end_background_img)
        except Exception as e:
            print(f"Error loading end background: {e}")
            self.end_background = pygame.Surface((self.width, self.height))
            self.end_background.fill((0, 0, 0))

        try:
            self.title_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 74)
            self.text_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 36)
            self.control_font = pygame.font.Font(self.config.get_font_path("ZenMasters.ttf"), 24)
        except Exception:
            self.title_font = pygame.font.SysFont("arial", 74)
            self.text_font = pygame.font.SysFont("arial", 36)
            self.control_font = pygame.font.SysFont("arial", 24)

    def _prepare_background_image(self, image):
        img_width, img_height = image.get_size()
        crop_width = min(img_width, self.width)
        crop_height = min(img_height, self.height)
        x_offset = max(0, (img_width - crop_width) // 2)
        y_offset = max(0, (img_height - crop_height) // 2)

        background = pygame.Surface((self.width, self.height))
        background.fill((0, 0, 0))  

        try:
            cropped = image.subsurface((x_offset, y_offset,
                                        min(crop_width, img_width - x_offset),
                                        min(crop_height, img_height - y_offset)))

            x_pos = (self.width - cropped.get_width()) // 2
            y_pos = (self.height - cropped.get_height()) // 2
            background.blit(cropped, (x_pos, y_pos))

            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))

            background.blit(overlay, (0, 0))

            return background

        except Exception as e:
            print(f"Error cropping background image: {e}")
            background.fill((0, 0, 0))
            return background

    def _init_game_objects(self):
        self.level = None
        self.player = None
        self.firefly = None

    def _init_level(self):
        self.level = Level(self.config, self.current_level)
        self.player = Player(self.config, *self.level.player_start)
        self.firefly = Firefly(self.config, self.level.firefly_path)
        self.current_state = self.GAME

    def _init_slideshow(self):
        try:
            final_img = pygame.image.load(self.config.final_image_path).convert()
            img_width, img_height = final_img.get_size()
            crop_width = min(img_width, self.width)
            crop_height = min(img_height, self.height)
            x_offset = max(0, (img_width - crop_width) // 2)
            y_offset = max(0, (img_height - crop_height) // 2)
            self.slide_background = pygame.Surface((self.width, self.height))
            cropped = final_img.subsurface((x_offset, y_offset, min(crop_width, img_width - x_offset),
                                            min(crop_height, img_height - y_offset)))
            self.slide_background.fill((0, 0, 0))
            x_pos = (self.width - cropped.get_width()) // 2
            y_pos = (self.height - cropped.get_height()) // 2
            self.slide_background.blit(cropped, (x_pos, y_pos))
        except Exception as e:
            print(f"Error loading final image: {e}")
            self.slide_background = pygame.Surface((self.width, self.height))
            self.slide_background.fill((0, 0, 0))

        self.continue_prompt = self.control_font.render("Press 'Enter' to continue", True, (180, 180, 180))
        self.current_slide = 0
        self.current_state = self.SLIDESHOW

    def _init_light_masks(self):
        cell_size = self.config.cell_size
        self.player_light_mask = self._create_light_mask(int(cell_size * 1.5), alpha=210)
        self.firefly_light_mask = self._create_light_mask(int(cell_size * 3.5), alpha=180)

    def _create_light_mask(self, radius, alpha=220):
        size = radius * 2
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        for r in range(radius, 0, -1):
            step_alpha = int(alpha * (1 - r / radius))
            pygame.draw.circle(mask, (0, 0, 0, step_alpha), center, r)
        return mask

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

    def _handle_slideshow_events(self, event):
        if event.key == pygame.K_RETURN:
            self.current_slide += 1
            if self.current_slide >= len(self.slideshow_slides):
                self.current_state = self.END

    def _check_level_completion(self):
        if self.firefly.path and (self.player.grid_x, self.player.grid_y) == self.firefly.path[-1]:
            if self.current_level < self.total_levels:
                self.current_level += 1
                self._init_level()
            else:
                self.game_music.stop()
                self._init_slideshow()
                self._init_slideshow()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False


            if event.type == pygame.KEYDOWN:
                if self.current_state == self.MENU:
                    self._handle_menu_events(event)
                elif self.current_state == self.GAME:
                    self._handle_game_events(event)
                elif self.current_state == self.SLIDESHOW:
                    self._handle_slideshow_events(event)
                elif self.current_state == self.END and event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self, dt):
        if self.current_state == self.GAME:
            self.firefly.update(dt, wait_for_player=(self.player.grid_x, self.player.grid_y))
            self.player.update(dt, self.level.get_walls())
            self._check_level_completion()
        elif self.current_state == self.SLIDESHOW:
            self.player.animation_timer += dt
            self.firefly.animation_timer += dt

            if self.player.animation_timer >= self.player.animation_delay:
                self.player.animation_timer -= self.player.animation_delay
                self.player.frame = (self.player.frame + 1) % len(self.player.images)

            if self.firefly.animation_timer >= self.firefly.animation_delay:
                self.firefly.animation_timer -= self.firefly.animation_delay
                self.firefly.frame = (self.firefly.frame + 1) % len(self.firefly.images)

    def _draw_slideshow(self):
        self.screen.blit(self.slide_background, (0, 0))

        strip_height = 150
        strip_top = self.height - strip_height - 50
        strip = pygame.Surface((self.width, strip_height), pygame.SRCALPHA)
        strip.fill((0, 0, 0, 180))
        self.screen.blit(strip, (0, strip_top))

        slide_data = self.slideshow_slides[self.current_slide]
        speaker_text = self.control_font.render(slide_data["speaker"] + ":", True, (255, 255, 255))
        speaker_rect = speaker_text.get_rect(topleft=(50, strip_top + 20))
        self.screen.blit(speaker_text, speaker_rect)

        text = slide_data["text"]
        color = slide_data["color"]
        text_height = 70
        words = text.split()
        line = ""

        for word in words:
            test_line = line + word + " "
            test_width = self.control_font.size(test_line)[0]
            if test_width > self.width - 100:
                line_surf = self.control_font.render(line, True, color)
                self.screen.blit(line_surf, (50, strip_top + text_height))
                text_height += line_surf.get_height() + 10
                line = word + " "
            else:
                line = test_line

        if line:
            line_surf = self.control_font.render(line, True, color)
            self.screen.blit(line_surf, (50, strip_top + text_height))

        prompt_rect = self.continue_prompt.get_rect(bottomright=(self.width - 20, self.height - 20))
        self.screen.blit(self.continue_prompt, prompt_rect)

        if slide_data["speaker"] == "Player":
            img = pygame.transform.scale(
                self.player.images[self.player.frame],
                (self.config.cell_size * 8, self.config.cell_size * 8)
            )
            img_rect = img.get_rect(center=(self.width // 4, strip_top - 100))
            if self.player.last_direction[0] < 0:
                img = pygame.transform.flip(img, True, False)
            self.screen.blit(img, img_rect)
        elif slide_data["speaker"] == "Firefly":
            img = pygame.transform.scale(
                self.firefly.images[self.firefly.frame],
                (self.config.cell_size * 3, self.config.cell_size * 3)
            )
            img_rect = img.get_rect(center=(self.width // 4, strip_top - 50))
            self.screen.blit(img, img_rect)

    def draw(self):
        self.screen.fill(self.config.colors['background'])

        if self.current_state == self.MENU:
            self._draw_menu()
        elif self.current_state == self.GAME:
            self._draw_game(show_player=True)
        elif self.current_state == self.SLIDESHOW:
            self._draw_slideshow()
        elif self.current_state == self.END:
            self._draw_end()

        pygame.display.flip()

    def _draw_menu(self):
        self.screen.blit(self.menu_background, (0, 0))

        title = self.title_font.render("Firefly", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(title, title_rect)

        prompt = self.text_font.render("Press ENTER to start", True, (200, 200, 200))
        prompt_rect = prompt.get_rect(center=(self.width // 2, self.height * 2 // 3))
        self.screen.blit(prompt, prompt_rect)

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

        darkness = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        darkness.fill((0, 0, 0, 250))

        cell_size = self.config.cell_size
        px = self.player.grid_x * cell_size + cell_size // 2
        py = self.player.grid_y * cell_size + cell_size // 2

        fx, fy = self.firefly.pos
        fx += cell_size // 2
        fy += cell_size // 2

        darkness.blit(self.player_light_mask, self.player_light_mask.get_rect(center=(px, py)),
                      special_flags=pygame.BLEND_RGBA_SUB)

        darkness.blit(self.firefly_light_mask, self.firefly_light_mask.get_rect(center=(fx, fy)),
                      special_flags=pygame.BLEND_RGBA_SUB)

        self.screen.blit(darkness, (0, 0))

    def _draw_end(self):
        self.screen.blit(self.end_background, (0, 0))

        text = self.title_font.render("The End", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 4))
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
