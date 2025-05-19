import os
import configparser


class ConfigManager:
    def __init__(self, config_path='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    @property
    def screen_size(self):
        return (self.config.getint('Graphics', 'screen_width'),
                self.config.getint('Graphics', 'screen_height'))

    @property
    def cell_size(self):
        return self.config.getint('Graphics', 'cell_size')

    @property
    def fps(self):
        return self.config.getint('Graphics', 'fps')

    @property
    def images_path(self):
        return self.config.get('Paths', 'images')

    @property
    def sounds_path(self):
        return self.config.get('Paths', 'sounds')

    @property
    def colors(self):
        return {
            'background': eval(self.config.get('Colors', 'background')),
            'wall': eval(self.config.get('Colors', 'wall')),
            'player': eval(self.config.get('Colors', 'player'))
        }

    @property
    def move_cooldown(self):
        return self.config.getfloat('Game', 'move_cooldown')

    @property
    def initial_level(self):
        return self.config.getint('Game', 'initial_level')

    @property
    def total_levels(self):
        return self.config.getint('Game', 'total_levels')

    def get_image_path(self, filename):
        return os.path.join(self.images_path, filename)

    def get_sound_path(self, filename):
        return os.path.join(self.sounds_path, filename)

    def get_level_path(self, level_num):
        return os.path.join(self.config.get('Paths', 'levels'), f"level{level_num}.txt")

    def get_font_path(self, filename):
        font_dir = os.path.join(os.path.dirname(self.images_path), "fonts")
        font_path = os.path.join(font_dir, filename)
        if os.path.exists(font_path):
            return font_path
        return os.path.join(self.images_path, filename)

    @property
    def firefly_animation_delay(self):
        return self.config.getfloat('Firefly', 'animation_delay')

    @property
    def firefly_move_delay(self):
        return self.config.getfloat('Firefly', 'move_delay')

    @property
    def final_image_path(self):
        return os.path.join(self.images_path, self.config.get('Paths', 'final_image'))
