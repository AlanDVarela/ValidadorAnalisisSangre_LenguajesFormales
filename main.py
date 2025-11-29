from lexer import lexer
from parser import parser
from datetime import datetime
import re

# Validacion semantica
def validar_semantica(data):

    errores_encontrados = []  # Lista para acumular todos los errores

    # Validacion folio
    folio = data.get("folio")
    if folio is None:
        errores_encontrados.append("✖ Error estructural: Falta el campo 'folio'.")
    elif not str(folio).isdigit():
        errores_encontrados.append(f"✖ Error de formato: El folio '{folio}' debe ser numérico y sin espacios.")
    
    #Validacion fechas 
    fechas_ok = True
    dt_toma = None
    dt_validacion = None
    dt_nacimiento = None
    fmt_hora = "%d/%m/%Y %H:%M:%S"

    # Fecha Toma
    str_toma = data.get("fecha_toma")
    if str_toma:
        try:
            dt_toma = datetime.strptime(str_toma, fmt_hora)
        except ValueError:
            errores_encontrados.append(f"✖ Error de formato: 'fecha_toma' ({str_toma}) debe ser 'dd/mm/yyyy hh:mm:ss'.")
            fechas_ok = False
    else:
        errores_encontrados.append("✖ Error estructural: Falta 'fecha_toma'.")
        fechas_ok = False

    # Fecha Validación
    str_val = data.get("fecha_validacion")
    if str_val:
        try:
            dt_validacion = datetime.strptime(str_val, fmt_hora)
        except ValueError:
            errores_encontrados.append(f"✖ Error de formato: 'fecha_validacion' ({str_val}) debe ser 'dd/mm/yyyy hh:mm:ss'.")
            fechas_ok = False
    else:
        errores_encontrados.append("✖ Error estructural: Falta 'fecha_validacion'.")
        fechas_ok = False

    # Coherencia temporal
    if dt_toma and dt_validacion:
        if dt_validacion < dt_toma:
            errores_encontrados.append("✖ Error lógico: La fecha de validación es anterior a la fecha de toma.")
            fechas_ok = False

    # Edad vs nacimiento
    if "paciente" in data:
        #Validar nombre, texto,espacios, sin numeros
        nombre_pac = data["paciente"].get("nombre")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\,]+$", str(nombre_pac)):
            errores_encontrados.append(f"✖ Error semántico: El nombre del paciente '{nombre_pac}' no es válido (solo se permiten letras y comas).")

        str_nac = data["paciente"].get("fecha_nacimiento")
        edad_reportada = data["paciente"].get("edad")
        #Validar edad positivo
        val_edad = None # Variable auxiliar para guardar la edad limpia

        # Validar que la edad es numero y positiva
        if edad_reportada is not None:
            try:
                val_edad = float(edad_reportada)
                
                if val_edad < 0:
                    errores_encontrados.append(f"✖ Error lógico: La edad '{edad_reportada}' no puede ser negativa.")
                    val_edad = None 
                elif val_edad > 120:
                    errores_encontrados.append(f"    ⚠ Advertencia: La edad '{edad_reportada}' es inusualmente alta.")
            except (ValueError, TypeError):
                errores_encontrados.append(f"✖ Error de formato: La edad '{edad_reportada}' debe ser un número.")
        
        # 2. Validar fecha nacimiento y cruzar con edad (si la edad era válida)
        if str_nac:
            try:
                dt_nacimiento = datetime.strptime(str_nac, "%d/%m/%Y")
                
                if dt_toma and val_edad is not None:
                    #Edad real
                    edad_calculada = dt_toma.year - dt_nacimiento.year - ((dt_toma.month, dt_toma.day) < (dt_nacimiento.month, dt_nacimiento.day))
                    
                    # Comparamos (convertimos val_edad a int para ignorar decimales ej: 25.0 == 25)
                    if int(val_edad) != edad_calculada:
                        errores_encontrados.append(f"✖ Error lógico: La edad declarada ({int(val_edad)}) no coincide con la fecha de nacimiento ({edad_calculada} años).")
                        fechas_ok = False

            except ValueError:
                errores_encontrados.append(f"✖ Error de formato: 'fecha_nacimiento' ({str_nac}) debe ser 'dd/mm/yyyy'.")
                fechas_ok = False

        #Validar sexo
        sexo_reportado = data["paciente"].get("sexo")
    
        # M o F
        if sexo_reportado not in ["M", "F"]:
            errores_encontrados.append(f"✖ Error semántico: Sexo '{sexo_reportado}' no válido. Debe ser 'M' o 'F'.")

    if fechas_ok:
        print("✔ Fechas correctas y lógicas.")

    # Validaciones semánticas
    if data.get("seccion") != "Biometría Hemática":
        errores_encontrados.append(f"✖ Error semántico: Sección '{data.get('seccion')}' inválida. Se espera 'Biometría Hemática'.")

    validos_biometria = ["Leucocitos", "Eritrocitos", "Hemoglobina", "Hematocrito",
                         "Plaquetas", "Neutrófilos", "Linfocitos", "Monocitos"]

    if "parametros" in data and isinstance(data["parametros"], list):
        for i, param in enumerate(data["parametros"]):
            nombre = param.get("nombre")
            
            if nombre not in validos_biometria:
                errores_encontrados.append(f"✖ Error semántico: '{nombre}' no pertenece a la sección 'Biometría Hemática'.")
            

            limite_str = param.get("limite", "")
            resultado = param.get("resultado")

            # validacion limite [min - max]
            patron = r"^\[\s*(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)\s*\]$"

            match = re.match(patron, limite_str)

            if not match:
                errores_encontrados.append(f"✖ Error de formato: El límite '{limite_str}' no cumple con el formato '[min - max]'.")

            else:
                #validacion resultados vs limites
                try:
                    min_val = float(match.group(1))
                    max_val = float(match.group(2))
                    val_resultado = float(resultado)

                    # Validar si está fuera de rango
                    if not (min_val <= val_resultado <= max_val):
                        print(f"    ⚠ Alerta clínica: '{nombre}' ({val_resultado}) está fuera del rango normal {limite_str}")

                except ValueError:
                    errores_encontrados.append(f"✖ Error semántico: El resultado '{resultado}' no es numérico, no se puede comparar.")
            

            #Validacion nota
            if "nota" in param and param["nota"] not in ["*", "**", "+"]:
                errores_encontrados.append(f"✖ Error de formato: Nota '{param['nota']}' inválida.")

    try:
        cedula = data["firma"]["cedula"]
        if len(str(cedula)) != 8 or not str(cedula).isdigit():
            errores_encontrados.append("✖ Error de formato: campo 'cedula' debe tener 8 dígitos.")
    except KeyError:
        errores_encontrados.append("✖ Error semántico: Falta campo 'cedula'.")

    # Imprimir todos los errores al final
    if errores_encontrados:
        #print("\nErrores semánticos detectados:")
        for e in errores_encontrados:
            print(e)
        print(f"✔ Archivo verificado con {len(errores_encontrados)} observaciones/advertencias.")
    else:
        print("✔ Archivo verificado sin errores.")




# Carga de archivo
def cargar_y_validar(nombre_archivo):
    
    print(f"Validando archivo: {nombre_archivo}")
    print("-" * 43)


    lexer.error = False
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

            try:
                resultado = parser.parse(contenido)
            except SyntaxError as e:
                # Error léxico reportado desde t_error
                print(str(e))
                return
            except Exception as e:
                # Otros errores durante el parseo
                print(f"✖ Error inesperado durante el parseo: {e}")
                return

            # Si el lexer marcó error por otro camino (por precaución)
            if getattr(lexer, "error", False):
                print("✖ El análisis se detuvo debido a errores léxicos (caracteres inválidos).")
                return

            if not resultado:
                print("✖ Error en la estructura general")
            else:
                print("✔ Estructura general válida.")
                validar_semantica(resultado)

    except FileNotFoundError:
        print(f"✖ Error: El archivo '{nombre_archivo}' no existe.")
    except Exception as e:
        print(f"✖ Error inesperado: {e}")


#Ejecucion
if __name__ == "__main__":
    cargar_y_validar("reporte_hematologia.json")