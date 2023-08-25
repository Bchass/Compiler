import sys, enum

'''
Determine where each token starts/stops
WHILE(keyword) nums(identifier) >(operator) 0(num) REPEAT(keyword)
'''
class Lexer:
    def __init__(self, source):
        self.source = source + '\n' # Push source code to lexer as a string. Append a new line.
        self.currChar = '' # Current char in string
        self.currPos = -1 # Current pos in string
        self.nextChar()
    
    # Process next char
    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.source):
            self.currChar = '\0'  
        else:
            self.currChar = self.source[self.currPos]
    
    # Return lookahead char
    def peek(self):
        if self.currPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.currPos + 1]

    # Invalid token, error out
    def abort(self, message):
        sys.exit("Lex error " + message)
    
    
    # Skip whitespace, not new lines
    def skip_whitespace(self):
        if self.currChar == ' ' or self.currChar == '\t' or self.currChar == '\r':
            self.nextChar()

    # Skip comments
    def skip_comments(self):
        pass

    def getToken(self):
        token_map = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.ASTERISK,
            '/': TokenType.SLASH,
            '\n': TokenType.NEWLINE,
            '\0': TokenType.EOF,
        }
        
        # when providing tokens, we need to skip whitespace chars
        self.skip_whitespace()

        '''
        If the current char is in the token_map(dict), take the current char, the token_map and assign '[]' self.currChar.
        '''
        if self.currChar in token_map:
            token = Token(self.currChar, token_map[self.currChar])
        else:
            self.abort("Unknown token: " + self.currChar)
        # Go onto the next cahr
        self.nextChar()
        return token


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText # actual text 'PLUS'
        self.kind = tokenKind # The token assigned '+'


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    
    # Keywords
    label = 101
    goto = 102
    print = 103
    input = 104
    let = 105
    IF = 106
    then = 107
    endif = 108
    WHILE = 109
    repeat = 110
    endwhile = 111

    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211