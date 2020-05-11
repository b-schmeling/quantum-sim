from enum import Enum
from numpy import array
from math import sqrt, pi, e
import numpy as np

ZERO = array([[complex(1,0)], [complex(0,0)]])
ONE = array([[complex(0,0)], [complex(1,0)]])

class Gatetype(Enum):
    SINGLE = 1
    DOUBLE = 2
    COMBINE = 3
    MEASURE = 4
    MEASUREALL = 5

i = complex(0,1)

PauliX = array([[0, 1],[1, 0]])

PauliY = array([[0, -i],[i, 0]])

PauliZ = array([[1, 0],[0, -1]])

Hadamard = array([[1,1],[1,-1]]) * (1 / sqrt(2))

Phase = array([[1, 0],[0,i]])

OpT = array([[1, 0], [0, pow(e, i * pi / 4)]])

Swap = array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])

CNotReverse = array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])

CNot = array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])

I = array([[1,0],[0,1]])
