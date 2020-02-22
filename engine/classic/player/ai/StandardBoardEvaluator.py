from engine.classic.player.ai.BoardEvaluator import BoardEvaluator
from engine.classic.board import Board
from engine.classic.player import Player
from engine.classic.piece import Piece


class StandardBoardEvaluator(BoardEvaluator):

    def evaluate(self, board: Board.Board, depth: int) -> int:
        return self.scorePlayer(board.whitePlayer, depth) - self.scorePlayer(board.blackPlayer, depth)

    def scorePlayer(self, player: Player.Player, depth: int) -> int:
        return self.pieceValue(player) + self.check(player) + self.checkMate(player, depth)

    @staticmethod
    def mobility(player: Player.Player) -> int:
        return int((len(player.legalMoves) * 100) / len(player.getOpponent.legalMoves)) * 2

    @staticmethod
    def attacks(player: Player.Player) -> int:
        attackScore = 0
        for move in player.legalMoves:
            if move.isAttack:
                movedPiece: Piece.Piece = move.movedPiece
                attackedPiece: Piece.Piece = move.attackedPiece
                if movedPiece.pieceType.pieceValue() <= attackedPiece.pieceType.pieceValue():
                    attackScore += 1
        return attackScore * 2

    @staticmethod
    def pieceValue(player: Player.Player) -> int:
        pieceValueScore = 0
        numBishops = 0
        for piece in player.activePieces:
            pieceValueScore += piece.pieceType.pieceValue()
            if piece.pieceType.isBishop():
                numBishops += 1
        return pieceValueScore + (50 if numBishops == 2 else 0)

    @staticmethod
    def check(player: Player.Player) -> int:
        return 20 if player.getOpponent.isInCheck else 0

    def checkMate(self, player: Player.Player, depth: int) -> int:
        return 100000 * self.depthBonus(depth) if player.getOpponent.isInCheckMate else 0

    @staticmethod
    def depthBonus(depth: int) -> int:
        return 1 if depth == 0 else 100 * depth

    @staticmethod
    def castled(player: Player.Player) -> int:
        return 40 if player.isCastled else 0
