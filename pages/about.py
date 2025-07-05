import dash
from dash import html

dash.register_page(__name__, path="/about")

layout = html.Div(
    [
        html.H2("About Page"),
        html.P("This is the about page of the SentiMint application."),
        html.P("This is a learning project to explore Dash and data visualization."),
    ]
)
