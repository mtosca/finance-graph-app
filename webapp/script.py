from flask import Flask, render_template
from stock_price_service import StockPriceGraph
from bokeh.embed import components
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/price/")
def price():
    # let's hardcode some dates for the moment
    start = datetime.datetime(2020, 3, 1)
    end = datetime.datetime(2020, 5, 27)

    graph = StockPriceGraph("AAPL", start, end)
    script, div = graph.draw_html()

    return render_template(
        "graph.html",
        script1=script,
        div1=div,
        cdn_css=graph.css_files(),
        cdn_js=graph.js_files(),
    )


if __name__ == "__main__":
    app.run(debug=True)
