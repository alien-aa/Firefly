import pygame
import sys
from config import ConfigManager
from core.game import Game

def main():
    pygame.init()
    pygame.mixer.init()

    config = ConfigManager()
    pygame.display.set_caption("Firefly")
    screen = pygame.display.set_mode(config.screen_size)


    # Load icon (from assets/images)
    try:
        icon = pygame.image.load(config.get_image_path("firefly_0.png")).convert_alpha()
        pygame.display.set_icon(icon)
    except Exception:
        print("Icon not found, using default window icon.")

    game = Game(config)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
