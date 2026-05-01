from tutor import responder

print("=== Tutor IA Socrático de Bases de Datos ===")

while True:
    pregunta = input("\nPregunta (o 'salir'): ")

    if pregunta.lower() == "salir":
        break

    respuesta = responder(pregunta)

    print("\nTutor IA:\n")
    print(respuesta)