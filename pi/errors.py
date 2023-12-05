class NoPathError(Exception):
    def __init__(self):
        super().__init__(f"No possible path found")

class IllegalStartPositionError(Exception):
    def __init__(self, position):
        super().__init__(
            f"the position {position} is already occupied, kindly pick a better position"
        )

class QuitError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
