from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analizar")
async def analizar_marquilla(imagen: UploadFile = File(...)):
    contenido = await imagen.read()
    imagen_base64 = base64.b64encode(contenido).decode("utf-8")
    
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Eres un experto en cuidado de ropa. Analiza esta imagen de una marquilla de ropa e identifica todos los símbolos de lavado que veas. 
                        Para cada símbolo encontrado indica:
                        1. Nombre del símbolo
                        2. Qué significa
                        3. Instrucción específica de lavado
                        
                        Al final genera un resumen completo de instrucciones de lavado para esta prenda.
                        Responde en español."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagen_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    return {"resultado": respuesta.choices[0].message.content}

@app.get("/")
def root():
    return {"mensaje": "Servicio de análisis de marquillas activo"}