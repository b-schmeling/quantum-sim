from numpy import array, kron, vstack
from defs import *
import random
from qubit import Qubit

def generateStates(numqbits):
    return [format(x, "0%ib" % numqbits)
             for x in range(0, pow(2,numqbits))]

class State:
    def __init__(self, qbits):
        self.numqbits = qbits
        self.size = pow(2,qbits)
        self.data = []
        for x in range(0,qbits):
            a = Qubit()
            self.data.append(a)
        random.seed()
        
    def __str__(self):
        ret = ""
        indx = 0
        for x in self.data:
            ret = ret + "Qubit: %i\n%s" % (indx, str(x))
            indx += 1
        return ret

    def reset(self):
        self.data = []
        for x in range(0,self.numqbits):
            a = Qubit()
            self.data.append(a)

    def qbit(self, qbitNum):
        return self.data[qbitNum]

    def combine(self, qbit1, qbit2):
        self.data[qbit1] += self.data[qbit2]

    def M(self,qbitNum):
        #measurement will destroy entangled quantum state
        #and return combined qubits to separate positions
        q = self.data[qbitNum]
        qs = [qbitNum] #qs holds empty qubit positions to fill
        for x in range(0, q.number):
            if not len(self.data[x].data):
                qs.append(x)
        tmpstate = random.choices(
            generateStates(q.number),
            weights=[x*x for x in q.data])
        tmpstate = tmpstate[0]
        for x in tmpstate:
            n = qs.pop()
            if x == '0':
                self.data[n].data = ZERO
                self.data[n].number = 1
            else:
                self.data[n].data = ONE
                self.data[n].number = 1
        return tmpstate

    def Measure(self):
        ret = ""
        for x in range(0, self.numqbits):
            self.M(x)
            ret = self.M(x) + ret
            #doubling is necessary due to combinations
        return ret
        
    def SingleGate(self, qbitNum, gate, internalqbitNum=None):
        matrix = gate
        q = self.data[qbitNum]
        if internalqbitNum is not None:
            #i.e., there is more than one qubit in that position
            for x in range(0,internalqbitNum):
                matrix = kron(matrix, I)
            for x in range(internalqbitNum + 1, q.number):
                matrix = kron(I, matrix)
        self.data[qbitNum].data = matrix.dot(q.data)

    def CNot(self, qbit, control, target):
        #must be consecutive and combined
        if control < target:
            matrix = CNot
        else:
            matrix = CNotReverse
        self.DoubleGate(qbit, control, target, matrix)
        

    def X(self, qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, PauliX, internalqbitNum)
        
    def Y(self, qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, PauliY, internalqbitNum)
        
    def Z(self, qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, PauliZ, internalqbitNum)

    def H(self, qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, Hadamard, internalqbitNum)
    
    def PhaseShift(self,qbitNum, angle):
        self.SingleGate(qbitNum, Phase)

    def S(self,qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, Phase, internalqbitNum)        
    
    def T(self,qbitNum, internalqbitNum=None):
        self.SingleGate(qbitNum, OpT, internalqbitNum)

    def DoubleGate(self, qbit, pos1, pos2, gate):
        #must be consecutive and combined
        matrix = gate
        q = self.data[qbit]
        for x in range(0,min(pos1, pos2)):
            matrix = kron(matrix, I)
        for x in range(max(pos1, pos2) + 1, q.number):
            matrix = kron(I, matrix)
        self.data[qbit].data = matrix.dot(q.data)

    def Swap(qbit, pos1, pos2):
        self.DoubleGate(qbit, pos1, pos2, Swap)

    def printState(self):
        for num in self.data:
            print("real: %f imaginary: %f" % (num.real, num.imag))
        
