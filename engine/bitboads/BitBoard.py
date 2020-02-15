def createStandardBoard() -> "BitBoard":

    white_pawn_init_pos = 0x000000000000FF00
    white_knight_init_pos = 0x0000000000000042
    white_bishop_init_pos = 0x0000000000000024
    white_rook_init_pos = 0x0000000000000081
    white_queen_init_pos = 0x0000000000000010
    white_king_init_pos = 0x0000000000000008
    black_pawn_init_pos = 0x00FF000000000000
    black_knight_init_pos = 0x4200000000000000
    black_bishop_init_pos = 0x2400000000000000
    black_rook_init_pos = 0x8100000000000000
    black_queen_init_pos = 0x1000000000000000
    black_king_init_pos = 0x0800000000000000

    return BitBoard(white_pawn_init_pos, white_knight_init_pos, white_bishop_init_pos,
                    white_rook_init_pos, white_queen_init_pos, white_king_init_pos,
                    black_pawn_init_pos, black_knight_init_pos, black_bishop_init_pos,
                    black_rook_init_pos, black_queen_init_pos, black_king_init_pos)


class BitBoard:

    whitePawns: int
    whiteKnights: int
    whiteBishops: int
    whiteRooks: int
    whiteQueen: int
    whiteKing: int

    blackPawns: int
    blackKnights: int
    blackBishops: int
    blackRooks: int
    blackQueen: int
    blackKing: int

    whitePieces: int
    blackPieces: int

    white_pawn_init_pos = 0x000000000000FF00
    black_pawn_init_pos = 0x00FF000000000000

    all_tiles = 0xFFFFFFFFFFFFFFFF

    bishop_diagonals = [-9, -7, 7, 9]

    def __init__(self, whitePawns, whiteKnight, whiteBishops, whiteRook, whiteQueen, whiteKing,
                 blackPawn, blackKnight, blackBishops, blackRook, blackQueen, blackKing):
        self.blackKing = blackKing
        self.blackQueen = blackQueen
        self.blackRooks = blackRook
        self.blackBishops = blackBishops
        self.blackKnights = blackKnight
        self.blackPawns = blackPawn
        self.whiteKing = whiteKing
        self.whiteQueen = whiteQueen
        self.whiteRooks = whiteRook
        self.whiteBishops = whiteBishops
        self.whiteKnights = whiteKnight
        self.whitePawns = whitePawns

        self.whitePieces = self._calculateWhitePieces()
        self.blackPieces = self._calculateBlackPieces()

        self.knight_lookup_table = self.calculateKnightLookupTable()

    def __str__(self):
        return self._toBinaryString("BLACK KING", self.blackKing) \
               + self._toBinaryString("BLACK QUEEN", self.blackQueen) \
               + self._toBinaryString("BLACK ROOKS", self.blackRooks) \
               + self._toBinaryString("BLACK BISHOPS", self.blackBishops) \
               + self._toBinaryString("BLACK KNIGHTS", self.blackKnights) \
               + self._toBinaryString("BLACK PAWNS", self.blackPawns) \
               + self._toBinaryString("WHITE KING", self.whiteKing) \
               + self._toBinaryString("WHITE QUEEN", self.whiteQueen) \
               + self._toBinaryString("WHITE ROOKS", self.whiteRooks) \
               + self._toBinaryString("WHITE BISHOP", self.whiteQueen) \
               + self._toBinaryString("WHITE KNIGHTS", self.whiteKnights) \
               + self._toBinaryString("WHITE PAWNS", self.whitePawns)

    def calculateLegalMoves(self) -> "BitBoard":
        return BitBoard(self._calculateWhitePawnLegals(), self._calculateWhiteKnightLegals(),
                        self._calculateWhiteBishopLegals(), self._calculateWhiteRookLegals(),
                        self._calculateWhiteQueenLegals(), self._calculateWhiteKingLegals(),
                        self._calculateBlackPawnLegals(), self._calculateBlackKnightLegals(),
                        self._calculateBlackBishopLegals(), self._calculateBlackRookLegals(),
                        self._calculateBlackQueenLegals(), self._calculateBlackKingLegals())

    def _calculateWhitePawnLegals(self) -> int:
        allPieces: int = self.whitePieces & self.blackPieces
        return (self.whitePawns << 8 & ~allPieces) | ((self.whitePawns & self.white_pawn_init_pos) << 16 & ~allPieces)

    def _calculateBlackPawnLegals(self) -> int:
        allPieces: int = self.whitePieces & self.blackPieces
        return (self.blackPawns >> 8 & ~allPieces) | ((self.blackPawns & self.black_pawn_init_pos) >> 16 & ~allPieces)

    def _calculateWhiteKnightLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.whiteKnights):
            legals |= self.knight_lookup_table[position] & ~self.whitePieces
        return legals

    def _calculateBlackKnightLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.blackKnights):
            legals |= self.knight_lookup_table[position] & ~self.blackPieces
        return legals

    def _calculateWhiteBishopLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.whiteBishops):
            candidate = position
            for diagonal in self.bishop_diagonals:
                candidate += diagonal
                while 0 <= candidate < 64 and (candidate | self.whitePieces) == 0:
                    legals |= candidate
                    if candidate | self.blackPieces != 0:
                        break
                    candidate += diagonal
        return legals

    def _calculateBlackBishopLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.blackBishops):
            candidate = position
            for diagonal in self.bishop_diagonals:
                candidate += diagonal
                while 0 <= candidate < 64 and (candidate | self.blackPieces) == 0:
                    legals |= candidate
                    if candidate | self.whitePieces != 0:
                        break
                    candidate += diagonal
        return legals

    def _calculateWhiteRookLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.whiteRooks):
            legals |= position
        return legals

    def _calculateBlackRookLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.blackRooks):
            legals |= position
        return legals

    def _calculateWhiteQueenLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.whiteQueen):
            legals |= position
        return legals

    def _calculateBlackQueenLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.blackQueen):
            legals |= position
        return legals

    def _calculateWhiteKingLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.whiteKing):
            legals |= position
        return legals

    def _calculateBlackKingLegals(self) -> int:
        legals = 0
        for position in self._bitPosition(self.blackKing):
            legals |= position
        return legals

    def _calculateWhitePieces(self) -> int:
        return self.whitePawns | self.whiteKnights | self.whiteBishops | self.whiteRooks \
               | self.whiteQueen | self.whiteKing

    def _calculateBlackPieces(self) -> int:
        return self.blackPawns | self.blackKnights | self.blackBishops | self.blackRooks \
               | self.blackQueen | self.blackKing

    @staticmethod
    def _bitPosition(n: int) -> list:
        result = []
        i, bit = 0, 0
        while n != 0:
            if n & 1 != 0:
                result.append(bit)
            n = n >> 1
            bit += 1
        return result

    @staticmethod
    def _toBinaryString(title: str, bits: int) -> str:
        s = "0" * 64
        s = int(s)
        print(s)
        s |= int("{0:b}".format(bits))
        builder = title + "\n"
        i = 1
        s = str(s)
        for c in s:
            builder += c
            if i % 8 == 0:
                builder += "\n"
            i += 1
        builder += "\n"
        return builder

    @staticmethod
    def calculateKnightLookupTable() -> list:

        knightLookupTable = [1 << 10 | 1 << 17, 1 << 11 | 1 << 16 | 1 << 18, 1 << 8 | 1 << 12 | 1 << 17 | 1 << 19,
                             1 << 9 | 1 << 13 | 1 << 18 | 1 << 20, 1 << 10 | 1 << 14 | 1 << 19 | 1 << 21,
                             1 << 11 | 1 << 15 | 1 << 20 | 1 << 22, 1 << 12 | 1 << 21 | 1 << 23, 1 << 13 | 1 << 22,
                             1 << 2 | 1 << 18 | 1 << 25, 1 << 3 | 1 << 19 | 1 << 24 | 1 << 26,
                             1 | 1 << 4 | 1 << 16 | 1 << 20 | 1 << 25 | 1 << 27,
                             1 << 1 | 1 << 5 | 1 << 17 | 1 << 21 | 1 << 26 | 1 << 28,
                             1 << 2 | 1 << 6 | 1 << 18 | 1 << 22 | 1 << 27 | 1 << 29,
                             1 << 3 | 1 << 7 | 1 << 19 | 1 << 23 | 1 << 28 | 1 << 30,
                             1 << 4 | 1 << 20 | 1 << 29 | 1 << 31, 1 << 5 | 1 << 21 | 1 << 30,
                             1 << 1 | 1 << 10 | 1 << 26 | 1 << 33, 1 | 1 << 2 | 1 << 11 | 1 << 27 | 1 << 32 | 1 << 34,
                             1 << 1 | 1 << 3 | 1 << 8 | 1 << 12 | 1 << 24 | 1 << 28 | 1 << 33 | 1 << 35,
                             1 << 2 | 1 << 4 | 1 << 9 | 1 << 13 | 1 << 25 | 1 << 29 | 1 << 34 | 1 << 36,
                             1 << 3 | 1 << 5 | 1 << 10 | 1 << 14 | 1 << 26 | 1 << 30 | 1 << 35 | 1 << 37,
                             1 << 4 | 1 << 6 | 1 << 11 | 1 << 15 | 1 << 27 | 1 << 31 | 1 << 36 | 1 << 38,
                             1 << 5 | 1 << 7 | 1 << 12 | 1 << 28 | 1 << 37 | 1 << 39,
                             1 << 6 | 1 << 13 | 1 << 29 | 1 << 38, 1 << 9 | 1 << 18 | 1 << 34 | 1 << 41,
                             1 << 8 | 1 << 10 | 1 << 19 | 1 << 35 | 1 << 40 | 1 << 42,
                             1 << 9 | 1 << 11 | 1 << 16 | 1 << 20 | 1 << 32 | 1 << 36 | 1 << 41 | 1 << 43,
                             1 << 10 | 1 << 12 | 1 << 17 | 1 << 21 | 1 << 33 | 1 << 37 | 1 << 42 | 1 << 44,
                             1 << 11 | 1 << 13 | 1 << 18 | 1 << 22 | 1 << 34 | 1 << 38 | 1 << 43 | 1 << 45,
                             1 << 12 | 1 << 14 | 1 << 19 | 1 << 23 | 1 << 35 | 1 << 39 | 1 << 44 | 1 << 46,
                             1 << 13 | 1 << 15 | 1 << 20 | 1 << 36 | 1 << 45 | 1 << 47,
                             1 << 14 | 1 << 21 | 1 << 37 | 1 << 46, 1 << 17 | 1 << 26 | 1 << 42 | 1 << 49,
                             1 << 16 | 1 << 18 | 1 << 27 | 1 << 43 | 1 << 48 | 1 << 50,
                             1 << 17 | 1 << 19 | 1 << 24 | 1 << 28 | 1 << 40 | 1 << 44 | 1 << 49 | 1 << 51,
                             1 << 18 | 1 << 20 | 1 << 25 | 1 << 29 | 1 << 41 | 1 << 45 | 1 << 50 | 1 << 52,
                             1 << 19 | 1 << 21 | 1 << 26 | 1 << 30 | 1 << 42 | 1 << 46 | 1 << 51 | 1 << 53,
                             1 << 20 | 1 << 22 | 1 << 27 | 1 << 31 | 1 << 43 | 1 << 47 | 1 << 52 | 1 << 54,
                             1 << 21 | 1 << 23 | 1 << 28 | 1 << 44 | 1 << 53 | 1 << 55,
                             1 << 22 | 1 << 29 | 1 << 45 | 1 << 54, 1 << 25 | 1 << 34 | 1 << 50 | 1 << 57,
                             1 << 24 | 1 << 26 | 1 << 35 | 1 << 51 | 1 << 56 | 1 << 58,
                             1 << 25 | 1 << 27 | 1 << 32 | 1 << 36 | 1 << 48 | 1 << 52 | 1 << 57 | 1 << 59,
                             1 << 26 | 1 << 28 | 1 << 33 | 1 << 37 | 1 << 49 | 1 << 53 | 1 << 58 | 1 << 60,
                             1 << 27 | 1 << 29 | 1 << 34 | 1 << 38 | 1 << 50 | 1 << 54 | 1 << 59 | 1 << 61,
                             1 << 28 | 1 << 30 | 1 << 35 | 1 << 39 | 1 << 51 | 1 << 55 | 1 << 60 | 1 << 62,
                             1 << 29 | 1 << 31 | 1 << 36 | 1 << 52 | 1 << 61 | 1 << 63,
                             1 << 30 | 1 << 37 | 1 << 53 | 1 << 62, 1 << 33 | 1 << 42 | 1 << 58,
                             1 << 32 | 1 << 34 | 1 << 43 | 1 << 59,
                             1 << 33 | 1 << 35 | 1 << 40 | 1 << 44 | 1 << 56 | 1 << 60,
                             1 << 34 | 1 << 36 | 1 << 41 | 1 << 45 | 1 << 57 | 1 << 61,
                             1 << 35 | 1 << 37 | 1 << 42 | 1 << 46 | 1 << 58 | 1 << 62,
                             1 << 36 | 1 << 38 | 1 << 43 | 1 << 47 | 1 << 59 | 1 << 63,
                             1 << 37 | 1 << 39 | 1 << 44 | 1 << 60, 1 << 38 | 1 << 45 | 1 << 61, 1 << 41 | 1 << 51,
                             1 << 40 | 1 << 42 | 1 << 52, 1 << 41 | 1 << 43 | 1 << 53,
                             1 << 42 | 1 << 44 | 1 << 47 | 1 << 54, 1 << 43 | 1 << 45 | 1 << 49 | 1 << 55,
                             1 << 44 | 1 << 46 | 1 << 50 | 1 << 55, 1 << 45 | 1 << 47 | 1 << 51, 1 << 46 | 1 << 53]

        return knightLookupTable


if __name__ == '__main__':
    v2 = createStandardBoard().calculateLegalMoves()
    print(v2)
