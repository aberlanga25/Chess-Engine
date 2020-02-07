from engine.piece.Piece import Piece
from engine.piece.Queen import Queen
from engine.board import BoardUtils
from engine.board.Move import PawnMove, PawnJump, PawnAttackMove, PawnEnPassant, PawnPromotion
from engine.piece.PieceType import PieceType

from typing import List


class Pawn(Piece):
    _moves = [8, 16, 7, 9]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self._pieceType = PieceType.PAWN

    def calculateLegalMoves(self, board) -> List:
        legalMoves = []

        for candidOffset in self._moves:
            candidDest: int = self.piecePosition + (candidOffset * self.pieceAlliance.get_direction())

            if not BoardUtils.isValidTileCoordinate(candidDest):
                continue

            if candidOffset == 8 and not board.tile(candidDest).isTileOccupied():
                if self.pieceAlliance.isPawnPromotionSquare(candidDest):
                    legalMoves.append(PawnPromotion(PawnMove(board, self, candidDest)))
                else:
                    legalMoves.append(PawnMove(board, self, candidDest))

            elif candidOffset == 16 and self.isFirstMove() and (
                    (BoardUtils.inSecondRow(self.piecePosition) and self.pieceAlliance.isBlack())
                    or (BoardUtils.inSevenRow(self.piecePosition) and self.pieceAlliance.isWhite())):
                behindCandidateCoord = self.piecePosition + (self.pieceAlliance.get_direction() * 8)
                if not board.tile(behindCandidateCoord).isTileOccupied() and not board.tile(
                        candidDest).isTileOccupied():
                    legalMoves.append(PawnJump(board, self, candidDest))

            elif candidOffset == 7 and not (
                    (BoardUtils.inEightColumn(self.piecePosition) and self.pieceAlliance.isWhite())
                    or (BoardUtils.inFirstColumn(self.piecePosition) and self.pieceAlliance.isBlack())):
                if board.tile(candidDest).isTileOccupied():
                    pieceOnCandid = board.tile(candidDest).pieceOnTile
                    if pieceOnCandid.pieceAlliance != self.pieceAlliance:
                        if self.pieceAlliance.isPawnPromotionSquare(candidDest):
                            legalMoves.append(PawnPromotion(PawnAttackMove(board, self, candidDest, pieceOnCandid)))
                        else:
                            legalMoves.append(PawnAttackMove(board, self, candidDest, pieceOnCandid))
                elif board.enPassantPawn is not None:
                    if board.enPassantPawn.piecePosition == self.piecePosition + (
                            self.pieceAlliance.get_direction() * - 1):
                        pieceOnCandid = board.enPassantPawn
                        if self.pieceAlliance != pieceOnCandid.pieceAlliance:
                            legalMoves.append(PawnEnPassant(board, self, candidDest, pieceOnCandid))

            elif candidOffset == 9 and not (
                    (BoardUtils.inEightColumn(self.piecePosition) and self.pieceAlliance.isBlack())
                    or (BoardUtils.inFirstColumn(self.piecePosition) and self.pieceAlliance.isWhite())):
                if board.tile(candidDest).isTileOccupied():
                    pieceOnCandid = board.tile(candidDest).pieceOnTile
                    if pieceOnCandid.pieceAlliance != self.pieceAlliance:
                        if self.pieceAlliance.isPawnPromotionSquare(candidDest):
                            legalMoves.append(PawnPromotion(PawnAttackMove(board, self, candidDest, pieceOnCandid)))
                        else:
                            legalMoves.append(PawnAttackMove(board, self, candidDest, pieceOnCandid))
                elif board.enPassantPawn is not None:
                    if board.enPassantPawn.piecePosition == self.piecePosition - (
                            self.pieceAlliance.get_direction() * - 1):
                        pieceOnCandid = board.enPassantPawn
                        if self.pieceAlliance != pieceOnCandid.pieceAlliance:
                            legalMoves.append(PawnEnPassant(board, self, candidDest, pieceOnCandid))

        return legalMoves

    def movePiece(self, move):
        return Pawn(move.destinationCoordinate, move.movedPiece.pieceAlliance)

    @property
    def promotionPiece(self):
        return Queen(self.piecePosition, self.pieceAlliance)