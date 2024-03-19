from flask import render_template, jsonify
import config
from models import Chart_Data


app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    # data = Chart_Data.query.limit(10).all()
    # return render_template("home.html", data=data)

    return render_template("home.html")


if __name__ == "__main__":
    #  Listen on all available networks/interfaces
    app.run(host="0.0.0.0", port=8000, debug=True)