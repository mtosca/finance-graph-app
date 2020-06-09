import datetime
from pandas_datareader import data
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

# 12 hours candle width
HOURS_IN_MILLIS_12 = 12 * 60 * 60 * 1000


def status(o, c):
    return "red" if c < o else "green"


class StockPriceGraph:
    def __init__(self, ticker, start, end):

        self.data = data.DataReader(ticker, data_source="yahoo", start=start, end=end)
        self.figure = None

    def draw_html(self):

        # keep the figure stored
        if self.figure != None:
            return self.figure

        # prepare useful data first
        self.data["Status"] = [
            status(o, c) for o, c in zip(self.data.Open, self.data.Close)
        ]
        self.data["PriceAvg"] = (self.data.Open + self.data.Close) / 2
        self.data["Spread"] = abs(self.data.Close - self.data.Open)

        fig = figure(
            x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width"
        )
        fig.title.text = "Candlestick chart"
        fig.grid.grid_line_alpha = 0.7

        # draw max and min lines on the back layer
        fig.segment(
            self.data.index,
            self.data.High,
            self.data.index,
            self.data.Low,
            color="black",
        )

        # draw green candles then
        fig.rect(
            self.data.index[self.data.Status == "green"],
            self.data.PriceAvg[self.data.Status == "green"],
            HOURS_IN_MILLIS_12,
            self.data.Spread[self.data.Status == "green"],
            fill_color="green",
            line_color="black",
        )

        # draw red candles finally
        red_candles = self.data.index[self.data.Status == "red"]
        fig.rect(
            red_candles,
            self.data.PriceAvg[self.data.Status == "red"],
            HOURS_IN_MILLIS_12,
            self.data.Spread[self.data.Status == "red"],
            fill_color="red",
            line_color="black",
        )

        self.figure = fig
        return components(self.figure)

    def js_files(self):
        return CDN.js_files

    def css_files(self):
        return CDN.css_files
