from abc import ABC, abstractmethod
from typing import List

from engine.classic.board.MoveTransition import MoveTransition
from engine.classic.board.Move import MoveStatus
from engine.classic.player import Alliance


class Player(ABC):
    def __init__(self, board, legalMoves, opponentMoves):
        self.board = board
        self.playerKing = self.establishKing
        self._isInCheck = len(self._calculateAttacksOnTile(self.playerKing.piecePosition, opponentMoves)) != 0
        self.legalMoves = legalMoves + self.calculateKingCastles(legalMoves, opponentMoves)
        self.opponetMoves = opponentMoves

    @property
    def establishKing(self):
        for piece in self.activePieces:
            if piece.pieceType.isKing():
                return piece
        raise Exception("Not allowed board")

    def isMoveLegal(self, move):
        return move in self.legalMoves

    @property
    def isInCheck(self):
        return self._isInCheck

    @property
    def isInCheckMate(self):
        return self._isInCheck and not self.hasEscapeMoves()

    @property
    def isInStaleMate(self):
        return not self._isInCheck and not self.hasEscapeMoves()

    @property
    def isCastled(self):
        return self.playerKing.isCastled

    def makeMove(self, move):
        if not self.isMoveLegal(move):
            return MoveTransition(self.board, move, MoveStatus.Illegal_Move)
        transitionBoard = move.execute()

        kingAttacks = self._calculateAttacksOnTile(transitionBoard.currentPlayer.getOpponent.playerKing.piecePosition,
                                                   transitionBoard.currentPlayer.legalMoves)

        if len(kingAttacks) != 0:
            return MoveTransition(self.board, move, MoveStatus.Leaves_Player_Check)

        return MoveTransition(transitionBoard, move, MoveStatus.Done)

    @property
    @abstractmethod
    def activePieces(self) -> List:
        pass

    @property
    @abstractmethod
    def alliance(self) -> Alliance.Alliance:
        pass

    @property
    @abstractmethod
    def getOpponent(self):
        pass

    @abstractmethod
    def calculateKingCastles(self, legalMoves, opponentsLegalMoves):
        pass

    @staticmethod
    def _calculateAttacksOnTile(coordinate, moves):
        attackMoves = []
        for move in moves:
            if coordinate == move.destinationCoordinate:
                attackMoves.append(move)
        return attackMoves

    def hasEscapeMoves(self):
        for move in self.legalMoves:
            transition = self.makeMove(move)
            if transition.moveStatus.isDone():
                return True
        return False
