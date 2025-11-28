from lexer import lexer
from parser import parser

#prueba a realizar
data2 = '''{
      "folio": 15502427,
      "fecha_toma": "14/06/2020 07:51:57",
      "fecha_validacion": "14/06/2020 17:08:05",
      "paciente": {
        "nombre": "Ramírez Guzmán, María",
        "fecha_nacimiento": "25/04/1985",
        "sexo": "F",
        "edad": 35
      }
    }''' # cadena de entrada

data = '''
{
  {
  "folio": "15502427",
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ramírez Guzmán, María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  },
  "medico_solicitante": "Dr. Rafael Barberá Vázquez",
  "seccion": "Biometría Hemática",
  "parametros": [
    {
      "nombre": "Leucocitos", 
      "resultado": 5.9, 
      "unidad": "10^3/µL",
      "limite": "[4.5 - 10.0]"
    },
    {
      "nombre": "Eritrocitos", 
      "resultado": 4.82, 
      "unidad": "10^6/µL",
      "limite": "[4.3 - 5.8]"
    },
    {
      "nombre": "Hemoglobina", 
      "resultado": 14.2, 
      "unidad": "g/dL",
      "limite": "[12.0 - 16.0]"
    },
    {
      "nombre": "Hematocrito", 
      "resultado": 42.5, 
      "unidad": "%", 
      "limite": "[36.0 - 46.0]"
    },
    {
      "nombre": "Plaquetas", 
      "resultado": 210, 
      "unidad": "10^3/µL",
      "limite": "[150 - 400]", 
      "nota": "+"
    }
  ],
  "firma": {
    "responsable": "Q.F.B. Alejandra Ruiz Salgado",
    "cedula": "09874563"
  }
}'''



lexer.input(data) # Se analiza la cadena por el analizador léxico
print(f"Analizando fragmento:\n {data} \n")
print("=== ANALIZADOR LÉXICO ===")
for token in lexer:
    print(f"Token: {token.type}, Valor: {token.value}")

# se analiza la cadena por el parser sintáctico
print("\n=== ANALIZADOR SINTÁCTICO ===\n")
result = parser.parse(data) 
print("\nResultado del análisis sintáctico:\n")
if result is None:
    print("\nArchivo no válido")
else:
    print("\nArchivo válido:\n")
    print(result)