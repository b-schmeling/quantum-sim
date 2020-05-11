from numpy import array, kron, vstack
from defs import *
import random

def generateStates(numqbits):
    return [format(x, "0%ib" % numqbits)
             for x in range(0, pow(2,numqbits))]

class Qubit():
    def __init__(self):
        self.number = 1
        self.data = [ZERO]
        
    def __str__(self):
        ret = ""
        for x in self.data:
            for y in x:
                ret = ret + "[%.3f+%.3fj]\n" % (y.real, y.imag)
        return ret

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

    def qbit(self, qbitNum):
        return self.data[qbitNum]

    def combineqbits(self, qbit1, qbit2):
        self.data[qbit1].data = kron(self.data[qbit1].data,
                                self.data[qbit2].data)
        self.data[qbit1].number += self.data[qbit2].number
        self.data[qbit1].data = self.data[qbit1].data.reshape(
            pow(2,self.data[qbit1].number),1)                                    
        self.data[qbit2].data = []
        self.data[qbit2].number = 0

    def M(self,qbitNum):
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
            n = qs.pop(0)
            if x == '0':
                self.data[n].data = ZERO
                self.data[n].number = 1
            else:
                self.data[n].data = ONE
                self.data[n].number = 1
        return tmpstate
            

    def SingleGate(self, qbitNum, gate):
        matrix = gate
        for x in range(0,qbitNum):
            matrix = kron(matrix, I)
        for x in range(qbitNum + 1, self.numqbits):
            matrix = kron(I, matrix)
        print(matrix)
        self.data = matrix.dot(self.allqbits()).flatten()

    def CNot(self, control, target):
        #must be consecutive
        if control < target:
            matrix = CNot
        else:
            matrix = CNotReverse
        for x in range(0,min(control, target)):
            matrix = kron(matrix, I)
        for x in range(max(control, target) + 1, self.numqbits):
            matrix = kron(I, matrix)
        print(matrix)
        self.data = matrix.dot(self.allqbits()).flatten()
        

    def X(self, qbitNum):
        self.SingleGate(qbitNum, PauliX)
        
    def Y(self, qbitNum):
        self.SingleGate(qbitNum, PauliY)
        
    def Z(self, qbitNum):
        self.SingleGate(qbitNum, PauliZ)

    def H(self, qbitNum):
        self.SingleGate(qbitNum, Hadamard)
    
    def PhaseShift(self,qbitNum, angle):
        self.SingleGate(qbitNum, Phase)

    def S(self,qbitNum):
        self.SingleGate(qbitNum, Phase)        
    
    def T(self,qbitNum):
        self.SingleGate(qbitNum, OpT)

    def DoubleGate(self,qbit1, qbit2, gate):
        #must be consecutive
        matrix = gate
        for x in range(0,min(qbit1, qbit2)):
            matrix = kron(matrix, I)
        for x in range(max(qbit1, qbit2) + 1, self.numqbits):
            matrix = kron(I, matrix)
        print(matrix)
        self.data = matrix.dot(self.allqbits()).flatten()

    def Swap(qbit1, qbit2):
        self.DoubleGate(qbit1,qbit2, Swap)

    def printState(self):
        for num in self.data:
            print("real: %f imaginary: %f" % (num.real, num.imag))
        
