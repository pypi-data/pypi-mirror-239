import math

# Constants

Pi = 3.14159265359

# Classes

class Vector:
    X, Y = 0, 0
    def __init__(self, X = 0, Y = 0):
        self.X = X
        self.Y = Y
    def __str__(self):
        return f"{self.X}, {self.Y}"
    def length(self):
        return math.sqrt(self.X**2 + self.Y**2)

# Methods

def Clamp(N, Min, Max):
    if N < Min:
        return Min
    elif N > Max:
        return Max
    return N

def Clamp01(N):
    if N < 0:
        return 0
    elif N > 1:
        return 1
    return N

def Lerp(Start, Goal, Alpha):
    A,B = 0,0
    if Start < Goal:
        A = Start
        B = Goal
    else:
        A = Goal
        B = Start
    return (B - A) * Alpha + A
