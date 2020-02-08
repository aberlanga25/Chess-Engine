def isValidTileCoordinate(coordinate) -> bool:
    return 0 <= coordinate < 64


def inFirstColumn(coordinate) -> bool:
    return coordinate in range(0, 57, 8)


def inSecondColumn(coordinate) -> bool:
    return coordinate in range(1, 58, 8)


def inThirdColumn(coordinate) -> bool:
    return coordinate in range(2, 59, 8)


def inFourColumn(coordinate) -> bool:
    return coordinate in range(3, 60, 8)


def inFiveColumn(coordinate) -> bool:
    return coordinate in range(4, 61, 8)


def inSixColumn(coordinate) -> bool:
    return coordinate in range(5, 62, 8)


def inSevenColumn(coordinate) -> bool:
    return coordinate in range(6, 63, 8)


def inEightColumn(coordinate) -> bool:
    return coordinate in range(7, 64, 8)


def inFirstRow(coordinate) -> bool:
    return coordinate in range(0, 8)


def inSecondRow(coordinate) -> bool:
    return coordinate in range(8, 16)


def inThirdRow(coordinate) -> bool:
    return coordinate in range(16, 24)


def inFourRow(coordinate) -> bool:
    return coordinate in range(24, 32)


def inFiveRow(coordinate) -> bool:
    return coordinate in range(32, 40)


def inSixRow(coordinate) -> bool:
    return coordinate in range(40, 48)


def inSevenRow(coordinate) -> bool:
    return coordinate in range(48, 56)


def inEightRow(coordinate) -> bool:
    return coordinate in range(56, 64)


def getCoordinateAtPosition(pos) -> int:
    return _position.get(pos)


def isEndGame(board):
    return board.currentPlayer.isInCheckMate or board.currentPlayer.isInStaleMate


def isThreatenedBoardImmediate(board) -> bool:
    return board.whitePlayer.isInCheck or board.blackPlayer.isInCheck


def getPositionAtCoordinate(coordinate) -> str:
    return _algebraic[coordinate]


_algebraic = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]


def _initiPosition():
    p = {}
    for i in range(64):
        p[_algebraic[i]] = i
    return p


_position = _initiPosition()
