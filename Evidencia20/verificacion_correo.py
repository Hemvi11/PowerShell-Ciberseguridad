import sys
import requests
import time
import getpass
import os
import logging
import csv
import urllib.parse

# Configuración logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def obtener_api_key():
    if not os.path.exists("apikey.txt"):
        print("No se encontró apikey.txt")
        clave = getpass.getpass("Ingresa tu API key: ").strip()
        with open("apikey.txt", "w", encoding="utf-8") as f:
            f.write(clave)
        print("API key guardada en apikey.txt")
    with open("apikey.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

def crear_reporte_csv():
    with open("reporte.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Título", "Dominio", "Fecha de Brecha", "Datos Comprometidos", "Verificada", "Sensible"])

def agregar_fila_csv(fila):
    with open("reporte.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fila)

def main():
    if len(sys.argv) != 2:
        print("Uso: python verificar_correo.py correo@example.com")
        sys.exit(1)
    correo = sys.argv[1]

    api_key = obtener_api_key()
    crear_reporte_csv()

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(correo)}"
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "PythonScript"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        brechas = response.json()
        logging.info(f"Consulta exitosa para {correo}. Brechas encontradas: {len(brechas)}")
        print(f"\nLa cuenta {correo} ha sido comprometida en {len(brechas)} brechas.\n")

        for i, brecha in enumerate(brechas[:3]):
            nombre = brecha['Name']
            detalle_url = f"https://haveibeenpwned.com/api/v3/breach/{urllib.parse.quote(nombre)}"
            detalle_resp = requests.get(detalle_url, headers=headers)
            if detalle_resp.status_code == 200:
                detalle = detalle_resp.json()
                fila = [
                    detalle.get('Title', ''),
                    detalle.get('Domain', ''),
                    detalle.get('BreachDate', ''),
                    ", ".join(detalle.get('DataClasses', [])),
                    detalle.get('IsVerified', ''),
                    detalle.get('IsSensitive', '')
                ]
                agregar_fila_csv(fila)
                print(f"Detalle de brecha {i+1} agregado a reporte.csv")
            else:
                print(f"No se pudo obtener detalles de la brecha: {nombre}")

            if i < 2:
                print("Esperando 10 segundos antes de la siguiente consulta...\n")
                time.sleep(10)

        print("\nReporte generado en reporte.csv")
    elif response.status_code == 404:
        print(f"La cuenta {correo} no aparece en ninguna brecha conocida.")
        logging.info(f"Consulta exitosa para {correo}. No se encontraron brechas.")
    elif response.status_code == 401:
        print("Error de autenticación: revisa tu API key.")
        logging.error("Error 401: API key inválida.")
    else:
        print(f"Error inesperado. Código de estado: {response.status_code}")
        logging.error(f"Error inesperado. Código de estado: {response.status_code}")

if __name__ == "__main__":
    main()
