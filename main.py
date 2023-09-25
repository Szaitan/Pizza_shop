from flask import Flask, url_for, render_template, redirect


app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("cover.html")


if __name__ == "__main__":
    app.run(debug=True)
