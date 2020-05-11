from defs import *
from numpy import kron

class Qubit():
    def __init__(self):
        self.number = 1
        self.size = 2
        self.data = ZERO
        
    def __str__(self):
        ret = ""
        for x in self.data:
            for y in x:
                ret = ret + "[%.3f+%.3fj]\n" % (y.real, y.imag)
        return ret

    def __iadd__(self, other):
        self.data = kron(self.data, other.data)
        self.number += other.number
        self.size = pow(2, self.number)

        other.data = []
        other.number = 0

        return self
