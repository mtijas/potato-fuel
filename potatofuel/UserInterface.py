import time
from datetime import timedelta


class UserInterface:
    def __init__(self, config, engine, screen):
        self._config = config
        self._engine = engine
        self._screen = screen

    def start(self):
        """Start user interface"""
        self._screen.start()
        self.manage_windows()
        try:
            self.main_loop()
        finally:
            self._screen.stop()

    def main_loop(self):
        """User interface main loop
        # 
        # Handles keystrokes, updates UI and runs timer engine
        """
        while True:
            c = self._screen.get_char("statusline")
            if c == ord('q'):
                break
            elif c == ord('h'):
                self.show_help()

            if self._screen.is_resized:
                self.manage_windows()
                self._screen.ack_resize()

            time.sleep(0.2)

    

    def manage_windows(self):
        """Create, remove and resize windows"""
        lines, cols = self._screen.screen_size()
        content_width = cols

        if cols >= 50:
            content_width = round(cols * 0.6)
            sidebar_width = cols - content_width
            self._screen.resize_or_create_window(
                "sidebar", lines, sidebar_width, 0, content_width)
            self._screen.move_window("sidebar", 0, content_width)
        else:
            self._screen.remove_window("sidebar")

        if lines >= 6:
            self._screen.resize_or_create_window(
                "content", lines-3, content_width, 3, 0)
            self._screen.resize_or_create_window(
                "statusline", 3, content_width, 0, 0)
        else:
            self._screen.remove_window("content")
            self._screen.resize_or_create_window(
                "statusline", 1, content_width, 0, 0)

        self._screen.set_nodelays()
        self.prepopulate_sidebar()
        self.prepopulate_content()

    def show_help(self):
        """Show help inside content window"""
        self._screen.erase_window("content")
        self._screen.add_str("content", 1, 2, "Potato Timer Help")
        self._screen.add_str("content", 3, 2, "s: Start and stop timers")
        self._screen.add_str("content", 4, 2, "n: Next timer (starts from 0)")
        self._screen.add_str("content", 5, 2, "r: Reset current timer")
        self._screen.add_str("content", 6, 2, "h: Show/hide help")
        self._screen.add_str("content", 7, 2, "q: Quit")

        self._screen.add_str(
            "content", 9, 2, "For more help and config examples please consult:")
        self._screen.add_str(
            "content", 10, 2, "github.com/mtijas/potato-timer")
        self._screen.add_str("content", 12, 2, "(c) Markus Ijäs")

        self._screen.refresh_window("content")

        while True:
            c = self._screen.get_char("content")
            if c == ord('h'):
                break
            time.sleep(0.5)
        self._screen.erase_window("content")
        self.prepopulate_content()
