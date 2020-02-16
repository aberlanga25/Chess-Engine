#from engine.bitboads import BitBoard


class Searcher:

    def __init__(self):
        pass

    def execute(self, board, depth: int, isMaximizing: bool):


        highestSeenValue = float('-inf')

        bestMove = None

        for move in sorted(board.gen_moves(), key=board.value, reverse=True):
            transitionBoard = board.move(move)
            value = max(highestSeenValue, self.minimax(depth-1, transitionBoard, not isMaximizing))
            if value > highestSeenValue:
                bestMove = move
                highestSeenValue = value
        return bestMove

    def minimax(self, depth: int, board, isMaximizing: bool):
        if depth == 0:
            return board.score
        if isMaximizing:
            bestMove = float('-inf')
            for move in sorted(board.gen_moves(), key=board.value, reverse=True):
                transitionBoard = board.move(move)
                bestMove = max(bestMove, self.minimax(depth-1, transitionBoard, not isMaximizing))
            return bestMove
        else:
            bestMove = float('inf')
            for move in sorted(board.gen_moves(), key=board.value, reverse=True):
                transitionBoard = board.move(move)
                bestMove = min(bestMove, self.minimax(depth-1, transitionBoard, not isMaximizing))
            return bestMove

    @staticmethod
    def isEndGameScenario(board):
        return board.currentPlayer.isInCheckMate or board.currentPlayer.isInStaleMate