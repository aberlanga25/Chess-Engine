from bitarray import bitarray
import struct


class ChessBitSet(bitarray):
    def __init__(self):
        super().__init__(64)

    def __lshift__(self, n):
        self[n:] + (bitarray('0') * n)

    def __rshift__(self, n):
        (bitarray('0') * n) + self[:-n]

    def __str__(self):
        s = ""
        for i in range(len(self)):
            bit = self[i]
            if bit:
                s += " 1 "
            else:
                s += " . "
            if (i + 1) % 8 == 0:
                s += '\n'
        return s

    def shift(self, shift: int) -> bitarray:
        lenght = len(self)
        if shift > 0:
            if lenght + shift < 64:
                for bitIndex in range(lenght, 0):
                    self[bitIndex + shift] = self[bitIndex]
                self[:shift] = 0
            else:
                self[shift, lenght + shift] = 0
        elif shift < 0:
            if lenght < -shift:
                self.setall(0)
            else:
                for bitIndex in range(-shift, lenght):
                    self[bitIndex + shift] = self[bitIndex]
                self[shift, lenght + shift] = 0
        return self
