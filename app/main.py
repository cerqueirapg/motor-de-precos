from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pricing

app = FastAPI(
    title="Motor de Recomendação de Preços para E-commerce",
    description="API para cálculo de preço ideal com filtro de outliers e ajuste de margem.",
    version="1.0.0",
)

# Habilita CORS para que o Frontend HTML/JS consiga conversar com este Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite requisições de qualquer origem durante o desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas de precificação
app.include_router(pricing.router)


@app.get("/")
def home():
    return {"status": "API online", "documentacao": "/docs"}
