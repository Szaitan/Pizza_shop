from _decimal import Decimal
from flask import Flask, url_for, render_template, redirect, request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('app_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
basket_pizza_name_cost = []


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
        if request.args.get("reset"):
            print(True)
            basket_pizza_name_cost.clear()
            return redirect(url_for("main_page"))

        name_cost = []
        name = request.args.get("pizza_name")
        cost = request.form["total_pizza_cost"]
        name_cost.append(name)
        name_cost.append(cost)
        basket_pizza_name_cost.append(name_cost)
        return redirect(url_for("main_page"))

    all_pizza_data = Pizza.query.all()
    if len(basket_pizza_name_cost) != 0:
        return render_template("cover.html", all_pizza_data=all_pizza_data, plus_sign=len(basket_pizza_name_cost))
    else:
        return render_template("cover.html", all_pizza_data=all_pizza_data)


@app.route("/pizza-creator", methods=["POST"])
def pizza_page():
    pizza_name = request.args.get("pizza_name")
    pizza_cost = request.args.get("pizza_cost")
    if len(basket_pizza_name_cost) != 0:
        return render_template("pizza-page.html", pizza_name=pizza_name, pizza_cost=pizza_cost,
                               plus_sign=len(basket_pizza_name_cost))
    else:
        return render_template("pizza-page.html", pizza_name=pizza_name, pizza_cost=pizza_cost)


@app.route("/pizza-basket")
def pizza_basket():
    total_cost = 0
    for n in range(len(basket_pizza_name_cost)):
        total_cost += float(basket_pizza_name_cost[n][1])
    return render_template("basket-page.html", basket=basket_pizza_name_cost, total_cost=total_cost)


if __name__ == "__main__":
    app.run(debug=True)
