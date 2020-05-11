#!/usr/bin/env python
import curses
from run import Run
from defs import *
import sys


gates = [('Measure', Gatetype.MEASURE), 
         ('Combine', Gatetype.COMBINE),
         ('PauliX', Gatetype.SINGLE),
         ('PauliY', Gatetype.SINGLE),
         ('PauliZ', Gatetype.SINGLE),
         ('Hadamard', Gatetype.SINGLE),
         ('Phase', Gatetype.SINGLE),
         ('T', Gatetype.SINGLE),
         ('Swap', Gatetype.DOUBLE),
         ('CNot', Gatetype.DOUBLE),
         ('CNotReverse', Gatetype.DOUBLE),
         ('MeasureAll', Gatetype.MEASUREALL)]

def print_gates(scr, rowSelected):
    scr.clear()
    scr.attron(curses.color_pair(3))
    x = 2
    y = 2
    row = 0
    for g in gates:
        if row == rowSelected:
            scr.addstr(y, x, g[0], curses.color_pair(2))
        else:
            scr.addstr(y, x, g[0])
        row += 1
        y += 1
    scr.attroff(curses.color_pair(3))
    scr.refresh()
        
def print_qbits(scr, state, numQubits, maxY):
    scr.clear()
    qbitHeader = ""
    for n in range(0, numQubits):
        qbitHeader += "       %i      " % n
    lines = state.horizontalString()
    qubitsY = 2
    qubitsX = 1
    scr.attron(curses.color_pair(3))
    scr.addstr(1, qubitsX, qbitHeader)
    for l in lines:
        indx = 0
        s = ""
        for entry in l:
            s += "  %s" % entry
        scr.addstr(qubitsY, qubitsX, s)
        qubitsY += 1

    scr.addstr(24, 1, "G/Up: Gates | R: Run | S: Save Circuit | L: Load Circuit | E: Exit")
    scr.attroff(curses.color_pair(3))
    scr.refresh()

def do(run, gatetype, gate, arguments):
    arguments = arguments.split()
    args = [int(x) for x in arguments]
    run.addToCircuit(gatetype, gate, *args)
    if gatetype == Gatetype.MEASURE:
        run.state.M(*args)
    elif gatetype == Gatetype.COMBINE:
        run.state.combine(*args)
    elif gatetype == Gatetype.SINGLE:
        run.state.SingleGate(gate, *args)
    elif gatetype == Gatetype.DOUBLE:
        run.state.DoubleGate(gate, *args)
    elif gatetype == Gatetype.MEASUREALL:
        run.state.Measure()

def main(scr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    if len(sys.argv) < 2:
        scr.addstr("Usage: %s num_qubits" % sys.argv[0])
        scr.refresh()
        scr.getch()
        exit(1)

    numQubits = int(sys.argv[1])
    quantumState = Run(numQubits)
    currentRow = 0
    (maxX, maxY) = scr.getmaxyx()

    print_qbits(scr, quantumState.state, numQubits, maxY)


    #TODO: CLEANUP 
    while 1:
        key = scr.getch()
        if key == ord('g') or key == curses.KEY_UP:
            print_gates(scr, currentRow)
            while 1:
                key = scr.getch()
                if key == curses.KEY_UP and currentRow > 0:
                    currentRow -= 1
                elif key == curses.KEY_DOWN and currentRow < len(gates)-1:
                    currentRow += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    gate = gates[currentRow][0]
                    gatetype = gates[currentRow][1]
                    currentRow = 0
                    curses.echo()
                    scr.addstr(19,0,"Enter arguments:")
                    arguments = scr.getstr(20,0)
                    curses.noecho()
                    do(quantumState,gatetype, gate, arguments)
                    print_qbits(scr, quantumState.state, numQubits, maxY)
                    break
                
                elif key == ord('q'):
                    print_qbits(scr, quantumState.state, numQubits,maxY)
                    break
                print_gates(scr, currentRow)
        elif key == ord('q'):
            print_qbits(scr, quantumState.state, numQubits, maxY)
        elif key == ord('e'):
            break
        elif key == ord('s'):
             curses.echo()
             scr.addstr(25,0,"Enter filename to save:")
             filename = scr.getstr(26,0)
             quantumState.save(filename)
             curses.noecho()
             print_qbits(scr, quantumState.state, numQubits, maxY)
        elif key == ord('l'):
             curses.echo()
             scr.addstr(25,0,"Enter filename to load:")
             filename = scr.getstr(26,0)
             quantumState.load(filename)
             curses.noecho()
             print_qbits(scr, quantumState.state, numQubits, maxY)
        elif key == ord('r'):
            quantumState.runCircuit()
    
curses.wrapper(main)
