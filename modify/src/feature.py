import pandas as pd
import json
import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "processed", "songs_clean.csv")
output_path = os.path.join(BASE_DIR, "data", "processed", "mood_profiles.json")

# Cargar datos
df = pd.read_csv(data_path)

# Agrupar por estado de ánimo y calcular medias
moods = df.groupby("mood_inferido")[["energy", "valence", "tempo"]].mean().to_dict()

# Guardar en JSON
with open(output_path, "w") as f:
    json.dump(moods, f, indent=4)

print(f"✅ Archivo de perfiles emocionales guardado en: {output_path}")
  