import sqlite3
import pandas as pd
import os

# Obtener la ruta base del proyecto (carpeta modify/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas a los archivos
data_path = os.path.join(BASE_DIR, "data", "processed", "songs_clean.csv")
db_dir = os.path.join(BASE_DIR, "db")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "moodify.db")
init_sql = os.path.join(db_dir, "init_sql.sql")

# Cargar el CSV limpio
df = pd.read_csv(data_path)

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect(db_path)

# Crear tabla si no existe
with open(init_sql, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

# Insertar datos
df.to_sql("songs", conn, if_exists="replace", index=False)

print(f"✅ Base de datos creada correctamente en: {db_path}")

# Comprobar que funciona
check = pd.read_sql_query("SELECT genre, COUNT(*) as num FROM songs GROUP BY genre LIMIT 5;", conn)
print(check)

conn.close()
