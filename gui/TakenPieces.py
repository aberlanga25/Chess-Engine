from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from engine.classic.piece.PieceType import getValue


class TakenPieces(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainGrid = QGridLayout(self)
        self.setStyleSheet("")
        self.setContentsMargins(0, 0, 0, 0)

        self.mainGrid.setHorizontalSpacing(0)
        self.mainGrid.setVerticalSpacing(0)

        self.north = QGridLayout()
        self.south = QGridLayout()

        self.mainGrid.addLayout(self.north, 0, 0)
        self.mainGrid.addLayout(self.south, 1, 0)

        self.fillTables()

    def fillTables(self):
        for i in range(0,8):
            for h in range(0,2):
                label = QLabel("")
                self.north.addWidget(label, i, h)
                label2 = QLabel("")
                self.south.addWidget(label2, i, h)

    def redo(self, movelog):
        for i in reversed(range(0,self.north.count())):
            self.north.itemAt(i).widget().setParent(None)
        for i in reversed(range(0,self.south.count())):
            self.south.itemAt(i).widget().setParent(None)
        whiteTakenPieces = []
        blackTakenPieces = []

        for move in movelog.moves:
            if move.isAttack:
                takenPiece = move.attackedPiece
                if takenPiece.pieceAlliance.isWhite():
                    whiteTakenPieces.append(takenPiece)
                else:
                    blackTakenPieces.append(takenPiece)

        whiteTakenPieces = sorted(whiteTakenPieces, key=getValue, reverse=True)
        blackTakenPieces = sorted(blackTakenPieces, key=getValue, reverse=True)

        x= 0
        i =1
        for takenPiece in whiteTakenPieces:
            j = x%2
            label = QLabel()
            pixmap = QPixmap("img/"+takenPiece.pieceAlliance.value +
                                   str(takenPiece)+".jpg")
            label.setPixmap(pixmap)
            self.north.addWidget(label,i,j)
            if j == 1:
                i += 1
            x += 1
        for l in range(len(whiteTakenPieces),16):
            j = x % 2
            label = QLabel("")
            self.north.addWidget(label, i, j)
            if j == 1:
                i += 1
            x += 1

        x = 0
        i = 1
        for takenPiece in blackTakenPieces:
            j = x % 2
            label = QLabel()
            label.setPixmap(QPixmap("img/"+takenPiece.pieceAlliance.value +
                                   str(takenPiece)+".jpg"))
            self.south.addWidget(label,i,j)
            if j == 1:
                i += 1
            x += 1
        for l in range(len(whiteTakenPieces),16):
            j = x % 2
            label = QLabel("")
            self.south.addWidget(label, i, j)
            if j == 1:
                i += 1
            x += 1

