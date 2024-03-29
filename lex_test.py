from lex import *

'''
Let's check the type of tokens we supply
'''

def getToken_Test():
    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()
getToken_Test()