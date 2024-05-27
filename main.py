from src import Interface


class CGL:
    def __init__(self) -> None:
        self.interface = Interface()
        self.interface.show()


if __name__ == "__main__":
    CGL()
