def recommend_actions(match: dict) -> list:
    acciones = []

    if match["score"] >= 0.7:
        acciones.append("Tu perfil encaja muy bien. Prepara una carta personalizada.")
    elif match["score"] >= 0.4:
        acciones.append("Puedes aplicar, pero mejora las habilidades faltantes.")
    else:
        acciones.append("Revisa si esta oferta encaja con tu trayectoria.")

    if match["missing_skills"]:
        acciones.append("Habilidades a mejorar: " + ", ".join(match["missing_skills"]))

    return acciones
