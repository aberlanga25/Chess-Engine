from engine.player.Alliance import Alliance
from engine.player.Player import Player
from engine.board.Move import QueenSideCastleMove, KingSideCastleMove

class BlackPlayer(Player):
    def __init__(self, board, white, black):
        super().__init__(board, black, white)

    def __str__(self):
        return self.alliance.value

    @property
    def activePieces(self):
        return self.board.blackPieces

    @property
    def alliance(self):
        return Alliance.Black

    @property
    def getOpponent(self) -> Player:
        return self.board.whitePlayer

    def calculateKingCastles(self, legalMoves, opponentsLegalMoves):
        kingCastles = []

        if self.playerKing.isFirstMove and not self.isInCheck:

            if not self.board.tile(5).isTileOccupied() and not self.board.tile(6).isTileOccupied():
                rookTile = self.board.tile(7)

                if rookTile.isTileOccupied() and rookTile.pieceOnTile.isFirstMove():

                    if len(self._calculateAttacksOnTile(5, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(6, opponentsLegalMoves)) == 0 \
                            and rookTile.pieceOnTile.pieceType.isRook:

                        kingCastles.append(KingSideCastleMove(self.board, self.playerKing, 6, rookTile.pieceOnTile, rookTile.tileCoordinate, 5))

            if not self.board.tile(1).isTileOccupied() and not self.board.tile(2).isTileOccupied() and \
                    not self.board.tile(3).isTileOccupied():
                rookTile = self.board.tile(0)

                if rookTile.isTileOccupied() and rookTile.pieceOnTile.isFirstMove():
                    if len(self._calculateAttacksOnTile(1, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(2, opponentsLegalMoves)) == 0 \
                            and len(self._calculateAttacksOnTile(3, opponentsLegalMoves)) == 0 \
                            and rookTile.pieceOnTile.pieceType.isRook:
                        kingCastles.append(QueenSideCastleMove(self.board, self.playerKing, 2, rookTile.pieceOnTile, rookTile.tileCoordinate, 3))

        return kingCastles
