import fusionengine.files.window as window
from fusionengine.files.imports import *
import fusionengine.files.shape as shape


class Draw:
    def draw_line(
        self, window: window._CustomRenderer, x1: int, y1: int, x2: int, y2: int, color: tuple
    ) -> None:
        """Draws a line on the screen."""
        pg.draw.line(window.window, color, (x1, y1), (x2, y2))

    def draw_line_rect(
        self,
        window: window._CustomRenderer,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple,
    ) -> None:
        """Draws a rectangle that exists of lines on the screen."""
        rdr = window.window
        pg.draw.line(rdr, color, (x, y), (x + width, y))
        pg.draw.line(rdr, color, (x, y + height), (x + width, y + height))
        pg.draw.line(rdr, color, (x, y), (x, y + height))
        pg.draw.line(rdr, color, (x + width, y), (x + width, y + height))

    def draw_rect(
        self,
        window: window._CustomRenderer,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple,
    ) -> None:
        """Draws a rectangle on the screen."""
        s = pg.Surface((width, height), pg.SRCALPHA)
        s.fill((color[0], color[1], color[2], color[3]))
        window.window.blit(s, (x, y))

    def draw_own_rect(self, window: window._CustomRenderer, rect: shape._CustomShape) -> None:
        """Draws your rectangle on the screen."""
        pg.draw.rect(window.window, rect.color, rect.rect)

    def set_background_color(self, window: window._CustomRenderer, color: tuple) -> None:
        """Sets the background color of the screen."""
        s = pg.Surface((window.width, window.height), pg.SRCALPHA)
        s.fill(color)
        window.window.blit(s, (0, 0))

    def draw_arbitrary_polygon_outline(
        self,
        window: window._CustomRenderer,
        corners: tuple[tuple[int, int]],
        color: tuple[int, int, int, int],
    ) -> None:
        """Draw an arbitrary polygon outline.
        WARNING: This will lag the game more and more as the number of corners increase, as this is an O(n)/call function.
        """
        for i, (x1, y1) in enumerate(corners[:-1]):  # need to exclude last corner for IndexError
            x2, y2 = corners[i + 1]  # tuple unpacking
            self.draw_line(window, x1, y1, x2, y2, color)

    def set_pixel(self, window: window._CustomRenderer, x, y, color):
        window.window.set_at((x, y), color)
