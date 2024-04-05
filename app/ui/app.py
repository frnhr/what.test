from dash import Dash, html


__all__ = ['app']


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
])

