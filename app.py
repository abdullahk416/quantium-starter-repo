import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


DATA_PATH = "formatted_sales_data.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

REGION_OPTIONS = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]


def load_raw_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

    df = df.dropna(subset=["Date", "Sales", "Region"])

    df["Region"] = df["Region"].astype(str).str.strip().str.lower()

    return df


RAW_DF = load_raw_data()

app = Dash(__name__)
app.title = "Soul Foods Visualiser"


def build_figure(region_value: str):
    df = RAW_DF

    if region_value != "all":
        df = df[df["Region"] == region_value].copy()

    daily = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    title_region = "All Regions" if region_value == "all" else region_value.capitalize()

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Total Sales"},
        title=f"Pink Morsels Sales Over Time ({title_region})",
    )

    # Add vertical marker line using add_shape to avoid add_vline issues
    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE,
        x1=PRICE_INCREASE_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line={"width": 2, "dash": "dash"},
    )

    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (2021-01-15)",
        showarrow=False,
        yanchor="bottom",
    )

    return fig


app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="card header-card",
            children=[
                html.H1("Soul Foods Pink Morsels Sales Visualiser", className="title"),
                html.P(
                    "Filter by region to explore trends. The dashed vertical line marks the Jan 15, 2021 price increase.",
                    className="subtitle",
                ),
            ],
        ),

        html.Div(
            className="card controls-card",
            children=[
                html.Div(
                    className="control-row",
                    children=[
                        html.Div("Region", className="control-label"),
                        dcc.RadioItems(
                            id="region-radio",
                            options=REGION_OPTIONS,
                            value="all",
                            inline=True,
                            className="radio-group",
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            className="card chart-card",
            children=[
                dcc.Graph(
                    id="sales-chart",
                    figure=build_figure("all"),
                    className="chart",
                )
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region_value: str):
    return build_figure(region_value)


if __name__ == "__main__":
    app.run(debug=True)
