import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

df = pd.read_csv('../base_dados/base_de_dados.ismr')
df = df[['time_utc', 'svid', 'elev', 's4']]

df = df[df['time_utc'].between('2025-03-21 00:00:00', '2025-03-21 00:10:00')]

df_bar = df[df['time_utc'] == '2025-03-21 00:05:00']
df_bar['svid'] = df_bar['svid'].astype(str)
# fig_bar = px.bar(df_bar, x='svid', y='s4', color='s4', title='Índice S4 dos satélites 1 a 36 no instante 00:05 do dia 21 de março de 2025')

app = Dash(__name__)
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='color-dropdown',
        options=['Inferno', 'Viridis', 'Cividis', 'Bluered', 'Blues', 'Reds', 'Greens', 'Purples', 'Oranges'],
        value='Viridis',
        style={'width': '50%', 'margin': 'auto'},
        clearable=False # impede que o usuário limpe a seleção, garantindo que sempre haja uma opção selecionada
    ),
    dcc.Graph(
        id='s4-bar-graph',
        # figure=fig_bar
    )
])

@app.callback(
    Output('s4-bar-graph', 'figure'),
    Input('color-dropdown', 'value')
)
def update_bar_chart(selected_color):
    fig_bar = px.bar(df_bar, x='svid', y='s4', color='elev', color_continuous_scale=selected_color.lower(), title='Índice S4 dos satélites 1 a 36 no instante 00:05 do dia 21 de março de 2025')
    return fig_bar

if __name__ == '__main__':
    app.run(debug=True)