from enum import Enum

from engine.board.BoardUtils import *


class Alliance(Enum):
    White = "W"
    Black = "B"

    def get_direction(self) -> int:
        return {
            Alliance.White: -1,
            Alliance.Black: 1
        }.get(self)

    def choosePlayer(self, whitePlayer, blackPlayer):
        return {
            Alliance.White: whitePlayer,
            Alliance.Black: blackPlayer
        }.get(self)

    def isBlack(self):
        return {
            Alliance.White: False,
            Alliance.Black: True
        }.get(self)

    def isWhite(self):
        return {
            Alliance.White: True,
            Alliance.Black: False
        }.get(self)

    def isPawnPromotionSquare(self, position):
        return {
            Alliance.Black: inEightRow(position),
            Alliance.White: inFirstRow(position)
        }.get(self)
