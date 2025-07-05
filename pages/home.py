print("home.py loaded")
import dash
from dash import Input, Output, html, dcc
import yfinance as yf
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

YFINANCE_PERIODS = [
    "1d",
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
    "ytd",
    "max",
]

layout = html.Div(
    [
        html.H2("Ticker Tracker"),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Input(
                                id="ticker-input",
                                type="text",
                                placeholder="Enter ticker (e.g. SPY)",
                                debounce=True,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="ticker-period-dropdown",
                                options=[
                                    {"label": p.upper(), "value": p}
                                    for p in YFINANCE_PERIODS
                                ],
                                value="6mo",
                                clearable=False,
                                style={"width": "200px", "marginTop": "0px"},
                            ),
                            width="auto",
                        ),
                    ],
                    className="mb-3",
                ),
                dcc.Graph(id="price-chart"),
            ],
            fluid=True,
        ),
    ]
)


@dash.callback(
    Output("price-chart", "figure"),
    Input("ticker-input", "value"),
    Input("ticker-period-dropdown", "value"),
)
def update_price_chart(ticker, period):
    if not ticker:
        return px.line(title="Enter a ticker to see the price chart")

    try:
        df = yf.Ticker(ticker.upper()).history(period=period)
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
