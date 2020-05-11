from numpy import array, kron
from defs import *
import random

class State:
    def __init__(self, qbits):
        self.numqbits = qbits
        self.size = pow(2,qbits)
        self.data = np.zeros(self.size, dtype=complex, order='C')
        self.data[0] = complex(1,0)
        self.possibleStates = [format(x, "0%ib" % self.numqbits)
             for x in range(0, self.size)]
        random.seed()

    def qbit(self, qbitNum):
        qbitNum *= 2
        return self.data[qbitNum:qbitNum+2].reshape(2,1)

    def qbits(self, qbit1, qbit2):
        qbit1 *= 2
        qbit2 *= 2
        return np.hstack((
            self.data[tmp1:tmp1+2],
            self.data[tmp2:tmp2+2])).reshape(4,1)
    
    def allqbits(self):
        return self.data.reshape(self.size, 1)

    def M(self):
        tmpstate = random.choices(
            self.possibleStates,
            weights=[x*x for x in self.data])
        tmpstate = tmpstate[0]
        print(tmpstate)
        tmp = tmpstate[:1]
        tmpstate2 = tmpstate[1:]
        if tmp == '0':
            self.data = ZERO
        else:
            self.data = ONE
        for x in tmpstate2:
            if x == '0':
                self.data = kron(self.data, ZERO)
            else:
                self.data = kron(self.data, ONE)
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
        
