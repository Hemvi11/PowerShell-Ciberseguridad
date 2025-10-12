"""
funciones.py
Módulo con funciones para verificar correos comprometidos mediante la API de Have I Been Pwned.
Cumple con las guías PEP8 y genera registros de actividad en registro.log
"""

import os
import csv
import time
import logging
import argparse
import requests
import getpass


# Configurar logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def leer_apikey(path="apikey.txt"):
    """
    Lee de forma segura la API key desde un archivo.
    Si no existe, solicita la clave y la guarda localmente.
    """
    if not os.path.exists(path):
        clave = getpass.getpass("Ingresa tu API key: ")
        with open(path, "w") as archivo:
            archivo.write(clave.strip())

    with open(path, "r") as archivo:
        return archivo.read().strip()


def obtener_argumentos():
    """
    Obtiene los argumentos de línea de comandos con argparse.
    """
    parser = argparse.ArgumentParser(
        description="Verifica si un correo ha sido comprometido usando la API de Have I Been Pwned."
    )
    parser.add_argument("correo", help="Correo electrónico a verificar")
    parser.add_argument("-o", "--output", default="reporte.csv",
                        help="Nombre del archivo CSV de salida")
    return parser.parse_args()


def consultar_brechas(correo, api_key):
    """
    Consulta la API para verificar si el correo aparece en alguna brecha.
    """
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


def consultar_detalle(nombre, api_key):
    """
    Consulta detalles específicos de una brecha por su nombre.
    """
    url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


def generar_csv(nombre_archivo, lista_detalles):
    """
    Genera un archivo CSV con los detalles de las brechas encontradas.
    """
    with open(nombre_archivo, "w", newline='', encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Título", "Dominio", "Fecha de Brecha",
                         "Datos Comprometidos", "Verificada", "Sensible"])
        for detalle in lista_detalles:
            writer.writerow([
                detalle.get("Title"),
                detalle.get("Domain"),
                detalle.get("BreachDate"),
                ", ".join(detalle.get("DataClasses", [])),
                "Sí" if detalle.get("IsVerified") else "No",
                "Sí" if detalle.get("IsSensitive") else "No"
            ])
