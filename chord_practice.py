#!/usr/bin/python3

import itertools
import sys
import pprint
import random
import time
import subprocess

CHORDS = ['A', 'E', 'D']
RATE = 20

random.shuffle(CHORDS)

chords_lookup = dict(zip(range(len(CHORDS)), CHORDS))
def _chord(i):
    return chords_lookup[i]
chords = range(len(CHORDS))
print(chords)
print("chords:", chords)

if len(sys.argv) == 1 or sys.argv[1] == 'infinite':
    combinations = list(itertools.combinations(chords, 2))
    combinations = combinations + [tuple(reversed(l)) for l in combinations]
    print("combinations:", combinations)

    progression = [chords[0]]
    c = combinations.copy()
    for i in range(len(c)):
        curr = progression[-1]
        for j in range(len(c)):
            if c[j][0] == curr:
                progression.append(c[j][1])
                del c[j]
                print(c)
                break
        print(curr)
    progression = progression[:-1]

    print("progression:", [_chord(i) for i in progression])
    print("progression length:", len(progression))

    transitions = {k: 0 for k in combinations + list(zip(chords, chords))}
    for i in range(len(progression)):
        transitions[(progression[i], progression[(i + 1) % len(progression)])] += 1
    print('\n'.join([(_chord(a) + ' -> ' + _chord(b) + ' = ' + str(v)) for ((a,b),v) in transitions.items()]))

    endless_progression = itertools.cycle(progression)
    next_chord =_chord(endless_progression.__next__())
    try:
        while True:
            chord = next_chord
            next_chord =_chord(endless_progression.__next__())
            print(chord)
            subprocess.call("clear;toilet -f mono12 {};#false toilet -f smblock '   {}'".format(chord, next_chord), shell=True)
            time.sleep(60/RATE)
    except KeyboardInterrupt:
        subprocess.call("clear")
        sys.exit(0)
