from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QRect

from engine.board.BoardUtils import *
from engine.board import Board
from engine.board.Move import MoveFactory

from gui.TableUtils import BoardDirection
from gui.TakenPieces import TakenPieces
from gui.GameHistory import GameHistoryPanel

_chessboard: Board.Board
_boardDirection: BoardDirection
_highlightLegals: bool


class Table(QMainWindow):
    sourceTile = None
    destinationTile = None
    humanPiece = None

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle("PChess")

        global _chessboard, _boardDirection, _highlightLegals, _moveLog
        _chessboard = Board.createStandardBoard()
        _boardDirection = BoardDirection.NORMAL
        _highlightLegals = False
        _moveLog = Table.MoveLog()

        central_widget = QWidget(self)

        self.boardPanel = self.BoardPanel(central_widget, self)
        self.boardPanel.setGeometry(QRect(75, 10, 400, 400))
        self.takenPiece = TakenPieces(central_widget)
        self.takenPiece.setGeometry((QRect(0, 10, 75, 400)))
        self.gameHistory = GameHistoryPanel(central_widget)
        self.gameHistory.setGeometry(QRect(475, 10, 125, 400))

        self.setCentralWidget(central_widget)

        self._setMenuBar()

        self.show()

    def _setMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('File')
        pgnAct = QAction('Import PGN', self)
        pgnAct.triggered.connect(lambda: print("Import PGN"))
        exitAct = QAction("Exit", self)
        exitAct.triggered.connect(qApp.exit)

        prefMenu = menuBar.addMenu('Preference')
        flipAct = QAction('Flip Board', self)
        flipAct.triggered.connect(self._flipBoard)
        highlightAct = QAction("Highlight Legal Moves", self, checkable=True)
        highlightAct.setChecked(False)
        highlightAct.triggered.connect(self._toggleLegals)

        prefMenu.addAction(flipAct)
        prefMenu.addAction(highlightAct)
        fileMenu.addAction(pgnAct)
        fileMenu.addAction(exitAct)

    def _flipBoard(self):
        global _boardDirection
        _boardDirection = _boardDirection.opposite()
        self.boardPanel.drawBoard(_chessboard)

    def _toggleLegals(self, state):
        global _highlightLegals
        if state:
            _highlightLegals = True
        else:
            _highlightLegals = False

    class BoardPanel(QWidget):
        def __init__(self, parent, table):
            super().__init__(parent)
            self.Table = table

            self.setContentsMargins(0, 0, 0, 0)

            self.grid = QGridLayout(self)
            self.grid.setHorizontalSpacing(0)
            self.grid.setVerticalSpacing(0)
            self.boardTiles = []

            for i in range(8):
                for h in range(8):
                    tilePanel = Table.TilePanel(self, i * 8 + h)
                    tilePanel.clicked.connect(lambda: self.drawBoard(_chessboard))
                    tilePanel.clicked.connect(lambda: table.gameHistory.redo(_chessboard, _moveLog))
                    tilePanel.clicked.connect(lambda: table.takenPiece.redo(_moveLog))
                    self.grid.addWidget(tilePanel, i, h)
                    self.boardTiles.append(tilePanel)

        def drawBoard(self, board):
            for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().setParent(None)
            for i in range(8):
                for h in range(8):
                    newList = _boardDirection.traverse(self.boardTiles)
                    tile = newList[i * 8 + h]
                    tile.drawTile(board)
                    self.grid.addWidget(tile, i, h)

    class MoveLog:
        def __init__(self):
            self._moves = []

        @property
        def moves(self):
            return self._moves

        def addMove(self, move):
            self._moves.append(move)

        @property
        def size(self):
            return len(self._moves)

        def clear(self):
            self._moves = []

        def removeMove(self, move):
            self._moves.remove(move)

    class TilePanel(QWidget):
        clicked = pyqtSignal()

        def __init__(self, boardPanel, tileId):
            super().__init__(boardPanel)

            self.boardPanel = boardPanel
            self.tileId = tileId

            self.assignColor()
            self.grid = QGridLayout(self)
            self.grid.setContentsMargins(0, 0, 0, 0)

            self.label = QLabel(self)
            self.label.setScaledContents(True)

            self.assignTilePieceIcon(_chessboard)

            self.grid.addWidget(self.label)

            self.setLayout(self.grid)

        def assignColor(self):
            if inFirstRow(self.tileId) or inThirdRow(self.tileId) or inFiveRow(self.tileId) or inSevenRow(self.tileId):
                self.setStyleSheet("background-color: blanchedalmond;" if self.tileId % 2 == 0
                                   else "background-color: saddlebrown")
            else:
                self.setStyleSheet("background-color: blanchedalmond;" if self.tileId % 2 != 0
                                   else "background-color: saddlebrown")

        def drawTile(self, board):
            self.assignColor()
            self.assignTilePieceIcon(board)
            self.highlightLegals(board)

        def assignTilePieceIcon(self, board: Board.Board):
            for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().setParent(None)
            self.label = QLabel(self)
            self.label.resize(self.width(), self.height())
            if board.tile(self.tileId).isTileOccupied():
                self.label.setPixmap(QPixmap("img/"+board.tile(self.tileId).pieceOnTile.pieceAlliance.value +
                                   str(board.tile(self.tileId).pieceOnTile)+".png"))
            else:
                self.label.setText("")

        def highlightLegals(self, board):
            if _highlightLegals:
                for move in self.pieceLegalMoves(board):
                    if move.destinationCoordinate == self.tileId:
                        self.label.setText("Here")

        @staticmethod
        def pieceLegalMoves(board):
            if Table.humanPiece is not None and Table.humanPiece.pieceAlliance == board.currentPlayer.alliance:
                return Table.humanPiece.calculateLegalMoves(board)
            return []

        def mousePressEvent(self, e):
            global _chessboard

            if e.button() == Qt.RightButton:
                Table.destinationTile = None
                Table.sourceTile = None
                Table.humanPiece = None
            elif e.button() == Qt.LeftButton:
                if Table.sourceTile is None:
                    Table.sourceTile = _chessboard.tile(self.tileId)
                    Table.humanPiece = Table.sourceTile.pieceOnTile
                    if Table.humanPiece is None:
                        Table.sourceTile = None
                else:
                    Table.destinationTile = _chessboard.tile(self.tileId)
                    move = MoveFactory.createMove(_chessboard, Table.sourceTile.tileCoordinate,
                                                  Table.destinationTile.tileCoordinate)
                    transition = _chessboard.currentPlayer.makeMove(move)
                    if transition.moveStatus.isDone():
                        _chessboard = transition.transitionBoard
                        global _moveLog
                        _moveLog.addMove(move)
                    Table.destinationTile = None
                    Table.sourceTile = None
                    Table.humanPiece = None
                    #print(_chessboard)
            self.clicked.emit()


_moveLog: Table.MoveLog
