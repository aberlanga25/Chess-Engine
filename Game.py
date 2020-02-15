from engine.classic.board.Board import createStandardBoard
from gui.Table import Table

from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    board = createStandardBoard()
    print(board)

    table = Table()
    sys.exit(app.exec_())