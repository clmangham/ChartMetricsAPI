from flask import render_template
import config


app = config.connex_app
app.add_api(config.basedir / "api.yml")

@app.route("/")
def home():

    return render_template("home.html")


if __name__ == "__main__":
    #  Listen on all available networks/interfaces
    app.run(host="0.0.0.0", port=8000, debug=False)