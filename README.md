# Reto Técnico: Procesamiento de Transacciones Bancarias (CLI)

## Introducción
Este proyecto es una aplicación de línea de comandos (CLI) desarrollada en Python que procesa un archivo CSV con transacciones bancarias y genera un reporte con la siguiente información:
- **Balance Final**: Calculado como la suma de los montos de las transacciones de tipo "Crédito" menos la suma de los montos de tipo "Débito".
- **Transacción de Mayor Monto**: Identificación del ID y el monto de la transacción más alta.
- **Conteo de Transacciones**: Número total de transacciones para cada tipo.

El propósito de este reto es evaluar la capacidad de leer archivos CSV, procesar datos y generar informes de manera estructurada.

## Instrucciones de Ejecución

### 1. Requisitos Previos
- Tener instalado Python 3.7 o superior.
- Clonar este repositorio en tu máquina local.

### 2. Instalación
```bash
# Clonar el repositorio
git clone https://github.com/anthonycs4/retotecnico-cobol.git
cd retotecnico-cobol
# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate
#Agregar una archivo csv con el nombre:
transacciones.csv
#O usar el que esta por defecto
# Ejecutar la aplicación pasando un archivo CSV como argumento
python main.py transacciones.csv
```

### 3. Formato del Archivo CSV
```csv
id,tipo,monto
1,Crédito,100.00
2,Débito,50.00
3,Crédito,200.00
4,Débito,75.00
5,Crédito,150.00
```

## Enfoque y Solución
### transacciones.py:
```python
import csv
import sys
import json

def leer_transacciones(archivo_csv):
    """Lee el archivo CSV y devuelve una lista de transacciones."""
    transacciones = []
    try:
        with open(archivo_csv, mode='r', encoding='utf-8') as file:
            lector = csv.DictReader(file)
            for fila in lector:
                # Validación de datos
                try:
                    id_transaccion = int(fila["id"])
                    tipo_transaccion = fila["tipo"]
                    monto_transaccion = float(fila["monto"])
                    if tipo_transaccion not in ["Crédito", "Débito"]:
                        raise ValueError(f"Tipo de transacción inválido: {tipo_transaccion}")
                except ValueError as e:
                    print(f"Error en los datos de la transacción ID {fila['id']}: {e}")
                    continue  # Skip the invalid transaction

                transacciones.append({
                    "id": id_transaccion,
                    "tipo": tipo_transaccion,
                    "monto": monto_transaccion
                })
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_csv}' no fue encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

    return transacciones

def calcular_balance(transacciones):
    """Calcula el balance final sumando Créditos y restando Débitos."""
    credito_total = sum(t["monto"] for t in transacciones if t["tipo"] == "Crédito")
    debito_total = sum(t["monto"] for t in transacciones if t["tipo"] == "Débito")
    return credito_total - debito_total

def transaccion_mayor(transacciones):
    """Encuentra la transacción con el mayor monto."""
    mayor = max(transacciones, key=lambda t: t["monto"])
    return mayor["id"], mayor["monto"]

def contar_transacciones(transacciones):
    """Cuenta la cantidad de transacciones de cada tipo."""
    credito = sum(1 for t in transacciones if t["tipo"] == "Crédito")
    debito = sum(1 for t in transacciones if t["tipo"] == "Débito")
    return credito, debito

def mostrar_reporte(balance, max_transaccion, conteo, exportar=False):
    """Imprime el reporte de transacciones en la terminal y exporta el reporte si se solicita."""
    reporte = f"""
Reporte de Transacciones
---------------------------------------------
Balance Final: {balance:.2f}
Transacción de Mayor Monto: ID {max_transaccion[0]} - {max_transaccion[1]:.2f}
Conteo de Transacciones: Crédito: {conteo[0]} Débito: {conteo[1]}
"""
    print(reporte)

    if exportar:
        # Exportar el reporte a un archivo JSON y CSV
        try:
            with open('reporte.json', 'w') as json_file:
                json.dump({
                    "balance_final": balance,
                    "transaccion_mayor": {
                        "id": max_transaccion[0],
                        "monto": max_transaccion[1]
                    },
                    "conteo_transacciones": {
                        "credito": conteo[0],
                        "debito": conteo[1]
                    }
                }, json_file, indent=4)
            print("Reporte exportado a reporte.json")

            with open('reporte.csv', 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Balance Final", "Transacción Mayor ID", "Transacción Mayor Monto", "Conteo Crédito", "Conteo Débito"])
                writer.writerow([balance, max_transaccion[0], max_transaccion[1], conteo[0], conteo[1]])
            print("Reporte exportado a reporte.csv")
        except Exception as e:
            print(f"Error al exportar el reporte: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo_csv>")
        sys.exit(1)

    archivo_csv = sys.argv[1]
    transacciones = leer_transacciones(archivo_csv)
    if not transacciones:
        print("No se encontraron transacciones válidas.")
        sys.exit(1)

    balance = calcular_balance(transacciones)
    max_transaccion = transaccion_mayor(transacciones)
    conteo = contar_transacciones(transacciones)
    
    # Mostrar el reporte y exportar el reporte a archivos JSON y CSV
    mostrar_reporte(balance, max_transaccion, conteo, exportar=True)

```
### Main.py
```python
import sys
from transacciones import leer_transacciones, calcular_balance, transaccion_mayor, contar_transacciones, mostrar_reporte  # Importar mostrar_reporte

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.csv")
        sys.exit(1)

    archivo_csv = sys.argv[1]
    transacciones = leer_transacciones(archivo_csv)

    balance = calcular_balance(transacciones)
    id_mayor, monto_mayor = transaccion_mayor(transacciones)
    credito, debito = contar_transacciones(transacciones)

    print("Reporte de Transacciones")
    print("---------------------------------------------")
    print(f"Balance Final: {balance:.2f}")
    print(f"Transacción de Mayor Monto: ID {id_mayor} - {monto_mayor:.2f}")
    print(f"Conteo de Transacciones: Crédito: {credito} Débito: {debito}")

    # Mostrar el reporte y exportar el reporte a archivos JSON y CSV
    mostrar_reporte(balance, (id_mayor, monto_mayor), (credito, debito), exportar=True)  # Activamos la exportación aquí

if __name__ == "__main__":
    main()

```
## Estructura del Proyecto
```bash
retotecnico-cobol/
│── main.py              # Punto de entrada del programa
│── transacciones.py      # Funciones de procesamiento de datos
│── transacciones.csv     # Archivo de prueba
│── README.md            # Documentación del proyecto
```

## Documentación y Calidad del Código
- **Modularidad**: Se separaron las funciones en un archivo aparte (`transacciones.py`) para mantener la claridad.
- **Legibilidad**: Se usaron nombres de variables y funciones descriptivos.
- **Comentarios**: Se agregaron comentarios explicativos en el código para facilitar su comprensión.


