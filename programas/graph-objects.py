import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')
df = df[['time_utc', 'svid', 'elev', 's4']]

# filtrando apenas os satélites GLONASS (svid 38 a 61)
df = df[df['svid'].isin(range(38, 62))]
df = df[df['time_utc'].between('2025-03-21 05:30:00', '2025-03-21 07:30:00')]

fig_scatter = go.Figure(data=go.Scatter(
    x=df['time_utc'],
    y=df['s4'],
    mode='markers',
    marker=dict(
        size=10,
        color=df['elev'],  # cor baseada na elevação
        colorscale='sunsetdark',
        showscale=True,
        colorbar=dict(title='Elevação'),
        line=dict(width=0.5, color='black')
    ),
    text=df['svid'],  # texto para cada ponto (svid)
    hovertemplate='Satélite: %{text}<br>Tempo: %{x}<br>Índice S4: %{y}<extra></extra>'
))

fig_scatter.update_layout(
    title='Índice S4 dos satélites GLONASS ao longo do tempo',
    xaxis_title='Tempo (UTC)',
    yaxis_title='Índice S4',
    xaxis=dict(tickformat='%H:%M:%S', tickangle=45),
    yaxis=dict(range=[0, df['s4'].max() + 0.1])
)

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Exemplo de Gráfico tipo Scatter com Plotly Graph Objects', style={'textAlign': 'center'}),
    dcc.Graph(figure=fig_scatter)
])  

if __name__ == '__main__':
    app.run(debug=True)