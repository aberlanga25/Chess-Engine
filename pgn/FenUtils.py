from engine.classic.player.Alliance import Alliance
from engine.classic.board.Board import BoardBuilder
from engine.classic.piece.Pawn import Pawn
from engine.classic.piece.King import King
from engine.classic.piece.Bishop import Bishop
from engine.classic.piece.Knight import Knight
from engine.classic.piece.Rook import Rook
from engine.classic.piece.Queen import Queen
from engine.classic.board import Board
from engine.classic.board.BoardUtils import *


def createGameFromFen(fenString: str) -> Board.Board:
    return _parseFEN(fenString)


def _calculateTextBoard(board: Board.Board) -> str:
    s = ""
    x = [8,17,26,35,44,53,62]
    for i in range(64):
        if i in x:
            tileText = "/"
        else:
            tileText = str(board.tile(i).pieceOnTile) \
                if board.tile(i).pieceOnTile.pieceAlliance.isWhite() else str(board.tile(i).pieceOnTile).lower() \
                if board.tile(i).isTileOccupied() else "-"
        s += tileText
    return s.replace("--------", "8").replace("-------", "7").replace("------", "6").replace("-----", "5")\
        .replace("----", "4").replace("---", "3").replace("--", "2").replace("-", "1")


def _calculateCurrentPlayerText(board: Board.Board) -> str:
    return board.currentPlayer.alliance.value


def _calculateCastleText(board: Board.Board) -> str:
    s = ""
    return s


def _calculateEnPassantSquare(board: Board.Board) -> str:
    enPassant = board.enPassantPawn
    if enPassant is None:
        return getPositionAtCoordinate(enPassant.piecePosition + 8 * enPassant.pieceAlliance.get_direction() * -1)
    return "-"


def createFENFromGame(board: Board.Board) -> str:
    return _calculateTextBoard(board) + " " + _calculateCurrentPlayerText(board) + " " + _calculateCastleText(board) + " " \
           + _calculateEnPassantSquare(board) + " 0 1"


def _moveMaker(moveMaker: str) -> Alliance:
    if moveMaker == 'w':
        return Alliance.White
    elif moveMaker == 'b':
        return Alliance.Black


def _parseFEN(fenString: str) -> Board.Board:
    fenString.strip()
    fenPartition = fenString.split()
    builder = BoardBuilder()
    whiteKingSideCastle = _whiteKingCastle(fenPartition[2])
    whiteQueengSideCastle = _whiteQueenCastle(fenPartition[2])
    blackKingSideCastle = _blackKingCastle(fenPartition[2])
    blackQueenSideCastle = _blackQueenCastle(fenPartition[2])

    gameConfig: str = fenPartition[0]
    boardTiles: list = list(gameConfig.replace("/", "").replace("8", "--------").replace("7", "-------").replace("6", "------")
                            .replace("5", "-----").replace("4", "----").replace("3", "---")
                            .replace("2", "--").replace("1", "-"))
    i = 0
    while i < len(boardTiles):
        if boardTiles[i] == 'r':
            builder.setPiece(Rook(i, Alliance.Black))
            i += 1
        elif boardTiles[i] == 'n':
            builder.setPiece(Knight(i, Alliance.Black))
            i += 1
        elif boardTiles[i] == 'b':
            builder.setPiece(Bishop(i, Alliance.Black))
            i += 1
        elif boardTiles[i] == 'q':
            builder.setPiece(Queen(i, Alliance.Black))
            i += 1
        elif boardTiles[i] == 'k':
            kin = King(i, Alliance.Black)
            kin.setCastled(not blackKingSideCastle and not blackQueenSideCastle)
            builder.setPiece(kin)
            i += 1
        elif boardTiles[i] == 'p':
            builder.setPiece(Pawn(i, Alliance.Black))
            i += 1
        elif boardTiles[i] == 'R':
            builder.setPiece(Rook(i, Alliance.White))
            i += 1
        elif boardTiles[i] == 'N':
            builder.setPiece(Knight(i, Alliance.White))
            i += 1
        elif boardTiles[i] == 'B':
            builder.setPiece(Bishop(i, Alliance.White))
            i += 1
        elif boardTiles[i] == 'Q':
            builder.setPiece(Queen(i, Alliance.White))
            i += 1
        elif boardTiles[i] == 'K':
            kin = King(i, Alliance.White)
            kin.setCastled(not whiteKingSideCastle and not whiteQueengSideCastle)
            builder.setPiece(kin)
            i += 1
        elif boardTiles[i] == 'P':
            builder.setPiece(Pawn(i, Alliance.White))
            i += 1
        elif boardTiles[i] == '-':
            i += 1
    builder.setMoveMaker(_moveMaker(fenPartition[1]))
    return builder.build()


def _whiteKingCastle(fenString: str) -> bool:
    return 'K' in fenString


def _whiteQueenCastle(fenString: str) -> bool:
    return 'Q' in fenString


def _blackKingCastle(fenString: str) -> bool:
    return 'k' in fenString


def _blackQueenCastle(fenString: str) -> bool:
    return 'q' in fenString
