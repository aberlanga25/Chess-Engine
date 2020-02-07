from enum import Enum


class BoardDirection(Enum):
    NORMAL = "N"
    FLIPPED = "F"

    def traverse(self, boardTiles: list):
        return {
            self.NORMAL: boardTiles,
            self.FLIPPED: boardTiles[::-1]
        }.get(self)

    def opposite(self):
        return {
            self.NORMAL: self.FLIPPED,
            self.FLIPPED: self.NORMAL
        }.get(self)
