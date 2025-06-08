import json
import pandas as pd
import csv
import os

def obtener_preguntas(path='preguntas_personalidad.json'):
    with open(path, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return [item["pregunta"] for item in datos]

def guardar_resultado_usuario(nombre, resultado, ruta='resultados_personalidad.csv'):
    existe = os.path.isfile(ruta)
    with open(ruta, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        if not existe:
            writer.writerow(["Nombre", "Resultado"])
        writer.writerow([nombre, resultado])