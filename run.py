from state import State
from defs import *
import functools as ft
import pickle

class Run:
    def __init__(self, qbits):
        self.state = State(qbits)
        self.circuit = []

    def __str__(self):
        return str(self.state)

    def addToCircuit(self, gatetype, *args):
        if gatetype == Gatetype.MEASURE:
            self.circuit.append(ft.partial(self.state.M, *args))
        elif gatetype == Gatetype.COMBINE:
            args = args[1:]
            self.circuit.append(ft.partial(self.state.combine, *args))
        elif gatetype == Gatetype.SINGLE:
            self.circuit.append(ft.partial(self.state.SingleGate, *args))
        elif gatetype == Gatetype.DOUBLE:
            self.circuit.append(ft.partial(self.state.DoubleGate, *args))
        elif gatetype == Gatetype.MEASUREALL:
            self.circuit.append(ft.partial(self.state.Measure))
        
    def runCircuit(self):
        print("Initial State:")
        self.state.reset()
        print(self.state)
        for x in self.circuit:
            x()
        print("Final State:")
        print(self.state)

    def runNCircuit(self, n):
        results = []
        for x in range(0,n):
            self.state.reset()
            for x in self.circuit:
                x()
            results.append(self.state.Measure())
        return results

    def save(self, filename):
        #only in linux because of forward slash
        with open(filename, 'wb') as f:
            pickle.dump((self.state, self.circuit), f)

    def load(self, filename):
        #only works in linux
        with open(filename, 'rb') as f:
            x = pickle.load(f)
            self.state = x[0]
            self.circuit = x[1]
            
