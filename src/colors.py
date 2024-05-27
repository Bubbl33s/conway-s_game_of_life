class Color:
    red: int
    green: int
    blue: int
    alpha: int
    channels: tuple[int, ...]

    def __init__(self, red: int, green: int, blue: int, alpha: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self.channels = (self.red, self.green, self.blue, self.alpha)

    # Setting instance color must be int
    def get_int(self) -> tuple[int, ...]:
        return self.channels

    # Setting configure color must be float
    def get_float(self) -> tuple[float, ...]:
        # Doesn't matter if it's a list or a tuple
        return tuple(c/1 for c in self.channels)

    # Colors are provided in 0-1 scale
    def get_normalized(self) -> list[float]:
        return list(c/255 for c in self.channels)

    def set_color(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue
        self.channels = (self.red, self.green, self.blue, self.alpha)


# INITIAL COLOR CONSTANTS
WHITE = Color(255, 255, 255, 255)
BLACK = Color(0, 0, 0, 255)
GRAY_CELL_BORDER = Color(40, 40, 40, 255)
TRANSPARENT = Color(0, 0, 0, 0)
