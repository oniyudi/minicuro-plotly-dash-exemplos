import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')
df = df[['time_utc', 'svid', 'elev', 's4']]

df_bar = df[df['time_utc'] == '2025-03-21 00:05:00']
df_bar['svid'] = df_bar['svid'].astype(str)

# pegando exemplos de cores para o dropdown
color_options = px.colors.named_colorscales()

app = Dash(__name__)
app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Label('Selecione a escala de cores: ', className='label-input'),
            html.Div(children=[
                dcc.Dropdown(
                id='color-dropdown',
                options=color_options,
                value='viridis',
                clearable=False # impede que o usuário limpe a seleção, garantindo que sempre haja uma opção selecionada
                ),
            ], className='dropdown-color')
        ], className='input-group'),
        html.Div(children=[
            html.Label('Filtrar pela elevação: ', className='label-input'),
            dcc.Input(id='elev-input', type='number', min=0, className='input-number', placeholder='Digite a elevação mínima')

        ], className='input-group'),
    ], className='group'),
    dcc.Loading(
        dcc.Graph(
        id='s4-bar-graph',
        ),
        type='cube',
    )
])

@app.callback(
    Output('s4-bar-graph', 'figure'),
    Input('color-dropdown', 'value'),
    Input('elev-input', 'value')
)
def update_bar_chart(selected_color, elev_value):
    if elev_value is not None:
        filtered_df = df_bar[df_bar['elev'] >= elev_value]
    else:
        filtered_df = df_bar

    fig_bar = px.bar(filtered_df, x='svid', y='s4', color='elev', color_continuous_scale=selected_color.lower(), labels={'s4': 'Índice S4', 'elev': 'Elevação', 'svid': 'Satélite'}, title='Índice S4 dos satélites no instante 00:05 do dia 21 de março de 2025')
    fig_bar.update_traces(marker_line_color='black', marker_line_width=1.5)
    fig_bar.add_shape(
        type='line',
        xref='paper',
        x0=0,
        x1=1,
        y0=0.25,
        y1=0.25,
        line=dict(color='red', width=3, dash='dash'),
        layer='above'
    )
    fig_bar.add_annotation(
        text="Limite S4 Crítico (0.25)",
        xref="paper", x=0.01,  # 0.01 para dar uma leve margem da borda esquerda
        yref="y", y=0.25,      # O mesmo Y da sua linha
        yshift=12,             # Empurra o texto 12 pixels para CIMA da linha
        showarrow=False,       # Remove a setinha padrão do Plotly
        font=dict(color="red", size=12)
    )

    # parte utilzando o graph_objects para adicionar uma linha na legenda, já que as formas (shapes) não aparecem na legenda
    fig_bar.add_trace(go.Scatter(
        x=[None],  # Necessário para criar uma entrada na legenda, mas não queremos pontos reais
        y=[None],
        mode='lines',
        line=dict(color='red', width=3, dash='dash'),
        name='Limite S4 Crítico (0.25)',
    ))
    fig_bar.update_layout(
        legend=dict(
        yanchor="top",
        y=0.98,
        xanchor="right",
        x=0.98,
        bgcolor="rgba(255, 255, 255, 0.8)", # Fundo branco com 80% de opacidade
        bordercolor="black",
        borderwidth=1
        )
    )
    time.sleep(0.5) 
    return fig_bar

if __name__ == '__main__':
    app.run(debug=True)