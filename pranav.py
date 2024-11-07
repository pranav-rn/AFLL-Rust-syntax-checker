import ply.lex as lex
import ply.yacc as yacc

tokens=('WHILE','IF','ELSE','LET','ID','NUMBER','SEMICOLON','EQUALS','LBRACE','RBRACE','LPAREN','RPAREN','GT','LT','CHAR','FLOAT','STRING')

reserved={'while':'WHILE','if':'IF','else':'ELSE','let':'LET'}

t_SEMICOLON=r';'
t_EQUALS=r'='
t_LBRACE=r'\{'
t_RBRACE=r'\}'
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_GT=r'>'
t_LT=r'<'
t_ignore=' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type=reserved.get(t.value,'ID')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_CHAR(t):
    r"'.'"
    t.value = t.value[1] 
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1] 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}.")
    t.lexer.skip(1)

lexer=lex.lex()

def p_program(p):
    '''program : statement
               | program statement'''
    pass

def p_statement(p):
    '''statement : declaration
                 | while_loop
                 | if_statement'''
    pass

def p_declaration(p):
    '''declaration : LET ID EQUALS NUMBER SEMICOLON
                   | LET ID EQUALS FLOAT SEMICOLON
                   | LET ID EQUALS STRING SEMICOLON
                   | LET ID EQUALS CHAR SEMICOLON'''
    print(f"Correct Syntax: Variable declaration: {p[2]}={p[4]}")

def p_while_loop(p):
    '''while_loop : WHILE LPAREN condition RPAREN LBRACE program RBRACE
                  | WHILE condition LBRACE program RBRACE'''
    print(f"Correct Syntax: While loop with condition: {p[3]}")

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN LBRACE program RBRACE
                    | IF LPAREN condition RPAREN LBRACE program RBRACE ELSE LBRACE program RBRACE
                    | IF condition LBRACE program RBRACE
                    | IF condition LBRACE program RBRACE ELSE LBRACE program RBRACE'''
    if len(p)==8:
        print(f"Correct Syntax: If statement with condition: {p[3]}")
    else:
        print(f"Correct Syntax: If-else statement with condition: {p[3]}")

def p_condition(p):
    '''condition : ID GT NUMBER
                 | ID LT NUMBER
                 | ID EQUALS EQUALS NUMBER'''
    p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}" if len(p)==5 else f"{p[1]}{p[2]}{p[3]}"

def p_error(p):
    if p is None:
        print("Syntax error:Unexpected end of input.")
    else:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")

parser = yacc.yacc()

test_cases=[
    "let x=10;",                                # Correct
    "while (x>5) {let y=20;}",             # Correct
    "if (x==15) {let z=30;} else {let z=40;}",  # Correct
    "while (x>5 {let y=20;}",               # Error: missing )
    "if (x<15 {let z=30;} else {let z=40;}",  # Error: missing )
    "let y = 3.14;",            # Correct
    'let name = "hello";',      # Correct
    "let grade = 'A';"          # Correct
]

for i in test_cases:
    print(f"\nParsing:{i}")
    lexer.input(i)
    for tok in lexer:
        print(tok)
    parser.parse(i)
