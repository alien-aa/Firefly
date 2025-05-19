import pygame
import os
from config import ConfigManager
from core.game import Game


def main():
    pygame.init()
    config = ConfigManager('config.ini')

    # Установка иконки окна
    icon_path = config.get_image_path("firefly_0.png")
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
