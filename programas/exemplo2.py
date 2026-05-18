import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')

df = df[['time_utc', 'svid', 'elev', 's4']]

df = df[df['svid'].isin(range(1, 37))]

# df_scatter = df[df['svid'].isin(x for x in range(1,20) if x not in [6, 13, 15, 19])]
df_scatter = df[df['svid'].isin(range(1,20))]
df_scatter = df_scatter[df_scatter['time_utc'].between('2025-03-21 01:00:00', '2025-03-21 01:30:00')]

fig_scatter = px.scatter(df_scatter, x='time_utc', y='s4', color='s4', text='svid', color_continuous_scale='bluered', title='Índice S4 dos satélites 1 a 19 entre 00:00 e 00:20 do dia 21 de março de 2025')
fig_scatter.update_traces(textposition='bottom right')

fig_scatter_2 = px.scatter(df_scatter, x='time_utc', y='s4', color='s4', symbol='svid', labels={'svid': 'Satélites', 's4': 'Índice S4'}, color_continuous_scale=[(0, "blue"), (0.5, "green"), (1, "red")], title='Índice S4 dos satélites 1 a 19 entre 00:00 e 00:20 do dia 21 de março de 2025')
fig_scatter_2.update_layout(
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
        id='s4-scatter-graph',
        figure=fig_scatter
    ),
    dcc.Graph(
        id='s4-scatter-graph-2',
        figure=fig_scatter_2
    )
])
if __name__ == '__main__':
    app.run(debug=True)