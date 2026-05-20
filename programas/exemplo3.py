import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')

df = df[['time_utc', 'svid', 'elev', 's4', 'azim']]

# dados para o gráfico de linha
df_single = df[df['svid'].isin([19, 6])]
df_single = df_single[df_single['time_utc'].between('2025-03-21 00:00:00', '2025-03-21 00:50:00')]

# dados para o gráfico de barras
df_bar = df[df['svid'].isin(range(1,37))]
# df_bar = df_bar[df_bar['time_utc'].between('2025-03-21 00:00:00', '2025-03-21 01:00:00')]
df_bar = df_bar[df_bar['time_utc'] == '2025-03-21 00:35:00']
# usar o astype(str) para converter os valores de svid para string, garantindo que sejam tratados como categorias no gráfico de barras
df_bar['svid'] = df_bar['svid'].astype(str)

# dados para o gráfico polar
df_polar = df[df['svid'].isin(range(1,37))]
df_polar = df_polar[df_polar['time_utc'].between('2025-03-21 00:00:00', '2025-03-21 00:25:00')]
df_polar = df_polar[df_polar['s4'].notna()]

fig_single = px.line(df_single, x='time_utc', y='s4', color='svid', text='elev', title='Índice S4 dos satélites 6 e 19 entre 00:00 e 00:50 do dia 21 de março de 2025')
fig_single.update_traces(textposition='bottom right')

fig_bar = px.bar(df_bar, x='svid', y='s4', color='s4', text='s4', title='Índice S4 dos satélites 1 a 36 às 00:35 do dia 21 de março de 2025')

fig_polar = px.scatter_polar(df_polar, r='elev', theta='azim', color='s4', size='s4', symbol='svid', labels={'svid': 'Satélite', 's4': 'Índice S4'}, title='Posição dos satélites 1 a 36 das 00:00 a 00:25 do dia 21 de março de 2025')
fig_polar.update_traces(
    marker=dict(line=dict(width=1, color='gray'))
)
fig_polar.update_layout(
    legend=dict(
        orientation="h", # coloca a legenda horizontal
        yanchor="top", # ancoragem superior
        y=-0.25, # posição vertical da legenda
        xanchor="center", # ancoragem central
        x=0.5 # posição horizontal da legenda
    )
)

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Exemplo de Gráfico tipo Line com Plotly Express', style={'textAlign': 'center'}),

    dcc.Graph(
        id='s4-line-graph-single',
        figure=fig_single
    ),
    dcc.Graph(
        id='s4-bar-graph',
        figure=fig_bar
    ),
    dcc.Graph(
        id='s4-polar-graph',
        figure=fig_polar
    )
])
if __name__ == '__main__':
    app.run(debug=True)