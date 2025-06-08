reglas_preguntas = {
    "¿Te gusta pasar tiempo solo?": "introvertido",
    "¿Tienes miedo de hablar en público?": "introvertido",
    "¿Evitas eventos sociales grandes?": "introvertido",
    "¿Prefieres leer a salir?": "introvertido",
    "¿Te cansas después de socializar mucho?": "introvertido",
    "¿Tu círculo de amigos es pequeño?": "introvertido",
    "¿Piensas antes de hablar?": "introvertido",
    "¿Prefieres escuchar a hablar?": "introvertido",
    "¿Te cuesta hacer amigos nuevos?": "introvertido",
    "¿Eres más productivo en soledad?": "introvertido",

    "¿Te gusta estar con mucha gente?": "extrovertido",
    "¿Disfrutas de eventos sociales?": "extrovertido",
    "¿Tienes facilidad para iniciar conversaciones?": "extrovertido",
    "¿Te gusta salir con frecuencia?": "extrovertido",
    "¿Hablas más de lo que escuchas?": "extrovertido",
    "¿Tu círculo social es amplio?": "extrovertido",
    "¿Te gusta ser el centro de atención?": "extrovertido",
    "¿Te emociona conocer gente nueva?": "extrovertido",
    "¿Publicas mucho en redes sociales?": "extrovertido",
    "¿Te energiza estar con otros?": "extrovertido"
}

def clasificar_personalidad(respuestas_dict):
    intro, extro = 0, 0
    for pregunta, respuesta in respuestas_dict.items():
        if respuesta:
            tipo = reglas_preguntas.get(pregunta)
            if tipo == "introvertido":
                intro += 1
            elif tipo == "extrovertido":
                extro += 1
    if intro > extro:
        return "Introvertido"
    elif extro > intro:
        return "Extrovertido"
    else:
        return "Introvertido"  # predeterminado si hay empate