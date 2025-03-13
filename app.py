import pandas as pd
import plotly.express as px
import streamlit as st

# ⬇️ Carregar dados do cronograma
caminho_arquivo = "dados/cronograma.xlsx"
df = pd.read_excel(caminho_arquivo, header=0)

# ⬇️ Converter colunas de datas para datetime
df["Início Previsto"] = pd.to_datetime(df["Início Previsto"])
df["Término Previsto"] = pd.to_datetime(df["Término Previsto"])
df["Início Real"] = pd.to_datetime(df["Início Real"], errors="coerce")
df["Término Real"] = pd.to_datetime(df["Término Real"], errors="coerce")

# ⬇️ Criar colunas finais: se houver dados reais, usar; caso contrário, usar previstos
df["Início Final"] = df["Início Real"].fillna(df["Início Previsto"])
df["Término Final"] = df["Término Real"].fillna(df["Término Previsto"])

# ⬇️ Criar coluna de duração (real ou prevista)
df["Duração (dias)"] = (df["Término Final"] - df["Início Final"]).dt.days

# ⬇️ Criar gráfico de Gantt
fig = px.timeline(
    df,
    x_start="Início Final",
    x_end="Término Final",
    y="Descrição dos Serviços",
    color="Duração (dias)",  # Define a cor das barras conforme a duração
    color_continuous_scale=[[0, "darkblue"], [0.5, "royalblue"], [1, "cyan"]],  # Degradê azul
    title="📊 Cronograma de Obra - Gráfico de Gantt",
)

# ⬇️ Ajustar a ordem das tarefas corretamente
fig.update_yaxes(autorange="reversed")  # Agora as tarefas aparecem corretamente de cima para baixo

# ⬇️ Ajustar a formatação do gráfico
fig.update_layout(
    font=dict(color="darkblue"),  # Cor geral do texto
    title=dict(
        text="Cronograma de Obra - Gráfico de Gantt",
        font=dict(color="darkblue", size=18),  # Título azul escuro e maior
        x=0.5,  # Centralizar o título
    ),
    xaxis=dict(
        title="Datas",
        title_font=dict(color="darkblue", size=14),  # Cor e tamanho do título do eixo X
        tickfont=dict(color="darkblue", size=12),  # Cor das datas no eixo X
    ),
    yaxis=dict(
        title="Descrição dos Serviços",
        title_font=dict(color="darkblue", size=14),  # Cor e tamanho do título do eixo Y
        tickfont=dict(color="darkblue", size=12),  # Cor dos textos das tarefas
    ),
    coloraxis_colorbar=dict(
        title="Duração (dias)",
        title_font=dict(color="darkblue", size=14),  # Cor do título da legenda de cores
        tickfont=dict(color="darkblue", size=12),  # Cor dos números da legenda
    ),
    plot_bgcolor="lightcyan",  # Fundo do gráfico azul claro
    paper_bgcolor="azure",  # Fundo da página
)

# ⬇️ Exibir gráfico no Streamlit
st.set_page_config(page_title="Cronograma de Execução", layout="wide")
st.title("BFX Engenharia Ltda")
st.plotly_chart(fig, use_container_width=True)
