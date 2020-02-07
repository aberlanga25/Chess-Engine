from engine.player.Alliance import Alliance
from engine.piece.PieceType import PieceType

from abc import ABC, abstractmethod
from typing import List


class Piece(ABC):
    _piecePosition: int
    _pieceAlliance: Alliance
    _isFirstMove: bool

    def __init__(self, piecePosition, pieceAlliance):
        self._pieceAlliance = pieceAlliance
        self._piecePosition = piecePosition
        self._isFirstMove = True
        self._pieceType = None
        self._cachedHash = self.computeHashCode()

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.piecePosition == other.piecePosition and self.pieceAlliance == other.pieceAlliance \
               and self.isFirstMove == other.isFirstMove and self.pieceType == other.pieceType

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return self._cachedHash

    def __str__(self):
        return self.pieceType.value


    def computeHashCode(self):
        result = self.pieceType.__hash__()
        result = 31 * result + self.pieceAlliance.__hash__()
        result = 31 * result + self.piecePosition
        result = 31 * result + (1 if self.isFirstMove else 0)
        return result

    def isFirstMove(self):
        return self._isFirstMove

    def setFirstMove(self, option):
        self._isFirstMove = option

    @property
    def pieceType(self) -> PieceType:
        return self._pieceType

    @property
    def piecePosition(self) -> int:
        return self._piecePosition

    @property
    def pieceAlliance(self) -> Alliance:
        return self._pieceAlliance

    @abstractmethod
    def calculateLegalMoves(self, board) -> List:
        pass

    @abstractmethod
    def movePiece(self, move):
        pass
