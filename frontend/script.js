let chartInstance = null;

document.getElementById('pricing-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  // 1. Capturar valores digitados
  const custo = parseFloat(document.getElementById('custo').value);
  const taxa = parseFloat(document.getElementById('taxa').value) / 100;
  const margemDesejada = parseFloat(document.getElementById('margem_desejada').value) / 100;
  const margemMinima = parseFloat(document.getElementById('margem_minima').value) / 100;
  
  // Converter string de concorrentes para array de números
  const concorrentesRaw = document.getElementById('concorrentes').value;
  const precosConcorrentes = concorrentesRaw
    .split(',')
    .map(item => parseFloat(item.trim()))
    .filter(item => !isNaN(item));

  if (precosConcorrentes.length === 0) {
    alert('Insira pelo menos um preço de concorrente válido.');
    return;
  }

  // 2. Montar Payload JSON conforme o Pydantic aguarda
  const payload = {
    custo_produto: custo,
    taxa_marketplace: taxa,
    margem_desejada: margemDesejada,
    margem_minima: margemMinima,
    precos_concorrentes: precosConcorrentes
  };

  try {
    // 3. Chamada Fetch para a API Python FastAPI
    const response = await fetch('http://127.0.0.1:8000/api/v1/precificar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Erro ao processar precificação na API.');
    }

    const data = await response.json();
    
    // 4. Renderizar resultados no painel
    exibirResultados(data, custo);

  } catch (error) {
    alert('Não foi possível conectar com a API FastAPI. Verifique se o servidor Uvicorn está rodando!');
    console.error(error);
  }
});

function exibirResultados(data, custo) {
  document.getElementById('results-panel').style.display = 'block';

  // Atualizar KPIs
  document.getElementById('kpi-preco').innerText = `R$ ${data.preco_sugerido.toFixed(2)}`;
  document.getElementById('kpi-margem').innerText = `${(data.margem_efetiva * 100).toFixed(1)}%`;
  document.getElementById('kpi-mercado').innerText = `R$ ${data.media_concorrente_ajustada.toFixed(2)}`;

  // Atualizar Badge de Status
  const badge = document.getElementById('status-badge');
  badge.className = `badge badge-${data.status_viabilidade}`;
  badge.innerText = data.status_viabilidade.replace('_', ' ');

  // Atualizar Alertas
  const alertasBox = document.getElementById('alertas-container');
  if (data.alertas && data.alertas.length > 0) {
    alertasBox.style.display = 'block';
    alertasBox.innerHTML = data.alertas.map(a => `<p>⚠️ ${a}</p>`).join('');
  } else {
    alertasBox.style.display = 'none';
  }

  // Renderizar / Atualizar Gráfico com Chart.js
  renderizarGrafico(custo, data.preco_sugerido, data.media_concorrente_ajustada);
}

function renderizarGrafico(custo, precoSugerido, mediaMercado) {
  const ctx = document.getElementById('pricingChart').getContext('2d');

  if (chartInstance) {
    chartInstance.destroy(); // Destrói gráfico anterior antes de criar novo
  }

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Custo', 'Preço Sugerido', 'Média Mercado'],
      datasets: [{
        label: 'Valores (R$)',
        data: [custo, precoSugerido, mediaMercado],
        backgroundColor: ['#e74c3c', '#2ecc71', '#3498db'],
        borderRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      }
    }
  });
}