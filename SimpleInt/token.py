#======================================================================================#
#================================== Start of Program ==================================#
#======================================================================================#
# Token types
INTEGER, REAL, STRING = 'INTEGER', 'REAL', 'STRING'
# Operators and delimiters
PLUS, MINUS, MUL, MOD, DIV, SQRT, LOG, POW, EOF = (
    'PLUS', 'MINUS', 'MUL', 'MOD', 'DIV', 'SQRT', 'LOG', 'POW', 'EOF')
# Boolean values
TRUE, FALSE = 'TRUE', 'FALSE'
# Comparison operators
GE, GT, LT, LE, EQ, NE = 'GE', 'GT', 'LT', 'LE', 'EQ', 'NE'
# Parentheses
LP, RP = 'LP', 'RP'
# Square brackets (reserved for later)
LB, RB = 'LB', 'RB'
# Assignment (reserved for later)
ASSIGN = 'ASSIGN'
#======================================================================================#
# Token class:
#     - type: token type
#     - value: token value
#     - __str__: string representation of the class instance
#     - __repr__: same as __str__
#======================================================================================#
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()
#======================================================================================#
#=================================== End of Program ===================================#
#======================================================================================#