from modelo_personalidad import predecir_personalidad

def motor_inferencia(respuestas_usuario):
    # Codificar las respuestas "Si"/"No" en 1/0
    respuestas_codificadas = []
    for r in respuestas_usuario:
        if isinstance(r, str):
            if r.strip().lower() in ["si", "sí"]:
                respuestas_codificadas.append(1)
            elif r.strip().lower() == "no":
                respuestas_codificadas.append(0)
            else:
                respuestas_codificadas.append(0)
        else:
            respuestas_codificadas.append(int(r))

    # Llamada directa sin pasar ruta
    resultado_modelo = predecir_personalidad(respuestas_codificadas).lower()

    if resultado_modelo == "introvertido":
        resultado = "Introvertido"
        conclusion = "Eres una persona que disfruta de la tranquilidad, la introspección y los ambientes más controlados."
    else:
        resultado = "Extrovertido"
        conclusion = "Eres alguien que se recarga con la interacción social y disfruta estar rodeado de personas."

    return resultado, conclusion

def guardar_resultado(nombre_usuario, respuestas, resultado, archivo='resultados_personalidad.csv'):
    # Crear diccionario con nombre, respuestas y resultado
    datos = {
        "Nombre": nombre_usuario,
        **{f"P{i+1}": r for i, r in enumerate(respuestas)},
        "Resultado": resultado
    }

    try:
        df = pd.read_csv(archivo)
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    df.to_csv(archivo, index=False)