# ------------------------------------------------------------
# Dragon book - Exercise 3.5.1
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'TIMESTAMP',
    'PROC',
    'MESSAGE'
]

def t_TIMESTAMP(t):
    r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}\s-0300'
    return t

def t_PROC(t):
    r'\t[a-zA-Z][a-zA-Z0-9]*\t'
    # Regular expression for PROC
    t.value = t.value[1:len(t.value) - 1]
    return t

def t_MESSAGE(t):
    r'(.*?)\n'
    # Regular expression for MESSAGE
    t.value = t.value[:len(t.value) - 1]
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


class Ex351Lexer:
    data = None
    lexer = None

    def __init__(self):
        self.lexer = lex.lex()

    def setData(self, data):
        self.data = data
        self.lexer.input(data)

    def tokenize(self):
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            tokens.append(tok)
        return tokens


if __name__ == '__main__':
    lex = Ex351Lexer()
    lex.setData("17:54:14.473455 -0300	kernel	[IGFB][INFO   ] frameBuffer 0 : (colorMode=0x1)\n")
    print(lex.tokenize())
