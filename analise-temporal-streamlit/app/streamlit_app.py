import streamlit as st
from graficos import gerar_graficos
from utils import carregar_dados, gerar_insights
import pandas as pd

# Configuração inicial
st.set_page_config(page_title="Análise Temporal de Ocorrências 2024", layout="wide")

# Título do dashboard
st.title("📊 Análise Temporal de Ocorrências de Emergência 2024")
st.markdown("### 📖 Uma história baseada em dados sobre emergências de saúde em Pernambuco")

# Carregar dados
dados = carregar_dados()

# Sidebar com filtros interativos
st.sidebar.header("Filtros")
cidade = st.sidebar.selectbox("Selecione a cidade", dados['cidade'].unique())
tipos_default = dados['tipo'].unique().tolist()[:1]  # Seleciona o primeiro tipo como padrão
tipo_ocorrencia = st.sidebar.multiselect("Tipos de Ocorrência", 
                                       options=dados['tipo'].unique(), 
                                       default=tipos_default)

# Verificar se há tipos selecionados para evitar filtros vazios
if not tipo_ocorrencia:
    tipo_ocorrencia = dados['tipo'].unique().tolist()
    st.sidebar.warning("Nenhum tipo selecionado. Mostrando todos os tipos.")

# Filtrar dados
dados_filtrados = dados[(dados['cidade'] == cidade) & (dados['tipo'].isin(tipo_ocorrencia))]

# Gerar insights para a narrativa
insights = gerar_insights(dados_filtrados)

# Introdução à narrativa
st.markdown("""
## 🔍 O Contexto

Vamos explorar como as emergências médicas em Pernambuco se distribuem ao longo do tempo.
Esta análise pode ajudar gestores públicos a otimizar recursos e melhorar o tempo de resposta.

Acompanhe nossa jornada pelos dados e descubra padrões temporais que podem salvar vidas!
""")

# Primeiro capítulo da história: Panorama geral
st.markdown("## 📆 Quando ocorrem mais chamados de emergência?")

# KPIs principais - Métricas destacadas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Dia com Mais Ocorrências", 
              value=insights['dia_pico'], 
              delta=f"{insights['contagem_dia_pico']} chamados")

with col2:
    st.metric(label="Horário de Pico", 
              value=f"{insights['hora_pico']}h", 
              delta=f"{insights['contagem_hora_pico']} chamados")

with col3:
    st.metric(label="Diferença Fim de Semana vs. Dia Útil", 
              value=f"{abs(insights['diferenca_percentual']):.1f}%", 
              delta="mais nos fins de semana" if insights['diferenca_percentual'] > 0 else "mais nos dias úteis")

# Gerar visualizações com comentários narrativos
gerar_graficos(dados_filtrados)

# Capítulo 2: Períodos do dia e tipos de emergência
st.markdown("""
## 🌓 Períodos Críticos e Tipos de Emergência

Diferentes momentos do dia apresentam desafios únicos para as equipes de emergência.
Vamos analisar como os tipos de ocorrência se distribuem nos diferentes períodos.
""")

# Gráfico de tipos de ocorrência por período
periodo_counts = dados_filtrados.groupby(['periodo', 'tipo']).size().reset_index(name='contagem')
pivot_table = periodo_counts.pivot(index='tipo', columns='periodo', values='contagem').fillna(0)

st.markdown("### Distribuição dos tipos de ocorrência por período do dia")
st.bar_chart(pivot_table)

# Insights sobre períodos
st.markdown("""
### Insights importantes:
""")

for periodo, tipo in insights['tipo_por_periodo'].items():
    st.markdown(f"- No período da **{periodo}**, as ocorrências mais comuns são do tipo **{tipo}**")

# Capítulo 3: Recomendações e conclusões
st.markdown("""
## 💡 O Que Podemos Aprender?

Com base na análise temporal, podemos extrair algumas lições valiosas para otimizar o atendimento de emergência:
""")

st.markdown(f"""
1. **Escala de equipes**: Reforçar equipes às {insights['hora_pico']}h e nos dias de {insights['dia_pico']}
2. **Tipos de treinamento**: Priorizar treinamento em {insights['tipo_por_periodo']['Madrugada']} para equipes do turno noturno
3. **Distribuição de recursos**: Ajustar a disponibilidade de ambulâncias conforme os padrões temporais identificados

Estes insights podem ajudar gestores a tomar decisões baseadas em dados, potencialmente salvando vidas através de uma melhor alocação de recursos!
""")

# Footer com informações adicionais
st.markdown("---")
st.markdown("📊 **Data Storytelling**: Análise Temporal de Ocorrências de Emergência em Pernambuco")

# Linha corrigida com tratamento de erro para evitar problemas com a data
try:
    if 'data' in dados.columns and pd.api.types.is_datetime64_any_dtype(dados['data']):
        data_atualizacao = dados['data'].max().strftime('%d/%m/%Y')
    else:
        data_atualizacao = "Dezembro/2024"  # Data padrão caso não consiga extrair
    st.markdown(f"Dados atualizados até: {data_atualizacao}")
except Exception as e:
    st.markdown("Dados de Dezembro/2024")
    
st.markdown("📧✨ Ficou com dúvida? Chama o Cassio Santos 🤠 ou a Sara Lopes 🌟!")
