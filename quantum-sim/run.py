from state import State
from defs import *
import functools as ft


class Circuit:
    def __init__(self):
        self.circuit = []

class Run:
    def __init__(self, qbits):
        self.state = State(qbits)
        self.circuit = []

    def addToCircuit(self, gatetype, *args):
        if gatetype == Gatetype.MEASURE:
            self.circuit.append(ft.partial(self.state.M, *args))
        elif gatetype == Gatetype.COMBINE:
            self.circuit.append(ft.partial(self.state.combine, *args))
        elif gatetype == Gatetype.SINGLE:
            self.circuit.append(ft.partial(self.state.SingleGate, *args))
        elif gatetype == Gatetype.DOUBLE:
            self.circuit.append(ft.partial(self.state.DoubleGate, *args))
        
    def runCircuit(self):
        print("Initial State:")
        print(self.state)
        for x in self.circuit:
            x()
        print("Final State:")
        print(self.state)
