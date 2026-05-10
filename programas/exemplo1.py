import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# carregando a base de dados
df = pd.read_csv('../base_dados/base_de_dados.ismr')

# pegando apenas os dados relevantes para o gráfico
df = df[['time_utc', 'svid', 'elev', 's4']]

# criando o gráfico scatter plot
fig = px.scatter(df, x='time_utc', y='s4', color='svid', title='Índice S4 ao longo do tempo')

# criando a aplicação Dash
app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Exemplo de Gráfico tipo Scatter com Dash', style={'textAlign': 'center'}),

    dcc.Graph(
        id='s4-graph',
        figure=fig
    )
])
if __name__ == '__main__':
    app.run(debug=True)