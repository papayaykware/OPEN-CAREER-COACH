# inicializar_mvp.py
# Generando el MVP funcional siguiendo la recomendación de DeepSeek
# con visión arquitectónica propia para OPEN-CAREER-COACH

import os

# Detecta automáticamente la carpeta 'Modulos' donde se ejecuta el script
base_path = os.path.dirname(os.path.abspath(__file__))

# Crear estructura de directorios para el MVP
os.makedirs(f"{base_path}/src/utils", exist_ok=True)
os.makedirs(f"{base_path}/src/cv_parser", exist_ok=True)
os.makedirs(f"{base_path}/src/job_parser", exist_ok=True)
os.makedirs(f"{base_path}/src/matching", exist_ok=True)
os.makedirs(f"{base_path}/src/ui", exist_ok=True)
os.makedirs(f"{base_path}/data/sample_cvs", exist_ok=True)
os.makedirs(f"{base_path}/data/sample_jobs", exist_ok=True)

# Crear archivos __init__.py para empaquetado Python
modulos_python = ["src", "src/utils", "src/cv_parser", "src/job_parser", "src/matching", "src/ui"]
for d in modulos_python:
    init_file = f"{base_path}/{d}/__init__.py"
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("")

print("🚀 Estructura MVP creada correctamente dentro de la carpeta Modulos.")
