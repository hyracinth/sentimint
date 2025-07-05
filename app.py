import dash
from dash import (
    Dash,
    html,
)
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUMEN]
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
    ],
    brand="SentiMint",
    brand_href="#",
    color="primary",
    # dark=True,
)

# App layout
app.layout = html.Div(
    [
        navbar,
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
