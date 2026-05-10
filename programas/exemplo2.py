import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')

df = df[['time_utc', 'svid', 'elev', 's4']]

df = df[df['svid'].isin(range(1, 37))]

# df['s4'] = df['s4'].fillna(df['s4'].mean(numeric_only=True))

df_single = df[df['svid'].isin([19, 6])]
df_single = df_single[df_single['time_utc'].between('2025-03-21 00:00:00', '2025-03-21 00:50:00')]

fig = px.line(df, x='time_utc', y='s4', color='svid', title='Índice S4 ao longo do tempo para cada satélite')

fig_single = px.line(df_single, x='time_utc', y='s4', color='svid', text='elev', title='Índice S4 dos satélites 6 e 19 entre 00:00 e 00:50 do dia 21 de março de 2025')
fig_single.update_traces(textposition='bottom right')

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Exemplo de Gráfico tipo Line com Plotly Express', style={'textAlign': 'center'}),

    dcc.Graph(
        id='s4-line-graph',
        figure=fig
    ),
    dcc.Graph(
        id='s4-line-graph-single',
        figure=fig_single
    )
])
if __name__ == '__main__':
    app.run(debug=True)