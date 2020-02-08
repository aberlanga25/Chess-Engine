from engine.board.BoardUtils import *


def getBoard(Move):
    return isThreatenedBoardImmediate(Move.board)


def getAttack(Move):
    return Move.isAttack


def getCastling(Move):
    return Move.isCastling


def getPieceValue(Move):
    return Move.movedPiece.pieceType.pieceValue()


class MoveSorter:

    @staticmethod
    def sort(moves):
        return sorted(sorted(sorted(sorted(moves, key=getBoard), key=getAttack), key=getCastling), key=getPieceValue)