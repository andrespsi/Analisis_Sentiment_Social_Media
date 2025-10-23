from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.utils.preprocesamiento import LimpiaTexto
from src.analysis.analizador import AnalizadorSentimiento
import time
import asyncio

app = FastAPI(
    title="API de Análisis de Sentimiento en Español",
    description="Servicio para analizar sentimiento de textos en español extraídos de redes sociales. Utiliza preprocesamiento avanzado y modelos de IA especializados.",
    version="1.0.0"
)

# --- INICIO DE LA CORRECCIÓN ---
# Usamos un middleware de FastAPI, que es la forma correcta de ejecutar código
# en cada petición (como medir el tiempo) sin interferir con los parámetros del endpoint.

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware para medir el tiempo de respuesta de cada petición y añadirlo
    a una cabecera personalizada en la respuesta.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Response-Time-ms"] = str(int(process_time * 1000))
    return response

# --- FIN DE LA CORRECCIÓN ---


# Instancias únicas de los componentes para que se carguen una sola vez
limpiador = LimpiaTexto()
analizador = AnalizadorSentimiento()


class TextoEntrada(BaseModel):
    """
    Modelo de datos para la entrada de la API.
    Define qué debe contener el cuerpo (body) de la petición POST.
    """
    texto: str = Field(..., example="¡Me encanta este producto ❤️, lo recomiendo totalmente!")


@app.post(
    "/analizar",
    summary="Analiza el sentimiento de un texto en español",
    response_description="Resultados del análisis de sentimiento",
    tags=["Sentimiento"],
)
async def analizar_sentimiento(entrada: TextoEntrada):
    """
    Este endpoint recibe un texto en español y devuelve un análisis de sentimiento completo.

    - **Procesa el texto** para limpiarlo (quita URLs, emojis, stopwords, etc.).
    - **Analiza el texto limpio** usando un modelo de IA para determinar el sentimiento.
    - **Retorna un JSON** con el texto original, el texto limpio y el resultado del análisis.
    """
    texto_original = entrada.texto
    try:
        # 1. Limpiar el texto de entrada
        texto_limpio = limpiador.limpiar(texto_original)

        # 2. Analizar el texto limpio
        resultado = await analizador.analizar(texto_limpio)

        # 3. Preparar y devolver la respuesta exitosa
        response_content = {
            "texto_original": texto_original,
            "texto_limpio": texto_limpio,
            "resultado": resultado
        }
        return JSONResponse(content=response_content)

    except Exception as e:
        # Manejo de errores por si algo falla durante el proceso
        error_content = {
            "error": str(e),
            "texto_original": texto_original
        }
        return JSONResponse(content=error_content, status_code=500)