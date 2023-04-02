from constants import CASE_SIZE


class Collision:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class RockCollision(Collision):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-x + CASE_SIZE, -y + CASE_SIZE, CASE_SIZE + 10, CASE_SIZE * 0.5 - 30)

class WallCollision(Collision):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(-x + CASE_SIZE, -y + CASE_SIZE, width, 1)

class TreeCollision(Collision):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-x + CASE_SIZE, -y + CASE_SIZE, CASE_SIZE * 0.5, -(CASE_SIZE // 2))