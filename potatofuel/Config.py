import yaml
from appdirs import AppDirs
from pathlib import Path


class Config:
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __init__(self, config_file=None):
        self._use_colors = True
        self._prefer_terminal_colors = False

        self._possible_files = [
            "~/.config/potatotimer/config.yml",
            "~/.potatotimer-config.yml",
        ]

        if config_file is not None:
            self._possible_files.insert(0, config_file)

        self.insert_xdg_conf_location()

        self._selected_config = self.find_config()
        if self._selected_config is not None:
            try:
                self.read_config()
            except:
                print(f'Error reading config: {self._selected_config}')
                print("Please check that the file is formatted correctly.")
                exit()

    def find_config(self):
        """Try to find config file"""
        for possibility in self._possible_files:
            p = Path(possibility)
            expanded = p.expanduser()
            """Older pythons than 3.8 might still throw an exception"""
            try:
                if expanded.is_file():
                    return expanded
            except:
                continue
        return None

    def insert_xdg_conf_location(self):
        """Insert XDG config file location"""
        dirs = AppDirs("potatotimer")
        xdg_config = dirs.user_config_dir
        p = Path(xdg_config).joinpath('config.yml')
        self._possible_files.insert(1, str(p))

    def read_config(self):
        """Load the config file"""
        with open(self._selected_config, 'r') as stream:
            settings_yaml = yaml.safe_load(stream)
            self.load_use_colors(settings_yaml)

    def load_use_colors(self, settings_yaml):
        """Try to load color use setting"""
        if "use_colors" in settings_yaml:
            if settings_yaml["use_colors"]:
                self._use_colors = True
            else:
                self._use_colors = False

        if "prefer_terminal_colors" in settings_yaml:
            if settings_yaml["prefer_terminal_colors"]:
                self._prefer_terminal_colors = True
            else:
                self._prefer_terminal_colors = False

    @property
    def selected_config(self):
        return self._selected_config

    @property
    def use_colors(self):
        return self._use_colors

    @property
    def prefer_terminal_colors(self):
        return self._prefer_terminal_colors
