from dash import (
    Dash,
    clientside_callback,
    html,
    dash_table,
    dcc,
    callback,
    Output,
    Input,
)
import yfinance as yf
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.LUMEN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
    ],
    brand="SentiMint",
    brand_href="#",
    color="primary",
    dark=True,
)

# App layout
app.layout = html.Div([
    navbar,
    dbc.Container(
        [
            html.H2("Ticker Tracker"),
            dcc.Input(id="ticker-input", type="text", placeholder="Enter ticker (e.g. SPY)", debounce=True),
            dcc.Graph(id="price-chart"),
        ],
        fluid=True,
    )]
)

@app.callback(
    Output("price-chart", "figure"),
    Input("ticker-input", "value"),
)
def update_price_chart(ticker):
    if not ticker:
        return px.line(title="Enter a ticker to see the price chart")

    try:
        df = yf.Ticker(ticker.upper()).history(period="6mo")
        if df.empty:
            return px.line(title=f"No data found for {ticker}")
        
        fig = px.scatter(
            df,
            x=df.index,
            y="Close",
            title=f"{ticker.upper()} Price Chart",
            labels={"x": "Date", "Close": "Price"},
            # template="plotly_dark",
        )
    except Exception as e:
        fig = px.line(title=f"Error fetching data for {ticker}: {str(e)}")

    return fig
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
