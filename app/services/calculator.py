from typing import List, Tuple

from app.schemas.product import PricingRequest, PricingResponse


def filtrar_outliers_iqr(precos: List[float]) -> float:
    """
    Filtra preços discrepantes usando o Intervalo Interquartil (IQR)
    e retorna a média ajustada dos concorrentes.
    """
    if not precos:
        return 0.0

    precos_ordenados = sorted(precos)
    n = len(precos_ordenados)

    # Se houver poucos dados, calcula a média simples diretamente
    if n < 4:
        return sum(precos_ordenados) / n

    # Posições dos quartis Q1 (25%) e Q3 (75%)
    q1 = precos_ordenados[int(n * 0.25)]
    q3 = precos_ordenados[int(n * 0.75)]
    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    # Filtra apenas os preços dentro do intervalo seguro
    precos_validos = [
        p for p in precos_ordenados if limite_inferior <= p <= limite_superior
    ]

    # Se o filtro remover tudo por algum motivo, usa a lista original
    if not precos_validos:
        precos_validos = precos_ordenados

    return sum(precos_validos) / len(precos_validos)


def calcular_precificacao(dados: PricingRequest) -> PricingResponse:
    alertas = []

    # 1. Obter a média dos concorrentes filtrando outliers
    media_concorrentes = filtrar_outliers_iqr(dados.precos_concorrentes)

    # 2. Calcular Preço Alvo ideal
    # Fórmula: Custo / (1 - (Margem Desejada + Taxa Marketplace))
    divisor_ideal = 1.0 - (dados.margem_desejada + dados.taxa_marketplace)

    if divisor_ideal <= 0:
        # Se a soma das taxas ultrapassar 100%, força um divisor mínimo seguro
        divisor_ideal = 0.01
        alertas.append("Margem desejada + taxa excedem o limite operacional.")

    preco_alvo = dados.custo_produto / divisor_ideal
    margem_efetiva = dados.margem_desejada
    status = "excelente"

    # 3. Validar teto de competitividade (se está 15% acima da média do mercado)
    teto_mercado = media_concorrentes * 1.15 if media_concorrentes > 0 else preco_alvo

    if preco_alvo > teto_mercado:
        # Tenta ajustar o preço para o teto competitivo
        preco_ajustado = teto_mercado

        # Recalcula a margem obtida com o preço mais baixo
        # Fórmula da margem: 1 - (Custo / Preço) - Taxa
        nova_margem = (
            1.0 - (dados.custo_produto / preco_ajustado) - dados.taxa_marketplace
        )

        if nova_margem < dados.margem_minima:
            # Não é seguro baixar tanto o preço, aciona o piso de margem mínima
            divisor_minimo = 1.0 - (dados.margem_minima + dados.taxa_marketplace)
            preco_alvo = dados.custo_produto / (
                divisor_minimo if divisor_minimo > 0 else 0.01
            )
            margem_efetiva = dados.margem_minima
            status = "incompetitivo"
            alertas.append(
                "Preço acima do mercado. Não foi possível reduzir o valor sem violar a margem mínima de segurança."
            )
        else:
            preco_alvo = preco_ajustado
            margem_efetiva = nova_margem
            status = "competitivo_ajustado"
            alertas.append(
                "Preço ajustado para baixo para se manter competitivo frente ao mercado."
            )

    return PricingResponse(
        preco_sugerido=round(preco_alvo, 2),
        margem_efetiva=round(margem_efetiva, 4),
        media_concorrente_ajustada=round(media_concorrentes, 2),
        status_viabilidade=status,
        alertas=alertas,
    )
