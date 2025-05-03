import streamlit as st
from graficos import gerar_graficos
from utils import carregar_dados

# Configuração inicial
st.set_page_config(page_title="Análise Temporal de Ocorrências 2024", layout="wide")

# Título do dashboard
st.title("📊 Análise Temporal de Ocorrências de Emergência 2024")

# Carregar dados
dados = carregar_dados()

# Filtros interativos
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

# Gerar gráficos
gerar_graficos(dados_filtrados)
