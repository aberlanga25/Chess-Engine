from unittest import TestCase

import asyncio
from engine.classic.board.Board import createStandardBoard
from engine.classic.board.Move import MoveFactory
from engine.classic.board.BoardUtils import *
from engine.classic.player.ai.MinMax import MinMax
from engine.classic.player.ai.AlphaBeta import AlphaBeta
from engine.classic.player.ai.ParallelMiniMax import ParallelMiniMax


class TestBoard(TestCase):

    def testKiwiPeteDepth(self):