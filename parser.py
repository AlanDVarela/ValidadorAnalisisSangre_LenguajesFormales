import ply.yacc as yacc
from lexer import lexer, tokens


# Definición de las funciones asociadas con las reglas de producción
def p_inicio(p):
    "inicio : objeto"
    p[0] = p[1]  #resultado de objeto

def p_objeto(p):
    "objeto : LBRACE miembros RBRACE"
    p[0] = p[2]

#Miembros
def p_miembros_uno(p):
    "miembros : par"
    clave, valor = p[1]
    p[0] = {clave: valor}  # clave valor de par

def p_miembros_varios(p):
    "miembros : miembros COMMA par"
    # p[1] = dict previo, p[2] = COMMA p[3] = (clave, valor)
    d = p[1] 
    clave, valor = p[3] #par
    d[clave] = valor    # sobrescribir clave
    p[0] = d

#Par
def p_par(p):
    "par : STRING COLON valor"
    p[0] = (p[1], p[3]) 


#Valores
def p_valor_string(p):
    "valor : STRING"
    p[0] = p[1]

def p_valor_number(p):
    "valor : NUMBER"
    p[0] = p[1]

def p_valor_objeto(p):
    "valor : objeto"
    p[0] = p[1]


#Manejar errores
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")  # Imprime el token donde ocurrió el error
    else:
        print("Syntax error at EOF")  # Indica un error al final de la entrada

# Construccion analizador sintactico
parser = yacc.yacc() #se crea instancia del analizador sintáctico
