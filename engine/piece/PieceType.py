from enum import Enum


class PieceType(Enum):
    PAWN = "p"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"

    def pieceValue(self):
        return {
            self.PAWN: 100,
            self.KNIGHT: 320,
            self.BISHOP: 320,
            self.ROOK: 500,
            self.QUEEN: 900,
            self.KING:20000
        }.get(self)

    def isRook(self):
        return {
            self.PAWN: False,
            self.KNIGHT: False,
            self.KING: False,
            self.BISHOP: False,
            self.ROOK: True,
            self.QUEEN: False,
        }.get(self)

    def isKing(self):
        return {
            self.PAWN: False,
            self.KNIGHT: False,
            self.KING: True,
            self.BISHOP: False,
            self.ROOK: False,
            self.QUEEN: False,
        }.get(self)


def getValue(Piece):
    return Piece.pieceType.pieceValue()