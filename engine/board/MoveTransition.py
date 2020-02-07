

class MoveTransition:
    def __init__(self, board, move, movestatus):
        self._transitionBoard = board
        self.move = move
        self._moveStatus = movestatus

    @property
    def moveStatus(self):
        return self._moveStatus

    @property
    def transitionBoard(self):
        return self._transitionBoard