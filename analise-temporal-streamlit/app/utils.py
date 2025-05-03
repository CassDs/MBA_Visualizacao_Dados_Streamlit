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
    
    return dados
