from typing import final, Final
from abc import ABC, abstractmethod
#from immutablecollections import ImmutableDict
from engine.classic.piece.Piece import Piece


def _createAllEmptyTiles() -> dict:
    emptyTile = {}
    for i in range(64):
        emptyTile[i] = EmptyTile(i)
    return emptyTile


class _Tile(ABC):
    _tileCoordinate: Final[int]

    def __init__(self, tileCoordinate) -> None:
        self._tileCoordinate = tileCoordinate


    @abstractmethod
    def isTileOccupied(self) -> bool:
        pass

    @property
    @abstractmethod
    def pieceOnTile(self) -> Piece:
        pass

    @property
    def tileCoordinate(self) -> int:
        return self._tileCoordinate


@final
class EmptyTile(_Tile):
    def __init__(self, coordinate):
        super().__init__(coordinate)

    def isTileOccupied(self) -> bool:
        return False

    def pieceOnTile(self) -> None:
        return None

    def __str__(self):
        return "-"


@final
class OccupiedTile(_Tile):
    _pieceOnTile: Final[Piece]

    def __init__(self, coordinate, piece) -> None:
        super().__init__(coordinate)
        self._pieceOnTile = piece

    def isTileOccupied(self) -> bool:
        return True

    @property
    def pieceOnTile(self) -> Piece:
        return self._pieceOnTile

    def __str__(self):
        return str(self._pieceOnTile.pieceType.value)


_EMPTY_TILES: Final[dict] = _createAllEmptyTiles()


def createTile(tileCoordinate, piece) -> _Tile:
    return OccupiedTile(tileCoordinate, piece) if piece else _EMPTY_TILES.get(tileCoordinate)
