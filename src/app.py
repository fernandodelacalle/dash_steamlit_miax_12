import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from api_handler import APIBMEHandler
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)


ah = APIBMEHandler()


app.layout = html.Div(children=[
        html.H1(children='MIAX DATA EXPLORER'),

        html.Div(children='''
            mIAx API
        '''),
        dcc.Dropdown(
            id='menu-index',
            options=[
                {'label': 'IBEX', 'value': 'IBEX'},
                {'label': 'DAX', 'value': 'DAX'},
                {'label': 'EUROSTOXX', 'value': 'EUROSTOXX'},
            ],
            value='IBEX'
        ),
        dcc.Dropdown(
            id='menu-tck',
        ),
        dcc.Graph(
            id='example-graph',
        )
    ]
)


@app.callback(
    Output('menu-tck', 'options'),
    Input('menu-index', 'value'),
)
def change_market(market):
    maestro = ah.get_ticker_master(market=market)
    lista_tcks = maestro.loc[:, 'ticker'].to_list()
    return [
        {'label': tck, 'value': tck}
        for tck in lista_tcks
    ]

@app.callback(
    Output('menu-tck', 'value'),
    Input('menu-tck', 'options'),
)
def change_tck_options(tck_options):
    return tck_options[0]['value']



@app.callback(
    Output('example-graph', 'figure'),
    State('menu-index', 'value'),
    Input('menu-tck', 'value'),
)
def plot_data(market, tck):
    data_ticker = ah.get_close_data_ticker(market=market, ticker=tck)
    fig = px.line(data_ticker)
    return fig


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=8080)
