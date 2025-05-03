import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st

def carregar_dados():
    # Encontrar o caminho correto do arquivo independente de onde o script é executado
    script_path = Path(__file__).parent.parent  # Sobe dois níveis: app -> analise-temporal-streamlit
    data_path = script_path / "data" / "ocorrencias2024.csv"
    
    # Verificar se o arquivo existe
    if not data_path.exists():
        # Se não existir, cria um DataFrame de exemplo para desenvolvimento
        st.warning(f"Arquivo não encontrado em: {data_path}. Usando dados de exemplo.")
        
        # Criar dados de exemplo
        cidades = ['Recife', 'Olinda', 'Jaboatão', 'Paulista', 'Caruaru']
        tipos = ['Incêndio', 'Acidente', 'Resgate', 'Atendimento Clínico', 'Queda']
        
        # Gerar 100 registros aleatórios
        n_registros = 100
        np.random.seed(42)  # Para reprodutibilidade
        
        dados = {
            'id': list(range(1, n_registros + 1)),
            'cidade': np.random.choice(cidades, n_registros),
            'tipo': np.random.choice(tipos, n_registros),
            'data_hora': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 90), 
                                                          hours=np.random.randint(0, 24),
                                                          minutes=np.random.randint(0, 60)) 
                         for _ in range(n_registros)]
        }
        
        dados = pd.DataFrame(dados)
    else:
        # Se existir, carrega o arquivo CSV com separador correto
        dados = pd.read_csv(data_path, sep=";")
        # Unir data e hora em uma coluna datetime
        dados['data_hora'] = pd.to_datetime(
            dados['data'] + ' ' + dados['hora_minuto'],
            errors='coerce'
        )
        # Padronizar nomes de colunas para o restante do app
        dados.rename(columns={
            'municipio': 'cidade'
        }, inplace=True)
        # Ajustar coluna 'tipo' se necessário (já existe)
        # Se não houver coluna 'tipo', pode ser necessário ajustar para 'subtipo' ou outro

    # Processar colunas de data e hora
    dados['dia_semana'] = dados['data_hora'].dt.day_name()
    dados['horario'] = dados['data_hora'].dt.hour
    
    # Traduzir dias da semana para português, se necessário
    mapeamento_dias = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    dados['dia_semana'] = dados['dia_semana'].map(mapeamento_dias)
    
    # Classificar ocorrências por período do dia
    def classificar_periodo(hora):
        if 5 <= hora < 12:
            return 'Manhã'
        elif 12 <= hora < 18:
            return 'Tarde'
        elif 18 <= hora < 22:
            return 'Noite'
        else:
            return 'Madrugada'
    
    dados['periodo'] = dados['horario'].apply(classificar_periodo)
    
    # Calcular métricas importantes que serão usadas no storytelling
    dados['fim_de_semana'] = dados['dia_semana'].isin(['Sábado', 'Domingo'])
    
    return dados

def gerar_insights(dados):
    """
    Gera insights automáticos a partir dos dados para apoiar a narrativa
    """
    insights = {}
    
    # Determinar o dia da semana com mais ocorrências
    contagem_por_dia = dados['dia_semana'].value_counts()
    insights['dia_pico'] = contagem_por_dia.idxmax()
    insights['contagem_dia_pico'] = contagem_por_dia.max()
    
    # Determinar o horário com mais ocorrências
    contagem_por_hora = dados['horario'].value_counts()
    insights['hora_pico'] = contagem_por_hora.idxmax()
    insights['contagem_hora_pico'] = contagem_por_hora.max()
    
    # Comparar dias úteis vs fim de semana
    ocorrencias_fim_de_semana = dados[dados['fim_de_semana']].shape[0]
    ocorrencias_dia_util = dados[~dados['fim_de_semana']].shape[0]
    
    insights['media_fim_de_semana'] = ocorrencias_fim_de_semana / 2 if ocorrencias_fim_de_semana > 0 else 0
    insights['media_dia_util'] = ocorrencias_dia_util / 5 if ocorrencias_dia_util > 0 else 0
    insights['diferenca_percentual'] = ((insights['media_fim_de_semana'] / insights['media_dia_util']) - 1) * 100 if insights['media_dia_util'] > 0 else 0
    
    # Tipo mais comum por período
    por_periodo = {}
    for periodo in dados['periodo'].unique():
        tipo_comum = dados[dados['periodo'] == periodo]['tipo'].value_counts().idxmax()
        por_periodo[periodo] = tipo_comum
    
    insights['tipo_por_periodo'] = por_periodo
    
    return insights
