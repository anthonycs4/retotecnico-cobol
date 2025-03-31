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
