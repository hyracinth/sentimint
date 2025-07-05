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
                        dbc.Col(
                            dcc.Checklist(
                                id="show-regression",
                                options=[
                                    {
                                        "label": "Show Linear Regression",
                                        "value": "regression",
                                    }
                                ],
                                value=[],
                                style={"marginTop": "8px"},
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
    Input("show-regression", "value"),
)
def update_price_chart(ticker, period, toggle_regression):
    if not ticker:
        return px.line(title="Enter a ticker to see the price chart")

    try:
        df = yf.Ticker(ticker.upper()).history(period=period)
        if df.empty:
            return px.line(title=f"No data found for {ticker}")

        #TODO This does not work...
        trendline = "ols" if "regression" in toggle_regression else None

        if trendline:
            # Need to convert index to numeric for trendline because ols expects number for x-axis
            df = df.copy()
            df["date_num"] = df.index.astype("int64") // 10**9  # Convert to seconds since epoch
       
            fig = px.scatter(
                df,
                x="date_num",
                y="Close",
                title=f"{ticker.upper()} Price Chart",
                labels={"date_num": "Date", "Close": "Price"},
                trendline=trendline,
                # template="plotly_dark",
            )

            # Reformat x-axis to show dates
            fig.update_xaxes(
                tickvals=df["date_num"][::max(1, len(df)//10)],
                ticktext=[d.strftime("%Y-%m-%d") for d in df.index[::max(1, len(df)//10)]],
                title_text="Date"
            )
        else:
            fig = px.scatter(
                df,
                x=df.index,
                y="Close",
                title=f"{ticker.upper()} Price Chart",
                labels={"x": "Date", "Close": "Price"},
            )
    except Exception as e:
        fig = px.line(title=f"Error fetching data for {ticker}: {str(e)}")

    return fig

