import sys
from transacciones import leer_transacciones, calcular_balance, transaccion_mayor, contar_transacciones, mostrar_reporte

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.csv")
        sys.exit(1)

    archivo_csv = sys.argv[1]
    transacciones = leer_transacciones(archivo_csv)

    if not transacciones:
        print("No se encontraron transacciones válidas.")
        sys.exit(1)

    balance = calcular_balance(transacciones)
    id_mayor, monto_mayor = transaccion_mayor(transacciones)
    credito, debito = contar_transacciones(transacciones)

    mostrar_reporte(balance, (id_mayor, monto_mayor), (credito, debito), exportar=True)

if __name__ == "__main__":
    main()
