from typing import List

from pydantic import BaseModel, Field


class PricingRequest(BaseModel):
    custo_produto: float = Field(..., gt=0, description="Custo Bse do Produto")
    taxa_marketplace: float = Field(
        ..., ge=0, lt=1, description="Taxa da Plataforma de Marketplace"
    )
    margem_desejada: float = Field(
        ..., ge=0, lt=1, description="Margem de Lucro desejada"
    )
    margem_minima: float = Field(
        ..., ge=0, lt=1, description="Piso mínimo de margem de segurança"
    )
    precos_concorrentes: List[float] = Field(
        ..., description="Lista de preços praticados pelo Mercado"
    )


class PricingResponse(BaseModel):
    preco_sugerido: float
    margem_efetiva: float
    media_concorrente_ajustada: float
    status_viabilidade: str
    alertas: List[str]
