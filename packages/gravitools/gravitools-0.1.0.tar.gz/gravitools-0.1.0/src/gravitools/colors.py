from gravitools import math

import textwrap

# Methods

def toHex(R, G, B):
    HexValues = [hex(R), hex(G), hex(B)]
    Result = ""
    for Value in HexValues:
        Value = Value.replace('0x','')
        if len(Value) < 2:
            Value = '0' + Value
        Result += Value
    return Result

def toRGB(HexColor):
    RawValues = textwrap.wrap(HexColor.replace('#',''), 2)
    NewValues = []
    for Value in RawValues:
        NewValues.append(int(Value, 16))
    return NewValues

def Gradient(Start, End, Alpha, Fragments = 100):
    Ratio = Alpha/Fragments
    return int(math.Lerp(Start.R, End.R, Ratio)), int(math.Lerp(Start.G, End.G, Ratio)), int(math.Lerp(Start.B, End.B, Ratio))

def GradientList(Start, End, Fragments = 100):
    List = []
    for Current in range(Fragments):
        List.append(int(math.Lerp(Start.R, End.R, Current/Fragments)), int(math.Lerp(Start.G, End.G, Current/Fragments)), int(math.Lerp(Start.B, End.B, Current/Fragments)))
    return List
    

# Classes

class new:
    R, G, B = 0, 0, 0
    Hex = ""
    def __init__(self, R=0,G=0,B=0):
        self.R = R
        self.G = G
        self.B = B
        self.Hex = toHex(R, G, B)
    def __str__(self):
        return f"{self.R},{self.G},{self.B}"
