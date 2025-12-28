import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


def load_data() -> pd.DataFrame:
    df = pd.read_csv("formatted_sales_data.csv")

    # Parse Date and clean rows
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # Ensure Sales is numeric
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df = df.dropna(subset=["Sales"])

    # Total sales per day, sorted by date
    daily = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    return daily


daily_sales = load_data()

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    labels={"Date": "Date", "Sales": "Total Sales"},
    title="Pink Morsels Sales Over Time",
)

# Mark the price increase date (use add_shape + add_annotation to avoid add_vline issues)
price_increase_date = pd.Timestamp("2021-01-15")

fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line={"width": 2, "dash": "dash"},
)

fig.add_annotation(
    x=price_increase_date,
    y=1,
    xref="x",
    yref="paper",
    text="Price increase (2021-01-15)",
    showarrow=False,
    yanchor="bottom",
)

app = Dash(__name__)

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Soul Foods Pink Morsels Sales Visualiser"),
        html.P(
            "Line chart of total daily sales. "
            "The dashed vertical line marks the Jan 15, 2021 price increase."
        ),
        dcc.Graph(figure=fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)

