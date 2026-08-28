from fastapi import APIRouter, HTTPException

from app.schemas.product import PricingRequest, PricingResponse
from app.services.calculator import calcular_precificacao

router = APIRouter(prefix="/api/v1", tags=["Precificação"])


@router.post("/precificar", response_model=PricingResponse)
def precificar_produto(dados: PricingRequest):
    try:
        resultado = calcular_precificacao(dados)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a precificação: {str(e)}",
        )
