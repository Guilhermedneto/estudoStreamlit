import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dados dos campeões brasileiros até 2022
data = {
    'Ano': ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
            '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
    'Campeão': ['Cruzeiro', 'Santos', 'Corinthians', 'São Paulo', 'São Paulo', 'São Paulo', 'Flamengo', 'Fluminense',
                'Corinthians', 'Fluminense',
                'Cruzeiro', 'Cruzeiro', 'Corinthians', 'Palmeiras', 'Corinthians', 'Palmeiras', 'Flamengo', 'Flamengo',
                'Flamengo', 'Palmeiras'],
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


# Função para calcular a média ponderada
def calculate_weighted_mean(selected_teams):
    selected_df = df[df['Campeão'].isin(selected_teams)]
    weights = selected_df['Pontuação'] / selected_df['Pontuação'].sum()
    weighted_mean = (selected_df['Pontuação'] * weights).sum()
    return weighted_mean


# Função para calcular o desvio padrão
def calculate_standard_deviation(selected_teams):
    selected_df = df[df['Campeão'].isin(selected_teams)]
    std_deviation = selected_df['Pontuação'].std()
    return std_deviation


# Função para mostrar o card com as estatísticas da equipe selecionada
def show_team_card(selected_team):
    team_mean, overall_mean = calculate_mean([selected_team])
    weighted_mean = calculate_weighted_mean([selected_team])
    std_deviation = calculate_standard_deviation([selected_team])

    st.sidebar.subheader(f'Estatísticas de {selected_team}')
    st.sidebar.write(f'Média Aritmética: {team_mean:.2f}')
    st.sidebar.write(f'Média Ponderada: {weighted_mean:.2f}')
    st.sidebar.write(f'Desvio Padrão: {std_deviation:.2f}')


# Função para mostrar o gráfico de radar
def show_radar_chart():
    st.title('Gráfico de Radar com Média Aritmética, Média Ponderada e Desvio Padrão')

    # Selecionar uma equipe
    selected_team = st.selectbox('Selecione uma equipe:', df['Campeão'].unique())

    # Filtrar o DataFrame para a equipe selecionada
    team_data = df[df['Campeão'] == selected_team]

    # Calcular as estatísticas da equipe selecionada
    team_mean, overall_mean = calculate_mean([selected_team])
    weighted_mean = calculate_weighted_mean([selected_team])
    std_deviation = calculate_standard_deviation([selected_team])

    # Gráfico de radar
    fig = go.Figure()

    # Adicionar traço para a equipe selecionada
    fig.add_trace(go.Scatterpolar(
        r=[team_mean, weighted_mean, std_deviation],
        theta=['Média Aritmética', 'Média Ponderada', 'Desvio Padrão'],
        fill='toself',
        name=selected_team,
        text=f'Média Aritmética: {team_mean:.2f}, Média Ponderada: {weighted_mean:.2f}, Desvio Padrão: {std_deviation:.2f}'
    ))

    # Adicionar traço para a média geral
    overall_mean_data = df['Pontuação'].mean()
    overall_std_deviation = df['Pontuação'].std()

    fig.add_trace(go.Scatterpolar(
        r=[overall_mean, overall_mean_data, overall_std_deviation],
        theta=['Média Aritmética', 'Média Ponderada', 'Desvio Padrão'],
        fill='toself',
        name='Média Geral',
        text=f'Média Aritmética: {overall_mean:.2f}, Média Ponderada: {overall_mean_data:.2f}, Desvio Padrão: {overall_std_deviation:.2f}'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            ),
        ),
        showlegend=True
    )

    st.plotly_chart(fig)


# Barra lateral com menu suspenso para selecionar a página
selected_page = st.sidebar.selectbox('Selecione a página:',
                                     ['Tabela', 'Gráfico de Barras', 'Gráfico de Linhas', 'Gráfico de Pizza',
                                      'Gráfico de Dispersão', 'Gráfico de Barra Empilhada',
                                      'Gráfico de Radar e Média Aritmética'])

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
    fig = px.pie(count_by_team, values=count_by_team.values, names=count_by_team.index,
                 title='Distribuição dos Títulos por Equipe')
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
