#======================================================================================#
#================================== Start of Program ==================================#
#======================================================================================#
from token import Token
from token import (
    INTEGER, REAL, STRING, PLUS, MINUS, MUL, MOD, DIV, SQRT, LOG, POW, EOF,
    TRUE, FALSE, GE, GT, LT, LE, EQ, NE, LP, RP, LB, RB, ASSIGN) 

# Interpreter class:
#    - __init__: initializes the interpreter with input text
#    - error: raises an error for invalid syntax
#    - skip_whitespace: skips whitespace characters
#    - peek: peeks at the next character without advancing the position
#    - advance_pos: advances the position in the input text
#    - _ln: computes natural logarithm using Taylor series expansion
#    - eat: consumes the current token if it matches the expected type
#    - get_next_token: tokenizes the input text
#    - factor: processes factors in the expression
#    - term: processes terms in the expression
#    - comparison: processes comparison operations
#    - expr: processes the entire expression
#======================================================================================#
class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos] if self.text else None
    #==================================================================#
    # Helpers and Utilities
    #==================================================================#
    # Raise an error for invalid syntax
    def error(self):
        raise Exception('Error parsing input')

    # Skip whitespace characters
    def skip_whitespace(self, text):
        while self.current_char is not None and self.current_char.isspace():
            self.advance_pos()

    # Peek at the next character without advancing the position
    def peek(self, text):
        next_pos = self.pos + 1
        if next_pos > len(text) - 1:
            return None
        return text[next_pos]

    # Advance the 'pos' pointer and set 'current_char'
    def advance_pos(self, x=1):
        self.pos += x
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
   
    # Natural logarithm using Taylor series expansion
    def _ln(self, x, term=20):
        if x <= 0:
            raise ValueError("Domain error: logarithm undefined for x <= 0")
        t = (x - 1) / (x + 1)
        t_pow = t
        result = 0.0
        k = 1
        for _ in range(term):
            result += t_pow / k
            t_pow = t_pow * t * t
            k += 2
        return 2 * result
    
    # Consume the current token if it matches the expected type
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    #==================================================================#
    # Tokenization
    #==================================================================#    
    def get_next_token(self):
        # Get the next token from the input text
        text = self.text

        # Skip any whitespace characters
        self.skip_whitespace(text)

        # End of input
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        
        # Tokenize integers
        if self.current_char.isdigit():
            tk = ''
            while self.pos < len(self.text) and self.current_char.isdigit():
                tk += self.text[self.pos]
                self.advance_pos()
            return Token(INTEGER, int(tk))
        
        # Tokenize operators and parentheses
        match self.current_char:
            case '+':
                self.advance_pos()
                return Token(PLUS, '+')
            case '-':
                self.advance_pos()
                return Token(MINUS, '-')
            case '*':
                self.advance_pos()
                return Token(MUL, '*')
            case '%':
                self.advance_pos()
                return Token(MOD, '%')
            case '/':
                self.advance_pos()
                return Token(DIV, '/')
            case '^':
                self.advance_pos()
                return Token(POW, '^')
            case '(':
                self.advance_pos()
                return Token(LP, '(')
            case ')':
                self.advance_pos()
                return Token(RP, ')')
            case '[':
                self.advance_pos()
                return Token(LB, '[')
            case ']':
                self.advance_pos()
                return Token(RB, ']')
            case 's':
                if self.text[self.pos:self.pos + 4] == 'sqrt':
                    token = Token(SQRT, 'sqrt')
                    self.advance_pos(4)
                    return token
                self.error()
            case 'l':
                if self.text[self.pos:self.pos + 4] == 'log2':
                    self.advance_pos(4)
                    return Token(LOG, 'log2')
                if self.text[self.pos:self.pos + 5] == 'log10':
                    self.advance_pos(5)
                    return Token(LOG, 'log10')
                self.error()
            case '>':
                if self.peek(text) == '=':
                    self.advance_pos(2)
                    return Token(GE, '>=')
                self.advance_pos()
                return Token(GT, '>')
            case '<':
                if self.peek(text) == '=':
                    self.advance_pos(2)
                    return Token(LE, '<=')
                self.advance_pos()
                return Token(LT, '<')
            case '=':
                if self.peek(text) == '=':
                    self.advance_pos(2)
                    return Token(EQ, '==')
                self.error()
            case '!':
                if self.peek(text) == '=':
                    self.advance_pos(2)
                    return Token(NE, '!=')
                self.error()
            case _:
                self.error()
    #==================================================================#
    # Expression Parsing and Evaluation
    #==================================================================#
    def factor(self):
        token = self.current_token

        match token.type:
            case 'PLUS':
                self.eat(PLUS)
                return +self.factor()
            case 'MINUS':
                self.eat(MINUS)
                return -self.factor()
            case 'INTEGER':
                self.eat(INTEGER)
                return token.value
            case 'SQRT':
                self.eat(SQRT)
                self.eat(LP)
                inner = self.expr()
                self.eat(RP)
                return inner ** 0.5
            case 'LOG':
                op = token.value
                self.eat(LOG)
                self.eat(LP)
                inner = self.expr()
                self.eat(RP)
                if op == 'log2':
                    return self._ln(inner) / self._ln(2)
                elif op == 'log10':
                    return self._ln(inner) / self._ln(10)
                self.error()
            case 'LP':
                self.eat(LP)
                result = self.expr()
                self.eat(RP)
                return result
            case _:
                self.error()
    #==================================================================#
    # Term operations
    #==================================================================#
    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV, MOD, POW):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                if self.factor() == 0:
                    raise ZeroDivisionError("division by zero")
                result = result / self.factor()
            elif token.type == MOD:
                self.eat(MOD)
                result = result % self.factor()
            elif token.type == POW:
                self.eat(POW)
                result = result ** self.factor()
                
        return result
    #==================================================================#
    # Comparison operations
    #==================================================================#
    def comparison(self):
        left = self.term()

        if self.current_token.type in (GE, LE, LT, GT, EQ, NE):
            op = self.current_token
            if op.type == GE:
                self.eat(GE)
                right = self.term()
                return TRUE if left >= right else FALSE
            elif op.type == LE:
                self.eat(LE)
                right = self.term()
                return TRUE if left <= right else FALSE
            elif op.type == LT:
                self.eat(LT)
                right = self.term()
                return TRUE if left < right else FALSE
            elif op.type == GT:
                self.eat(GT)
                right = self.term()
                return TRUE if left > right else FALSE
            elif op.type == EQ:
                self.eat(EQ)
                right = self.term()
                return TRUE if left == right else FALSE
            elif op.type == NE:
                self.eat(NE)
                right = self.term()
                return TRUE if left != right else FALSE
            
        return left
    #==================================================================#
    # Expression operations 
    # Parse and evaluate an additive expression (handles PLUS and MINUS).
    #==================================================================#
    # Behavior:
    #    - Primes the lexer on first call by reading the first token.
    #    - Parses a comparison-level value as the left operand, then
    #      repeatedly consumes PLUS/MINUS and combines with the next comparison.
    #    - Prevents mixing boolean comparison results with arithmetic; if a
    #      comparison produced a boolean sentinel, arithmetic chaining raises
    #      a parse error.

    # Returns:
    #    - numeric value (int/float) when arithmetic is performed or
    #      the raw comparison result when no additive operator follows.

    # Notes:
    #    - Prefer returning real Python booleans from `comparison()` and
    #      validate both operands before applying arithmetic to avoid
    #      surprising behavior.
    #==================================================================#
    def expr(self):
        # Prime the first token on first call
        if self.current_token is None:
            self.current_token = self.get_next_token()

        result = self.comparison()

        # Only allow arithmetic chaining when result is numeric
        while self.current_token.type in (PLUS, MINUS):
            # Disallow arithmetic if left is a boolean value
            if isinstance(result, bool):
                self.error()

            if self.current_token.type == PLUS:
                self.eat(PLUS)
                right = self.comparison()
                if isinstance(right, bool):
                    self.error()
                result = result + right
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                right = self.comparison()
                if isinstance(right, bool):
                    self.error()
                result = result - right

        return result
#======================================================================================#
#=================================== End of Program ===================================#
#======================================================================================#