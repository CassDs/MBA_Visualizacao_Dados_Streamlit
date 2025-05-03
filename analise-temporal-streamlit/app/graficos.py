import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

def gerar_graficos(dados):
    st.write(f"Analisando {len(dados)} ocorrências")
    
    # Verifica se o dataframe está vazio
    if len(dados) == 0:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # 1. Gráfico de barras: Ocorrências por dia da semana
    st.subheader("Ocorrências por Dia da Semana")
    
    # Ordenar dias da semana corretamente
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                  'Friday', 'Saturday', 'Sunday']
    
    # Versão em português se necessário
    ordem_dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 
                    'Sexta', 'Sábado', 'Domingo']
    
    # Detecta qual idioma está sendo usado nos dados
    dias_unicos = dados['dia_semana'].unique()
    if 'Segunda' in dias_unicos or 'Domingo' in dias_unicos:
        ordem = ordem_dias_pt
    else:
        ordem = ordem_dias
        
    # Gráfico com Plotly (mais interativo)
    ocorrencias_por_dia = dados['dia_semana'].value_counts().reset_index()
    ocorrencias_por_dia.columns = ['Dia da Semana', 'Quantidade']
    
    # Reordenar o dataframe
    if ordem[0] in ocorrencias_por_dia['Dia da Semana'].values:
        ocorrencias_por_dia['Dia da Semana'] = pd.Categorical(
            ocorrencias_por_dia['Dia da Semana'], 
            categories=ordem, 
            ordered=True
        )
        ocorrencias_por_dia = ocorrencias_por_dia.sort_values('Dia da Semana')
        
    fig = px.bar(
        ocorrencias_por_dia, 
        x='Dia da Semana', 
        y='Quantidade',
        color='Quantidade',
        title='Distribuição de Ocorrências por Dia da Semana',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2. Gráfico de linha: Ocorrências por horário
    st.subheader("Ocorrências por Horário")
    ocorrencias_por_horario = dados.groupby('horario').size().reset_index(name='count')
    
    fig = px.line(
        ocorrencias_por_horario, 
        x='horario', 
        y='count',
        title='Distribuição de Ocorrências por Hora do Dia',
        labels={'horario': 'Hora', 'count': 'Quantidade'},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. Comparação dias úteis vs. fim de semana
    st.subheader("Dias Úteis vs. Fim de Semana")
    
    # Adicionar coluna para indicar dia útil ou fim de semana
    dados['tipo_dia'] = dados['dia_semana'].apply(
        lambda x: 'Fim de Semana' if x in ['Saturday', 'Sunday', 'Sábado', 'Domingo'] else 'Dia Útil'
    )
    
    # Gráfico de barras agrupadas por tipo de ocorrência
    ocorrencias_por_tipo_dia = dados.groupby(['tipo_dia', 'tipo']).size().reset_index(name='count')
    
    fig = px.bar(
        ocorrencias_por_tipo_dia, 
        x='tipo', 
        y='count',
        color='tipo_dia',
        barmode='group',
        title='Tipos de Ocorrência: Dias Úteis vs. Fim de Semana',
        labels={'tipo': 'Tipo de Ocorrência', 'count': 'Quantidade', 'tipo_dia': 'Tipo de Dia'}
    )
    st.plotly_chart(fig, use_container_width=True)
