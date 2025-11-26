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


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        # Skip whitespace
        while self.pos < len(text) and text[self.pos].isspace():
            self.pos += 1

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        def peek():
            next_pos = self.pos + 1
            if next_pos > len(text) - 1:
                return None
            return text[next_pos]

        # Multi-digit integer
        if current_char.isdigit():
            tk = ''
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                tk += self.text[self.pos]
                self.pos += 1
            return Token(INTEGER, int(tk))

        # Operators
        if current_char == '+':
            self.pos += 1
            return Token(PLUS, '+')

        if current_char == '-':
            self.pos += 1
            return Token(MINUS, '-')

        if current_char == '*':
            self.pos += 1
            return Token(MUL, '*')

        if current_char == '%':
            self.pos += 1
            return Token(MOD, '%')

        if current_char == '/':
            self.pos += 1
            return Token(DIV, '/')

        if current_char == '^':
            self.pos += 1
            return Token(POW, '^')

        # Special functions
        if current_char == 's':
            # Match exactly 4 chars: 'sqrt'
            if self.text[self.pos:self.pos + 4] == 'sqrt':
                token = Token(SQRT, 'sqrt')
                self.pos += 4
                return token
            else:
                self.error()

        if current_char == 'l':
            if self.text[self.pos:self.pos + 4] == 'log2':
                self.pos += 4
                return Token(LOG, 'log2')
            elif self.text[self.pos:self.pos + 5] == 'log10':
                self.pos += 5
                return Token(LOG, 'log10')
            else:
                self.error()

        # Parentheses
        if current_char == '(':
            self.pos += 1
            return Token(LP, '(')

        if current_char == ')':
            self.pos += 1
            return Token(RP, ')')

        # Square brackets
        if current_char == '[':
            self.pos += 1
            return Token(LB, '[')

        if current_char == ']':
            self.pos += 1
            return Token(RB, ']')

        # Comparisons
        if current_char == '>':
            if peek() == '=':
                self.pos += 2
                return Token(GE, '>=')
            else:
                self.pos += 1
                return Token(GT, '>')

        if current_char == '<':
            if peek() == '=':
                self.pos += 2
                return Token(LE, '<=')
            else:
                self.pos += 1
                return Token(LT, '<')

        if current_char == '=':
            if peek() == '=':
                self.pos += 2
                return Token(EQ, '==')
            else:
                self.error()

        if current_char == '!':
            if peek() == '=':
                self.pos += 2
                return Token(NE, '!=')
            else:
                self.error()

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    # ln helper for log2/log10
    def _ln(self, x, term = 20):
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

    def factor(self):
        token = self.current_token

        if token.type == PLUS:
            self.eat(PLUS)
            return +self.factor()

        if token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()

        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value

        if token.type == SQRT:
            self.eat(SQRT)
            self.eat(LP)
            inner = self.expr()
            self.eat(RP)
            return inner ** 0.5

        if token.type == LOG:
            op = token.value
            self.eat(LOG)
            self.eat(LP)
            inner = self.expr()
            self.eat(RP)
            if op == 'log2':
                return self._ln(inner) / self._ln(2)
            elif op == 'log10':
                return self._ln(inner) / self._ln(10)
            else:
                self.error()

        if token.type == LP:
            self.eat(LP)
            result = self.expr()
            self.eat(RP)
            return result

        self.error()

    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV, MOD, POW):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()
            elif token.type == MOD:
                self.eat(MOD)
                result = result % self.factor()
            elif token.type == POW:
                self.eat(POW)
                result = result ** self.factor()

        return result

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

    def expr(self):
        # prime the first token on first call
        if self.current_token is None:
            self.current_token = self.get_next_token()

        result = self.comparison()

        # Only allow arithmetic chaining when result is numeric
        while self.current_token.type in (PLUS, MINUS):
            if isinstance(result, str):
                # already boolean TRUE/FALSE; disallow further arithmetic
                self.error()
                
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.comparison()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.comparison()

        return result
