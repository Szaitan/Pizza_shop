from flask import Flask, url_for, render_template, redirect, request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('app_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Pizza(db.Model):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)


@app.route("/", methods=["POST", "GET"])
def main_page():
    if request.method == "POST":
        print(request.form["total_pizza_cost"])
        return redirect(url_for("main_page"))
    all_pizza_data = Pizza.query.all()
    return render_template("cover.html", all_pizza_data=all_pizza_data)


@app.route("/pizza-creator", methods=["POST"])
def pizza_page():
    pizza_name = request.args.get("pizza_name")
    pizza_cost = request.args.get("pizza_cost")
    return render_template("pizza-page.html", pizza_name=pizza_name, pizza_cost=pizza_cost)


if __name__ == "__main__":
    app.run(debug=True)
