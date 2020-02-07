from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QRect, QModelIndex


class GameHistoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = DataModel()

        self.maingrid = QGridLayout(self)

        self.scrollArea = QScrollArea(self)

        self.table = QTableView(self.scrollArea)
        self.table.setGeometry(0,0,124,399)
        self.table.resizeRowsToContents()
        self.table.setModel(self.model)

        self.maingrid.addWidget(self.scrollArea)

    def redo(self, board, moveLog):
        self.model.clear()
        currentRow = 0
        moves = []
        for move in moveLog.moves:
            moveText = str(move)
            mv = {"white": "", "black": ""}

            moves.append(mv)
            if move.movedPiece.pieceAlliance.isWhite():
                self.model.insertRows(0)
                moves[currentRow]["white"] = moveText
                ix = self.model.index(0, 0, QModelIndex())
                self.model.setData(ix, moves[currentRow]["white"], Qt.EditRole)
            elif move.movedPiece.pieceAlliance.isBlack():
                moves[currentRow]["black"] = moveText
                ix = self.model.index(0, 1, QModelIndex())
                self.model.setData(ix, moves[currentRow]["black"], Qt.EditRole)
                currentRow += 1
                self.table.resizeRowToContents(ix.row())

        if len(moveLog.moves) > 0:
            lastMove = moveLog.moves[-1]
            moveText = str(lastMove)
            if lastMove.movedPiece.pieceAlliance.isWhite():
                ix = self.model.index(0, 0, QModelIndex())
                self.model.setData(ix, moveText + self.calculateCheckHash(board), Qt.EditRole)
            elif lastMove.movedPiece.pieceAlliance.isBlack():
                ix = self.model.index(0, 1, QModelIndex())
                self.model.setData(ix, moveText + self.calculateCheckHash(board), Qt.EditRole)
        self.table.resizeColumnsToContents()

    @staticmethod
    def calculateCheckHash(board):
        if board.currentPlayer.isInCheckMate:
            return "#"
        elif board.currentPlayer.isInCheck:
            return "+"
        return ""


class DataModel(QAbstractTableModel):
    def __init__(self, moves=None, parent=None):
        super(DataModel, self).__init__(parent)

        if moves is None:
            self.moves = []
        else:
            self.moves = moves

    def clear(self):
        self.beginResetModel()
        self.moves = []
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self.moves)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns the model holds. """
        return 2

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.moves):
            return None

        if role == Qt.DisplayRole:
            white = self.moves[index.row()]["white"]
            black = self.moves[index.row()]["black"]

            if index.column() == 0:
                return white
            elif index.column() == 1:
                return black

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "White"
            elif section == 1:
                return "Black"

        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.moves.insert(position + row, {"white": "", "black": ""})

        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)

        del self.moves[position:position + rows]

        self.endRemoveRows()
        return True

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given
            index and role.
        """
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.moves):
            address = self.moves[index.row()]
            if index.column() == 0:
                address["white"] = value
            elif index.column() == 1:
                address["black"] = value
            else:
                return False

            self.dataChanged.emit(index, index)
            return True

        return False
