import copy
from collections import deque
from pprint import pprint

def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    """https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-in-any-base-to-a-string"""
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def nidx(idx, lst):

    if(idx < 0): # too small
        return nidx(idx + len(lst), lst)
    if(idx >= len(lst)): # too large
        return nidx(idx - len(lst), lst)
    return idx

def gen_rules(n=30, colors=2, width=3):
    d = {}

    maxsize = colors ** width # Maximum possible rule n-string width.
    # i.e. 2^3 = 8 spaces
    
    nstr = baseN(n, colors).zfill(maxsize) # Our base-n rule.
    # i.e. 30 -> 0b00011110

    # print(nstr)

    for i in range(maxsize-1, -1, -1): # go through n-string to generate keys
    #for i in range(0, maxsize, 1): # go through n-string to generate keys

    # print(i)
        k = baseN(i, colors).zfill(width) # A single key, i.e. 0b111 or 0b101.
        
        d[k] = nstr[::-1][i] # d[011] = 1.

    # pprint(d)
    
    return d

def pretty_deque_grid(dqg):
    return '\n'.join(
            [''.join(row) for row in dqg]
            )

class CellularAutomaton(object):

    def cycle(self, times=1, verbose=False):
        
        if(times <= 0):
            return
        
        row = self.grid[-1] # get last row
        newrow = deque() # blank row
        
        if verbose: print(f"ROW {len(self.grid)}:")
        if verbose: print(''.join(row))

        for i in range(len(row)): # loop though all cells

            lb = -((self.width//2))
            ub = -lb
            
            lb += i
            ub += i 
            #Upper and lower bounds. the 'key' for rules.

            rule = ''
            for i in range(lb, ub+1, 1):
                rule += row[nidx(i, row)]

            newrow.append(self.rules[rule])
            
        if verbose: print(f"{nidx(lb, row):2d} - {nidx(ub, row):2d}: {rule} -> {self.rules[rule]}")

        self.grid.append(newrow)

        self.cycle(times - 1)

    def gen_rules(self):
        self.rules = gen_rules(n=self.rule,
                              colors=self.colors,
                              width=self.width)

    def __init__(self, n=30, colors=2, pwidth=3, gwidth=25):
        
        self.rule = n
        self.colors = colors
        self.width = pwidth

        self.grid = [ #2d list
            deque(['0' for i in range(gwidth)]),
        ]

        self.grid[0][len(self.grid[0])//2] = '1' # first row has a single black in middle.

        
        self.gen_rules()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return pretty_deque_grid(self.grid)

    def map(self, d={}) -> deque:
        """Maps chars to make output more printable."""
        for row in self.grid:
            for i in range(0, len(row)):
                row[i] = d[row[i]]
        return self.grid


ca = CellularAutomaton(30, colors=2, pwidth=3, gwidth=30)

pprint(ca.rules)

ca.cycle(20)

print(pretty_deque_grid(ca.map({'0': ' ', '1': '#'})))