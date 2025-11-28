import ply.yacc as yacc
from lexer import lexer, tokens


# Definición de las funciones asociadas con las reglas de producción
# regla inicial
def p_inicio(p):
    '''inicio : objeto'''
    p[0] = p[1]
    doc = p[0] #Guardamos objeto en doc

    if not isinstance(doc, dict): # doc es un dict
        print("✖ ERROR (PLY): estructura invalida o no es un objeto.")
        return

    # Validar campos obligarotios
    obligatorios = ["folio", "fecha_toma", "fecha_validacion", "paciente", "seccion", "parametros", "firma"]
    for campo in obligatorios:
        if campo not in doc:
            print(f"✖ ERROR: Falta la sección/campo obligatorio '{campo}'")

    # paciente debe ser objeto y contener nombre, sexo, edad
    paciente = doc.get("paciente")
    if "paciente" in doc:
        if not isinstance(paciente, dict): #validar que es dict
            print("✖ ERROR: 'paciente' debe ser un objeto con subcampos (nombre, sexo, edad).")
        else:
            if "nombre" not in paciente:
                print("✖ ERROR: Falta 'paciente.nombre'")
            if "sexo" not in paciente:
                print("✖ ERROR: Falta 'paciente.sexo'")        
            if "edad" not in paciente:
                print("✖ ERROR: Falta 'paciente.edad'")        

    # firma debe ser objeto y contener responsable y cedula
    firma = doc.get("firma")
    if "firma" in doc:
        if not isinstance(firma, dict): #validar que es dict
            print("✖ ERROR: 'firma' debe ser un objeto con subcampos (responsable, cedula).")
        else:
            if "responsable" not in firma:
                print("✖ ERROR: Falta 'firma.responsable'")   
            if "cedula" not in firma:
                print("✖ ERROR: Falta 'firma.cedula'")       

    # parametros: debe ser lista y cada elemento debe tener nombre, resultado, unidad, limite
    if "parametros" in doc:
        params = doc.get("parametros")
        if not isinstance(params, list): #Validar que es una lista
            print("✖ ERROR: 'parametros' debe ser una lista de objetos.")
        else:
            for i, item in enumerate(params): #Recorremos cada elemento de la lista
                if not isinstance(item, dict): #validar que cada elemento es un dict
                    print(f"✖ ERROR: 'parametros[{i}]' no es un objeto.")
                    continue
                for req_k in ["nombre", "resultado", "unidad", "limite"]:
                    if req_k not in item:
                        print(f"✖ ERROR: Falta '{req_k}' en parametros[{i}]")


# objetos { miembros }
def p_objeto(p):
    '''objeto : LBRACE miembros RBRACE'''
    p[0] = p[2]

# miembros {'folio': '123456' }
# miembros recursivo { 'folio': '123456', 'fecha_toma': '14/06/2020 07:51:57'}
def p_miembros(p):
    '''miembros : par 
                | miembros COMMA par'''
    if len(p) == 2: #Solo hay un par clave,valor
        p[0] = p[1]
    else: #Hay miembros(pares) previos
        acum = p[1] #dict acum miembros previos 
        par = p[3] # par clave:valor
        if isinstance(par, dict) and len(par) == 1: #Validar que par es un dict, y tenga clave,valor
            key = next(iter(par.keys())) #Extraemos key y buscamos si hay duplicado
            if key in acum:
                print(f"✖ ERROR SINTACTICO: Clave duplicada detectada en objeto: '{key}'")
            acum.update(par)
        else: #Par no es un dict o no es un dict valido
            try:
                acum.update(par) #intenta hacer update
            except Exception:
                msg = f"✖ ERROR SINTACTICO: Formato inesperado al agregar par: {par}"
                print(msg)
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
    '''lista : LBRACKET elementos RBRACKET'''
    p[0] = p[2]

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
    if p:
        print(f"ERROR SINTACTICO EN :{p.value}'")  # Imprime el token donde ocurrió el error
    else:
        print("ERROR SINTACTICO EN EOF")  # Indica un error al final de la entrada

# Construccion analizador sintactico
parser = yacc.yacc() #se crea instancia del analizador sintáctico
