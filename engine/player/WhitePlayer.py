from engine.player.Alliance import Alliance
from engine.player.Player import Player
from engine.board import Tile
from engine.board.Move import KingSideCastleMove, QueenSideCastleMove


class WhitePlayer(Player):
    def __init__(self, board, white, black):
        super().__init__(board, white, black)

    def __str__(self):
        return self.alliance.value

    @property
    def activePieces(self):
        return self.board.whitePieces

    @property
    def alliance(self):
        return Alliance.White

    @property
    def getOpponent(self) -> Player:
        return self.board.blackPlayer

    def calculateKingCastles(self, legalMoves, opponentsLegalMoves):
        kingCastles = []

        if self.playerKing.isFirstMove and not self.isInCheck:

            if not self.board.tile(61).isTileOccupied() and not self.board.tile(62).isTileOccupied():
                rookTile: Tile._Tile = self.board.tile(63)

                if rookTile.isTileOccupied() and rookTile.pieceOnTile.isFirstMove():

                    if len(self._calculateAttacksOnTile(61, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(62, opponentsLegalMoves)) ==0 \
                            and rookTile.pieceOnTile.pieceType.isRook:

                        kingCastles.append(KingSideCastleMove(self.board, self.playerKing, 62, rookTile.pieceOnTile, rookTile.tileCoordinate, 61))

            if not self.board.tile(59).isTileOccupied() and not self.board.tile(58).isTileOccupied() and \
                    not self.board.tile(57).isTileOccupied():
                rookTile = self.board.tile(56)

                if rookTile.isTileOccupied() and rookTile.pieceOnTile.isFirstMove():
                    if len(self._calculateAttacksOnTile(59, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(58, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(57, opponentsLegalMoves)) == 0 and rookTile.pieceOnTile.pieceType.isRook:

                        kingCastles.append(QueenSideCastleMove(self.board, self.playerKing, 59, rookTile.pieceOnTile, rookTile.tileCoordinate, 58))

        return kingCastles
