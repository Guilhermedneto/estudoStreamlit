import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statistics

# Dados dos campeões brasileiros até 2022
data = {
    'Ano': ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
            '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
    'Campeão': ['Cruzeiro', 'Santos', 'Corinthians', 'São Paulo', 'São Paulo', 'São Paulo', 'Flamengo', 'Fluminense', 'Corinthians', 'Fluminense',
                'Cruzeiro', 'Cruzeiro', 'Corinthians', 'Palmeiras', 'Corinthians', 'Palmeiras', 'Flamengo', 'Flamengo', 'Flamengo', 'Palmeiras'],
    'Pontuação': [100, 89, 81, 78, 77, 75, 67, 71, 71, 77, 76, 80, 81, 80, 72, 80, 90, 71, 71, 81]
}

# Criar um DataFrame a partir dos dados
df = pd.DataFrame(data)

# Função para calcular a média aritmética
def calculate_mean(selected_teams):
    selected_df = df[df['Campeão'].isin(selected_teams)]
    mean_value = selected_df['Pontuação'].mean()
    overall_mean = df['Pontuação'].mean()
    return mean_value, overall_mean

# Função para mostrar o card com a média da equipe selecionada
def show_team_card(selected_team):
    team_mean = df[df['Campeão'] == selected_team]['Pontuação'].mean()
    st.sidebar.subheader(f'Média de Pontos de {selected_team}')
    st.sidebar.write(f'{selected_team}: {team_mean:.2f}')

# Barra lateral com menu suspenso para selecionar a página
selected_page = st.sidebar.selectbox('Selecione a página:', ['Tabela', 'Gráfico de Barras', 'Gráfico de Linhas', 'Gráfico de Pizza', 'Gráfico de Dispersão', 'Gráfico de Barra Empilhada', 'Gráfico de Radar e Média Aritmética'])

# Mostrar a página selecionada
if selected_page == 'Tabela':
    st.title('Campeões Brasileiros de Futebol (Pontos Corridos) - Tabela')
    st.dataframe(df, width=600, height=400)
elif selected_page == 'Gráfico de Barras':
    st.title('Gráfico de Pontuação dos Campeões (Barras)')
    st.sidebar.subheader('Gráfico de Pontuação dos Campeões')
    selected_years = st.sidebar.multiselect('Selecione os anos:', df['Ano'].tolist())
    filtered_df = df[df['Ano'].isin(selected_years)]

    # Gráfico de barras
    fig = px.bar(filtered_df, x='Campeão', y='Pontuação', title='Pontuação dos Campeões por Ano')

    # Mostrar o gráfico de barras
    st.plotly_chart(fig)

    # Selecionar a equipe no gráfico de barras
    selected_team = st.selectbox('Selecione uma equipe:', df['Campeão'].unique())
    show_team_card(selected_team)
elif selected_page == 'Gráfico de Linhas':
    st.title('Gráfico de Evolução da Pontuação dos Campeões (Linhas)')

    # Gráfico de linhas
    fig = go.Figure()

    for campeao in df['Campeão'].unique():
        campeao_df = df[df['Campeão'] == campeao]
        fig.add_trace(go.Scatter(x=campeao_df['Ano'], y=campeao_df['Pontuação'], mode='lines+markers', name=campeao))

    fig.update_layout(title='Evolução da Pontuação dos Campeões por Ano', xaxis_title='Ano', yaxis_title='Pontuação')
    st.plotly_chart(fig)
elif selected_page == 'Gráfico de Pizza':
    st.title('Gráfico de Distribuição dos Títulos por Equipe (Pizza)')

    # Contagem de títulos por equipe
    count_by_team = df['Campeão'].value_counts()

    # Gráfico de pizza
    fig = px.pie(count_by_team, values=count_by_team.values, names=count_by_team.index, title='Distribuição dos Títulos por Equipe')
    st.plotly_chart(fig)
elif selected_page == 'Gráfico de Dispersão':
    st.title('Gráfico de Dispersão da Pontuação dos Campeões (Dispersão)')

    # Gráfico de dispersão
    fig = px.scatter(df, x='Ano', y='Pontuação', color='Campeão', title='Dispersão da Pontuação dos Campeões por Ano')
    st.plotly_chart(fig)
elif selected_page == 'Gráfico de Barra Empilhada':
    st.title('Gráfico de Pontuação dos Campeões por Ano (Barra Empilhada)')

    # Gráfico de barra empilhada
    fig = px.bar(df, x='Ano', y='Pontuação', color='Campeão', title='Pontuação dos Campeões por Ano (Barra Empilhada)')
    st.plotly_chart(fig)

    # Selecionar a equipe no gráfico de barras
    selected_team = st.selectbox('Selecione uma equipe:', df['Campeão'].unique())
    show_team_card(selected_team)
elif selected_page == 'Gráfico de Radar e Média Aritmética':
    show_radar_chart()
