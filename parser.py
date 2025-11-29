import ply.yacc as yacc
from lexer import lexer, tokens

error_sintactico_detectado = False


# Definición de las funciones asociadas con las reglas de producción
# regla inicial
def p_inicio(p):
    '''inicio : objeto'''

    global error_sintactico_detectado
    #Si hubo error de sintaxis, omitir validacion estructura
    if error_sintactico_detectado:
        p[0] = None
        return
    
    
    doc = p[1] #Guardamos la entrada en doc
    #bandera valido
    es_valido = True  

    
    if not isinstance(doc, dict): #doc es un dict
        print("✖ ERROR (PLY): estructura invalida o no es un objeto.")
        p[0] = None 
        return

    # Validar campos obligatorios
    obligatorios = ["folio", "fecha_toma", "fecha_validacion", "paciente", "seccion", "parametros", "firma"]
    for campo in obligatorios:
        if campo not in doc:
            print(f"✖ Error sintáctico: Falta la sección/campo obligatorio '{campo}'")
            es_valido = False 

    # paciente debe ser objeto y contener nombre, sexo, edad
    if "paciente" in doc:
        paciente = doc.get("paciente")
        if not isinstance(paciente, dict): #validar que es dict
            print("✖ ERROR: 'paciente' debe ser un objeto.")
            es_valido = False
        else:
            for i in ["nombre", "sexo", "edad"]:
                if i not in paciente:
                    print(f"✖ Error sintáctico:  Falta 'paciente.{i}'")
                    es_valido = False

   # firma debe ser objeto y contener responsable y cedula
    if "firma" in doc:
        firma = doc.get("firma")
        if not isinstance(firma, dict):
            print("✖ ERROR: 'firma' debe ser un objeto.")
            es_valido = False
        else:
            for i in ["responsable", "cedula"]:
                if i not in firma:
                    print(f"✖ Error sintáctico: Falta 'firma.{i}'")
                    es_valido = False

    # Validar parametros
    if "parametros" in doc:
        params = doc.get("parametros")
        if not isinstance(params, list):
            print("✖ ERROR: 'parametros' debe ser una lista.")
            es_valido = False
        elif len(params) == 0:
            print("✖ Error sintáctico:  La sección 'parametros' existe pero está vacía []. Debe contener resultados.")
            es_valido = False
        else:
            for i, parametro in enumerate(params):
                if not isinstance(parametro, dict):
                    print(f"✖ ERROR: 'parametros[{i}]' no es un objeto.")
                    es_valido = False
                    continue
                # dentro de la lista 
                for req in ["nombre", "resultado", "unidad", "limite"]:
                    if req not in parametro:
                        print(f"✖ Error sintáctico: Falta '{req}' en parametros[{i}]")
                        es_valido = False

    # Salida
    if es_valido:
        p[0] = doc   #Valido
    else:
        p[0] = None  #No es valida la estructura


# objetos { miembros }
def p_objeto(p):
    '''objeto : LBRACE miembros RBRACE
              | LBRACE RBRACE''' 
    #miembros con contenido
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = {}

# miembros {'folio': '123456' }
# miembros recursivo { 'folio': '123456', 'fecha_toma': '14/06/2020 07:51:57'}
def p_miembros(p):
    '''miembros : par 
                | miembros COMMA par'''
    
    global error_sintactico_detectado

    if len(p) == 2: #Solo hay un par clave,valor
        p[0] = p[1]
    else: #Hay miembros(pares) previos
        acum = p[1] #dict acum miembros previos 
        par = p[3] # par clave:valor
        if isinstance(par, dict) and len(par) == 1: #Validar que par es un dict, y tenga clave,valor
            key = next(iter(par.keys())) #Extraemos key y buscamos si hay duplicado
            if key in acum:
                print(f"✖ Error sintáctico: Clave duplicada detectada en objeto: '{key}'")
                error_sintactico_detectado = True
            acum.update(par)
        else: #Par no es un dict o no es un dict valido
            try:
                acum.update(par) #intenta hacer update
            except Exception:
                msg = f"✖ Error sintáctico: Formato inesperado al agregar par: {par}"
                print(msg)
                error_sintactico_detectado = True
        p[0] = acum #dict acumulado


# PAR 
def p_par(p):
    '''par : clave COLON valor'''
    p[0] = {p[1]: p[3]} #dict {'clave' : 'valor'}

# Palabras reservadas (No terminales)
def p_clave(p):
    '''clave : FOLIO
             | FECHA_TOMA
             | FECHA_VALIDACION
             | PACIENTE
             | NOMBRE
             | FECHA_NAC
             | SEXO
             | EDAD
             | MEDICO
             | SECCION
             | PARAMETROS
             | RESULTADO
             | UNIDAD
             | LIMITE
             | NOTA
             | FIRMA
             | RESPONSABLE
             | CEDULA
             '''  
    p[0] = p[1]

# Lista arreglo []
def p_lista(p):
    '''lista : LBRACKET elementos RBRACKET
             | LBRACKET RBRACKET''' 
    # elementos 
    if len(p) == 4:
        p[0] = p[2]  
    #vacio
    else:
        p[0] = [] 

#elementos lista
def p_elementos(p):
    '''elementos : valor
                 | elementos COMMA valor'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

# Valores 
def p_valor(p):
    '''valor : STRING
             | NUMBER
             | FECHA
             | FECHA_HORA
             | CARACTER
             | objeto
             | lista'''
    p[0] = p[1]

#Manejar errores
def p_error(p):
    global error_sintactico_detectado

    if error_sintactico_detectado:
        return

    error_sintactico_detectado = True
    if p:
        print(f"EError sintáctico en:{p.value}'")  # Imprime el token donde ocurrió el error
    else:
        print("Error sintáctico en EOF")  # Indica un error al final de la entrada

# Construccion analizador sintactico
parser = yacc.yacc() #se crea instancia del analizador sintáctico
