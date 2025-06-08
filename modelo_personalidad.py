import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def entrenar_modelo(path='datos_entrenamiento.json'):
    df = pd.read_json(path, encoding='utf-8')

    # Reemplazar Sí/No por 1/0
    df.replace({"Si": 1, "Sí": 1, "S\u00ed": 1, "No": 0}, inplace=True)
    df = df.infer_objects(copy=False)  # Forzar que los valores sean numéricos

    # Separar variables predictoras y la variable objetivo
    X = df.drop(columns=["Personality"])
    y = df["Personality"]

    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)

    return modelo, X.columns.tolist()

def predecir_personalidad(respuestas, path='datos_entrenamiento.json'):
    modelo, columnas = entrenar_modelo(path)
    df = pd.DataFrame([respuestas], columns=columnas)
    prediccion = modelo.predict(df)[0]
    return prediccion