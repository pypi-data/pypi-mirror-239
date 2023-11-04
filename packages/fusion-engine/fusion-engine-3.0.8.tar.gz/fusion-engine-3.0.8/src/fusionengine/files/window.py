import fusionengine.files.debug as debugfe
from fusionengine.files.imports import *


class _CustomRenderer:
    def __init__(
        self, window: pg.Surface, title: str, width: int, height: int, manager
    ) -> None:
        """A class that creates a new custom renderer. (Not for the user)

        Args:
            window (sdl2.SDL_CreateWindow): An created sdl2 window
        """
        self.window = window

        self.title = title
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

        self.manager = manager


class Window:
    def __init__(self) -> None:
        """A class that contains all the window functions."""
        self._running = False
        self._fps = 60
        self._quittable = True
        self.clock = pg.time.Clock()

    def new_window(self, title: str, width: int, height: int) -> _CustomRenderer:
        """Creates a new window.

        Args:
            title (str): Your window title
            width (int): Your window width
            height (int): Your window height

        Returns:
            window: Custom window class with all you need features
        """
        try:
            window_window = pg.display.set_mode((width, height))
            pg.display.set_caption(title)

            self.manager = gui.UIManager((800, 600))

            programIcon = pg.image.load(debugfe.DebugFiles().DEBUGIMAGE)
            pg.display.set_icon(programIcon)

            self._running = True
            self.window = _CustomRenderer(
                window_window, title, width, height, self.manager
            )

        except Exception:
            print("Error: Can't create a window.")

        return self.window

    def change_icon(self, image_path):
        """Changes icon

        Args:
            Icon_Path (str): Path to your icon

        """

        programIcon = pg.image.load(image_path)
        pg.display.set_icon(programIcon)

    def loop(self, your_loop) -> None:
        """A while loop decorator function.

        Args:
            your_loop (callable): Your main loop function
        """
        while self.running(self.window):
            your_loop()

    def running(self, window: _CustomRenderer) -> bool:
        """Returns if the window is running. Used for the main loop.

        Args:
            window: Your window

        Returns:
            bool: returns true if the window is running else false
        """
        self._refresh(window)
        return self._running

    def set_fps(self, fps: int) -> None:
        """Sets the desired frames per second for the game loop.

        Args:
            fps (int): The desired frames per second
        """
        self._fps = fps

    def force_quit(self) -> None:
        """Force quits the window.
        Specifically, stops and deletes window.
        Args:
            window: Your window
        """
        if self._quittable:
            self._running = False
            del self.window

    def toggle_quittable(self) -> None:
        """Toggles whether the window is quittable."""
        self._quittable = not self._quittable

    def _refresh(self, window: _CustomRenderer) -> None:
        """Does all things for refreshing window. (Not for the user)

        Args:
            window: Your window
        """

        self.DELTATIME = self.clock.tick(self._fps)

        for event in pg.event.get():
            if event.type == pg.QUIT and self._quittable:
                self._running = False

            self.manager.process_events(event)

        self.manager.update(self.DELTATIME)
        self.manager.draw_ui(window.window)

        pg.display.flip()

        window.window.fill((0, 0, 0))
