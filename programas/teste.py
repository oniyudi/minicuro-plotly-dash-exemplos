import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')
df = df[['time_utc', 'svid', 'elev', 's4']]

df_constallation = df[df['svid'].isin(range(1, 37))]

fig = px.scatter(
    df_constallation, 
    x='time_utc', 
    y='s4', 
    color='svid', 
    animation_frame='time_utc', 
    animation_group='svid', 
    range_x=[
        df_constallation['time_utc'].min(), 
        df_constallation['time_utc'].max()
    ], 
    range_y=[0, df_constallation['s4'].max() + 0.1],
    labels={'s4': 'Índice S4', 'time_utc': 'Tempo (UTC)', 'svid': 'Satélite'},
    title='Grafico animado',
    
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100

app = Dash(__name__)
app.layout = html.Div(children=[
    dcc.Loading(
        dcc.Graph(
        id='s4-constellation-graph',
        figure=fig
        ),
        type='cube',
    )
])

if __name__ == '__main__':
    app.run(debug=True)