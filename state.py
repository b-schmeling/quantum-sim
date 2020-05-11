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
        for x in range(0, self.numqbits):
            if self.data[x].number == 0:
                qs.append(x)
            if len(qs) == q.number:
                break
        tmpstate = random.choices(
            generateStates(q.number),
            weights=[x*x for x in q.data])
        tmpstate = tmpstate[0]
        for x in tmpstate:
            n = qs.pop()
            if x == '0':
                self.data[n].data = ZERO
                self.data[n].number = 1
                self.data[n].size = 2
            else:
                self.data[n].data = ONE
                self.data[n].number = 1
                self.data[n].size = 2
        return tmpstate

    def Measure(self):
        ret = ""
        for x in range(0, self.numqbits):
            self.M(x)
            ret = self.M(x) + ret
            #doubling is necessary due to combinations
        return ret
        
    def SingleGate(self, gate, qbitNum, internalqbitNum=None):
        matrix = gateDict[gate]
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
        self.DoubleGate(matrix, qbit, control, target)
        

    def X(self, qbitNum, internalqbitNum=None):
        self.SingleGate('PauliX', qbitNum, internalqbitNum)
        
    def Y(self, qbitNum, internalqbitNum=None):
        self.SingleGate('PauliY', qbitNum, internalqbitNum)
        
    def Z(self, qbitNum, internalqbitNum=None):
        self.SingleGate('PauliZ', qbitNum, internalqbitNum)

    def H(self, qbitNum, internalqbitNum=None):
        self.SingleGate('Hadamard', qbitNum, internalqbitNum)

    def S(self, qbitNum, internalqbitNum=None):
        self.SingleGate('Phase', qbitNum, internalqbitNum)        
    
    def T(self, qbitNum, internalqbitNum=None):
        self.SingleGate('OpT', qbitNum, internalqbitNum)

    def DoubleGate(self, gate, qbit, pos1, pos2):
        #must be consecutive and combined
        matrix = gateDict[gate]
        q = self.data[qbit]
        for x in range(0,min(pos1, pos2)):
            matrix = kron(matrix, I)
        for x in range(max(pos1, pos2) + 1, q.number):
            matrix = kron(I, matrix)
        self.data[qbit].data = matrix.dot(q.data)

    def Swap(qbit, pos1, pos2):
        self.DoubleGate('Swap',qbit, pos1, pos2)

    def printState(self):
        for num in self.data:
            print("real: %f imaginary: %f" % (num.real, num.imag))

    def horizontalString(self):
        numLines = max([q.size for q in self.data])
        lines = []
        for x in range(0,numLines):
            lines.append([])
        for qbit in self.data:
            indx = 0
            for entry in qbit.data:
                lines[indx].append(entry)
                indx += 1
            for l in range(indx, numLines):
                lines[indx].append([])
                indx += 1
        ret = []
        for l in lines:
            tmp = []
            for entry in l:
                if len(entry) == 0:
                    tmp.append("[          ]")
                else:
                    tmp.append("[%.2f+%.2fj]" % (entry.real, entry.imag))
            ret.append(tmp)
        return ret
        
        
