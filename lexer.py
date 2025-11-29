import ply.lex as lex
import re

# Palabras reservadas para string
reserved = {
    'folio': 'FOLIO',
    'fecha_toma': 'FECHA_TOMA',
    'fecha_validacion': 'FECHA_VALIDACION',
    'paciente': 'PACIENTE',
    'nombre': 'NOMBRE',
    'fecha_nacimiento': 'FECHA_NAC',
    'sexo': 'SEXO',
    'edad': 'EDAD',
    'medico_solicitante': 'MEDICO',
    'seccion': 'SECCION',
    'parametros': 'PARAMETROS',
    'resultado': 'RESULTADO',
    'unidad': 'UNIDAD',
    'limite': 'LIMITE',
    'nota': 'NOTA',
    'firma': 'FIRMA',
    'responsable': 'RESPONSABLE',
    'cedula': 'CEDULA'
}

# Tokens
tokens = [
    'LBRACE',       # {
    'RBRACE',       # }
    'LBRACKET',     # [
    'RBRACKET',     # ]
    'COLON',        # :
    'COMMA',        # ,
    'STRING',       # "ejemplo" 
    'NUMBER',       # 123, 1.23
    'FECHA',        # 27/11/2025
    'FECHA_HORA',   # 27/11/2025 20:01:58
    'CARACTER'      # M o F
]+ list(reserved.values())

#Reglas de expresion regular para cada token

#TOKENS ESTRUCTURALES
def t_LBRACE(t):
    r'\{'
    #print(f"→ Reconocí un LBRACE: {{")
    return t

def t_RBRACE(t):
    r'\}'
    #print(f"→ Reconocí un RBRACE: }}")
    return t

def t_LBRACKET(t):
    r'\['
    #print(f"→ Reconocí un LBRACKET: [")
    return t

def t_RBRACKET(t):
    r'\]'
    #print(f"→ Reconocí un RBRACKET: ]")
    return t

def t_COLON(t):
    r':'
    #print(f"→ Reconocí un COLON: :")
    return t

def t_COMMA(t):
    r','
    #print(f"→ Reconocí un COMMA: ,")
    return t

#TOKENS SEMANTICOS
def t_FECHA_HORA(t):
    r'"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}"' # dd/mm/yyyy hh:mm:ss
    t.value = t.value.strip('"')
    return t

def t_FECHA(t):
    r'"\d{2}/\d{2}/\d{4}"' # dd/mm/yyyy
    t.value = t.value.strip('"')
    return t

def t_CARACTER(t):
    r'"[FM]"' #M o F
    t.value = t.value.strip('"')
    return t

def t_STRING(t):
    r'"[^"]*"'
    val_clean = t.value.strip('"')
    # Checamos si es una palabra reservada
    t.type = reserved.get(val_clean.lower(), 'STRING') #CADENA defecto
    t.value = val_clean
    return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'  # NUEVO: Soporta enteros y decimales (ej. 5.9)
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    #print(f"→ Reconocí un NUMBER: {t.value}")
    return t

# Caracteres que vamos a ignorar (tabulares, espacios, saltos de linea)
t_ignore = ' \t\n'


# Caracteres ilegales
def t_error(t):
    msg = (f"✖ Error lexico: Carácter '{t.value[0]}' no válido.\n"
           "✖ El análisis se detuvo debido a errores léxicos (caracteres inválidos).")
    t.lexer.error = True
    # Detenemos el lexer/parseo lanzando una excepción clara
    raise SyntaxError(msg)
# Lexer
lexer = lex.lex() # Se crea instancia del analizador léxico
