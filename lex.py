import sys, enum, re

"""
Determine where each token starts/stops
WHILE(keyword) nums(identifier) >(operator) 0(num) REPEAT(keyword)
"""


class Lexer:
    def __init__(self, source):
        self.source = (
            source + "\n"
        )  # Push source code to lexer as a string. Append a new line.
        self.currChar = ""  # Current char in string
        self.currPos = -1  # Current pos in string
        self.nextChar()

    # Process next char
    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.source):
            self.currChar = "\0"
        else:
            self.currChar = self.source[self.currPos]

    # Return lookahead char
    def peek(self):
        if self.currPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.currPos + 1]

    # Invalid token, error out
    def abort(self, message):
        sys.exit("Lex error, " + message)

    # Skip whitespace, not new lines
    def skip_whitespace(self):
        while self.currChar == " " or self.currChar == "\t" or self.currChar == "\r":
            self.nextChar()

    # Skip comments
    def skip_comments(self):
        if self.currChar == "#":
            while self.currChar != "\n":
                self.nextChar()

    def getToken(self):
        token_map = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.ASTERISK,
            "/": TokenType.SLASH,
            "\n": TokenType.NEWLINE,
            "\0": TokenType.EOF,
            "=": TokenType.EQ,
            ">": TokenType.GT,
            ">=": TokenType.GTEQ,
            "<": TokenType.LT,
            "<=": TokenType.LTEQ,
            "!=": TokenType.NOTEQ,
            '"': TokenType.STRING,
        }

        # Initialize token_text and token_type to None
        token_text = None
        token_type = None

        # Skip whitespace and comments
        self.skip_whitespace()
        self.skip_comments()

        """
            If the current char is in the token_map(dict), take the current char, the token_map and assign '[]' self.currChar.
            Some operators need to be expanded on as below. '<=' will be read in as seperate chars if we let the dict handle it.
            """
        if self.currChar in token_map:
            token_type = token_map[self.currChar]
            token_text = self.currChar

        if self.currChar == ">":
            if self.peek() == "=":
                # need to look at the next char so we don't overlap the prior
                self.nextChar()
                lastChar = self.currChar
                token_text = lastChar + self.currChar
                token_type = TokenType.GTEQ
            else:
                token_text = self.currChar
                token_type = TokenType.GT

        elif self.currChar == "<":
            if self.peek() == "=":
                # need to look at the next char so we don't overlap the prior
                self.nextChar()
                lastChar = self.currChar
                token_text = lastChar + self.currChar
                token_type = TokenType.LTEQ
            else:
                token_text = self.currChar
                token_type = TokenType.LT

        elif self.currChar == "!":
            if self.peek() == "=":
                # need to look at the next char so we don't overlap the prior
                self.nextChar()
                lastChar = self.currChar
                token_text = lastChar + self.currChar
                token_type = TokenType.NOTEQ
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.currChar == '"':
            # need to look at the next char so we don't overlap the prior
            self.nextChar()
            start = self.currPos

            while self.currChar != '"':
                # check that no special chars are being used
                if (
                    self.currChar == "0"
                    or self.currChar == "\n"
                    or self.currChar == "\\"
                    or self.currChar == "\r"
                    or self.currChar == "%"
                ):
                    self.abort("Illegal character")
                self.nextChar()
            # take the curr positon and then -1 to end of string
            token_text = self.source[start : self.currPos - 1]
            token_tpye = TokenType.STRING

        # if we have a digit, take it's current pos
        elif self.currChar.isdigit():
            start = self.currPos
            # if the next char is a digit, move onto the next
            while self.peek().isdigit():
                self.nextChar()
            # if a decimial point in a num, move onto next char
            if self.peek() == ".":
                self.nextChar()
            # Need to check once more so we don't incorrectly record a num that wasn't given
            while self.peek().isdigit():
                self.nextChar()

            token_text = self.source[start : self.currPos + 1]
            token_type = TokenType.NUMBER

        if token_type is None:
            self.nextChar()
            return Token(token_text, token_type)
        else:
            self.abort("Unknown token: " + self.currChar)

    
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  # actual text 'PLUS'
        self.kind = tokenKind  # The token assigned '+'


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
