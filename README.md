
# 📊 Análise Temporal de Ocorrências de Emergência 2024

Este projeto tem como objetivo identificar **os dias e horários mais críticos** para chamadas de emergência no estado de Pernambuco, com base em um conjunto de dados reais de ocorrências de 2024.

A aplicação final será apresentada como um **dashboard interativo usando Streamlit**, com visualizações dinâmicas e uma narrativa baseada em dados.

---

## 🎯 Público-Alvo

Este projeto é voltado especialmente para:

- **Gestores públicos de saúde e segurança** (SAMU, Bombeiros, Secretarias Municipais de Saúde);
- **Tomadores de decisão e analistas de políticas públicas**;
- **Acadêmicos e pesquisadores em saúde coletiva e epidemiologia**;
- **Profissionais de planejamento urbano e emergencial**.

A ideia é fornecer **subsídios visuais e analíticos** para otimizar o tempo-resposta, prever demandas e escalar equipes em horários de maior risco.

---

## 🗂 Estrutura do Projeto

```
📁 analise-temporal-streamlit/
├── 📂 data/
│   └── ocorrencias2024.csv         # Conjunto de dados bruto
│
├── 📂 app/
│   └── streamlit_app.py            # Aplicação principal com Streamlit
│   └── graficos.py                 # Módulo com funções gráficas
│   └── utils.py                    # Funções auxiliares
│
├── 📂 assets/
│   └── imagens, ícones e banners
│
├── 📂 reports/
│   └── storytelling.md             # Roteiro da narrativa e insights
│
├── README.md                       # Este arquivo
└── requirements.txt                # Bibliotecas utilizadas
```

---

## 🔍 Perguntas Guiadoras

- Quais dias da semana concentram mais emergências?
- Existem horários de pico durante o dia?
- Há diferenças entre dias úteis e finais de semana?
- Certos tipos de ocorrência são mais comuns em horários específicos?

---

## 📊 Tecnologias Utilizadas

- `Python 3.10+`
- `Pandas`, `NumPy`
- `Matplotlib`, `Seaborn`, `Plotly`
- `Streamlit` (visualização interativa)

---

## 🚀 Como Executar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/CassDs/MBA_Visualizacao_Dados_Streamlit.git
cd analise-temporal-streamlit
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Rode o app:
```bash
streamlit run app/streamlit_app.py
```

---

## 🧠 Resultados Esperados

- **Dashboard interativo** com filtros por cidade, tipo e horário.
- **Storytelling visual** com insights baseados em padrões temporais.
- **Recomendações práticas** para escala de equipes, cobertura emergencial e políticas públicas.

---


## 📝 Licença

MIT License

---

> Desenvolvido por Cássio Santos e Sara Lopes como parte do Desafio "Data Storytelling - Visualização de Dados".
