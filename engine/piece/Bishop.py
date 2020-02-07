from engine.piece.Piece import Piece
from engine.piece.PieceType import PieceType
from engine.board import BoardUtils
from engine.board.Move import MajorMove, AttackMove
from typing import List

class Bishop(Piece):

    _moves = [-9, -7, 7, 9]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self._pieceType = PieceType.BISHOP

    def calculateLegalMoves(self, board) -> List:
        legalMoves = []

        for candidOffset in self._moves:
            candidDestination: int = self.piecePosition
            while BoardUtils.isValidTileCoordinate(candidDestination):
                if self.firstColumnExclusion(candidDestination, candidOffset) or\
                        self.eightColumnExclusion(candidDestination, candidOffset):
                    break

                candidDestination += candidOffset

                if BoardUtils.isValidTileCoordinate(candidDestination):
                    candidTile = board.tile(candidDestination)
                    if not candidTile.isTileOccupied():
                        legalMoves.append(MajorMove(board, self, candidDestination))
                    else:
                        pieceAtDestination = candidTile.pieceOnTile
                        pieceAtDestAlliance = pieceAtDestination.pieceAlliance
                        if pieceAtDestAlliance != self.pieceAlliance:
                            legalMoves.append(AttackMove(board, self, candidDestination, pieceAtDestination))
                        break

        return legalMoves

    @staticmethod
    def firstColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inFirstColumn(coordinate) and (future == -9 or future == 7)

    @staticmethod
    def eightColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inEightColumn(coordinate) and (future == -7 or future == 9)

    def movePiece(self, move):
        return Bishop(move.destinationCoordinate, move.movedPiece.pieceAlliance)
