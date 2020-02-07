from abc import ABC
from enum import Enum

from engine.board import Board
from engine.piece import Piece, Rook
from engine.board.BoardUtils import *


class Move(ABC):
    _destinationCoordinate: int

    def __init__(self, board, movedPiece, destinationCoordinate):
        self.board: Board.Board = board
        self._movedPiece: Piece.Piece = movedPiece
        self._destinationCoordinate = destinationCoordinate

    def __hash__(self):
        result = 1
        result = 31 * result + self.destinationCoordinate
        result = 31 * result + self.movedPiece.__hash__()
        return result

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.currentCoordinate == other.currentCoordinate \
               and self.destinationCoordinate == other.destinationCoordinate and self.movedPiece == other.movedPiece

    def __ne__(self, other):
        return not self == other

    @property
    def destinationCoordinate(self):
        return self._destinationCoordinate

    @property
    def currentCoordinate(self):
        return self._movedPiece.piecePosition

    @property
    def movedPiece(self):
        return self._movedPiece

    @property
    def isAttack(self):
        return False

    @property
    def isCastling(self):
        return False

    @property
    def attackedPiece(self):
        return None

    def execute(self):
        builder = Board.BoardBuilder()
        for piece in self.board.currentPlayer.activePieces:
            if not self.movedPiece == piece:
                builder.setPiece(piece)
        for piece in self.board.currentPlayer.getOpponent.activePieces:
            builder.setPiece(piece)
        builder.setPiece(self.movedPiece.movePiece(self))
        builder.setMoveMaker(self.board.currentPlayer.getOpponent.alliance)

        return builder.build()


class MajorMove(Move):
    def __init__(self, board, piece, coordinate):
        super().__init__(board, piece, coordinate)

    def __str__(self):
        return self.movedPiece.pieceType.value + getPositionAtCoordinate(self.destinationCoordinate)


class AttackMove(Move):
    def __init__(self, board, piece, coordinate, attackedPiece):
        super().__init__(board, piece, coordinate)
        self._attackedPiece = attackedPiece

    def __hash__(self):
        return self._attackedPiece.__hash__() + super().__hash__()

    def __eq__(self, other):
        if not isinstance(other, AttackMove):
            return False
        return super().__eq__(other) and self.attackedPiece == other.attackedPiece

    def __str__(self):
        return self.movedPiece.pieceType.value + "x" + getPositionAtCoordinate(self.destinationCoordinate)

    @property
    def attackedPiece(self):
        return self._attackedPiece

    def isAttack(self):
        return True


class PawnMove(Move):
    def __init__(self, board, piece, coordinate):
        super().__init__(board, piece, coordinate)

    def __str__(self):
        return getPositionAtCoordinate(self.destinationCoordinate)


class PawnAttackMove(AttackMove):
    def __init__(self, board, piece, coordinate, attackedPiece):
        super().__init__(board, piece, coordinate, attackedPiece)

    def __str__(self):
        return getPositionAtCoordinate(self.movedPiece.piecePosition)[:1] + "x" + getPositionAtCoordinate(
            self.destinationCoordinate)


class PawnEnPassant(PawnAttackMove):
    def __init__(self, board, piece, coordinate, attackedPiece):
        super().__init__(board, piece, coordinate, attackedPiece)

    def execute(self):
        builder = Board.BoardBuilder()
        for piece in self.board.currentPlayer.activePieces:
            if piece != self.movedPiece:
                builder.setPiece(piece)
        for piece in self.board.currentPlayer.getOpponent.activePieces:
            if piece != self.attackedPiece:
                builder.setPiece(piece)
        builder.setPiece(self.movedPiece.movePiece(self))
        builder.setMoveMaker(self.board.currentPlayer.getOpponent.alliance)
        return builder.build()


class PawnJump(Move):
    def __init__(self, board, piece, coordinate):
        super().__init__(board, piece, coordinate)

    def execute(self):
        builder = Board.BoardBuilder()

        for piece in self.board.currentPlayer.activePieces:
            if self.movedPiece != piece:
                builder.setPiece(piece)
        for piece in self.board.currentPlayer.getOpponent.activePieces:
            builder.setPiece(piece)
        movedPawn = self.movedPiece.movePiece(self)
        builder.setPiece(movedPawn)
        builder.setEnPassantPawn(movedPawn)
        builder.setMoveMaker(self.board.currentPlayer.getOpponent.alliance)
        return builder.build()

    def __str__(self):
        return getPositionAtCoordinate(self.destinationCoordinate)


class CastleMove(Move):
    def __init__(self, board, piece, coordinate, castleRook, castleRookStart, castleRookDest):
        super().__init__(board, piece, coordinate)
        self._castleRook: Piece.Piece = castleRook
        self.castleRookStart: int = castleRookStart
        self.castleRookDest: int = castleRookDest

    @property
    def castleRook(self):
        return self._castleRook

    def isCastling(self):
        return True

    def execute(self):
        builder = Board.BoardBuilder()

        for piece in self.board.currentPlayer.activePieces:
            if self.movedPiece != piece and self.castleRook != piece:
                builder.setPiece(piece)
        for piece in self.board.currentPlayer.getOpponent.activePieces:
            builder.setPiece(piece)
        self.movedPiece.setCastled(True)
        builder.setPiece(self.movedPiece.movePiece(self))
        newRook = Rook.Rook(self.castleRookDest, self.castleRook.pieceAlliance)
        newRook.setFirstMove(False)
        builder.setPiece(newRook)
        builder.setMoveMaker(self.board.currentPlayer.getOpponent.alliance)
        return builder.build()


class KingSideCastleMove(CastleMove):
    def __init__(self, board, piece, coordinate, castleRook, castleRookStart, castleRookDest):
        super().__init__(board, piece, coordinate, castleRook, castleRookStart, castleRookDest)

    def __str__(self):
        return "O-O"


class QueenSideCastleMove(CastleMove):
    def __init__(self, board, piece, coordinate, castleRook, castleRookStart, castleRookDest):
        super().__init__(board, piece, coordinate, castleRook, castleRookStart, castleRookDest)

    def __str__(self):
        return "O-O-O"


class PawnPromotion(Move):
    def __init__(self, move):
        super().__init__(move.board, move.movedPiece, move.destinationCoordinate)
        self.decoratedMove = move
        self.promotedPawn = move.movedPiece

    def __hash__(self):
        return self.decoratedMove.__hash__() + (31 * self.promotedPawn.__hash__())

    def __eq__(self, other):
        return isinstance(other, PawnPromotion) and self.decoratedMove.__eq__(other)

    def __str__(self):
        return getPositionAtCoordinate(self.movedPiece.piecePosition) + "-" \
               + getPositionAtCoordinate(self.destinationCoordinate) + "=" + self.movedPiece.pieceAlliance.value + "Q"

    def execute(self):
        pawnMoveBoard = self.decoratedMove.execute()
        builder = Board.BoardBuilder()
        for piece in pawnMoveBoard.currentPlayer.activePieces:
            if self.promotedPawn != piece:
                builder.setPiece(piece)
        for piece in pawnMoveBoard.currentPlayer.getOpponent.activePieces:
            builder.setPiece(piece)
        builder.setPiece(self.promotedPawn.promotionPiece.movePiece(self))
        builder.setMoveMaker(pawnMoveBoard.currentPlayer.alliance)
        return builder.build()

    def isAttack(self):
        return self.decoratedMove.isAttack()

    @property
    def attackedPiece(self):
        return self.decoratedMove.attackedPiece


class NullMove(Move):
    def __init__(self):
        super().__init__(None, None, -1)

    def execute(self):
        raise Exception("Cannot execute Null Move")


class MoveFactory:

    @staticmethod
    def createMove(board, current, destination):
        for move in board.allLegalMoves:
            if move.currentCoordinate == current and move.destinationCoordinate == destination:
                return move
        return nullMove


nullMove = NullMove()


class MoveStatus(Enum):
    Done = True
    Illegal_Move = False
    Leaves_Player_Check = False

    def isDone(self):
        return {
            self.Done: True,
            self.Illegal_Move: False,
            self.Leaves_Player_Check: False
        }.get(self)
