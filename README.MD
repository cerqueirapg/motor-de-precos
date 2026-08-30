# 🛒 Motor de Recomendação de Preços para E-commerce

Aplicação web desenvolvida para auxílio na precificação de produtos em plataformas de e-commerce. O sistema analisa os custos operacionais, calcula a margem de lucro desejada e aplica algoritmos estatísticos para ajustar o preço final frente à concorrência do mercado.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic
- **Frontend:** HTML5 Semântico, CSS3 (Grid & Flexbox), JavaScript ES6+ (Fetch API, Async/Await), Chart.js
- **Arquitetura & Boas Práticas:** Clean Architecture (Separação entre schemas, routers e services), Filtro Estatístico IQR, CORS liberado para integrações local/web.

---

## ⚙️ Regras de Negócio e Algoritmo

1. **Tratamento de Outliers (IQR):** O sistema analisa a lista de preços praticados pelos concorrentes e aplica o *Intervalo Interquartil (IQR)* para descartar valores discrepantes (preços anômalos) antes de calcular a média do mercado.
2. **Ajuste Automático de Margem:** Se o preço calculado ultrapassar **15% da média do mercado**, o sistema tenta reduzir o valor de venda até o teto competitivo.
3. **Piso de Segurança:** Se a redução do preço ferir a `margem_minima` estipulada pelo usuário, a aplicação trava o valor no limite da margem de segurança e emite um alerta de *Incompetitividade*.

---

## 📂 Estrutura do Repositório

```text
motor-de-precos/
├── app/
│   ├── main.py              # Ponto de entrada e configuração do FastAPI
│   ├── routers/             # Definição dos endpoints REST
│   │   └── pricing.py
│   ├── schemas/             # Validação de dados com Pydantic
│   │   └── product.py
│   └── services/            # Lógica de negócio e cálculos estatísticos
│       └── calculator.py
├── frontend/
│   ├── index.html           # Interface do usuário
│   ├── styles.css           # Estilização responsiva
│   └── script.js            # Integração assíncrona com a API
└── README.md

```
## ⚙️ Como Executar o Projeto Localmente
### Pré-requisitos
- Python instalado (versão 3.10 ou superior)
- Extensão Live Server no VS Code (ou qualquer servidor HTTP estático)

1. **Clonar o repositório:**
```bash
git clone https://github.com/seu-usuario/motor-de-precos.git
cd motor-de-precos
```
2. **Configurar o Ambiente Virtual e Dependências**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pydantic pytest
```
3. **Iniciar o Backend (FastAPI)**
```powershell
python -m uvicorn app.main:app --reload
```
- A API estará acessível em http://127.0.0.1:8000. A documentação Swagger pode ser acessada em http://127.0.0.1:8000/docs.

4. **Iniciar o Frontend**
- Abra a pasta frontend/index.html com o Live Server no VS Code para navegar na interface gráfica e realizar as simulações.
---