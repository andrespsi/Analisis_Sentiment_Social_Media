# main.py
import uvicorn
import sys
import os

# --- INICIO DE LA SOLUCIÓN ---
# Esto añade la carpeta raíz del proyecto (Sentiment+) a la lista de rutas de Python.
# De esta forma, Python siempre sabrá dónde encontrar el módulo 'src'.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# --- FIN DE LA SOLUCIÓN ---

if __name__ == "__main__":
    uvicorn.run("src.api.endpoints:app", host="127.0.0.1", port=8000, reload=True)