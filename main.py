from _decimal import Decimal
from flask import Flask, url_for, render_template, redirect, request
import os
from flask_sqlalchemy import SQLAlchemy
import stripe

stripe.api_key = os.environ.get("stripe_api_key")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('app_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
basket_pizza_name_cost = []

YOUR_DOMAIN = 'http://127.0.0.1:5000'  # Remmeber to change it at the very end!!!


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
        pizza_name = request.args.get("pizza_name")
        number_of_pizzas = request.form["total_pizza_number"]
        cost_of_pizzas = request.form["total_pizza_cost"]
        list_with_pizza_info = []
        for data in (pizza_name, number_of_pizzas, cost_of_pizzas):
            list_with_pizza_info.append(data)
        basket_pizza_name_cost.append(list_with_pizza_info)
        return redirect(url_for("main_page"))

    all_pizza_data = stripe.Product.list()

    price_list = []
    for data in all_pizza_data["data"]:
        price_list.append(stripe.Price.retrieve(data["default_price"]))
    data_length = len(price_list)

    if len(basket_pizza_name_cost) != 0:
        return render_template("cover.html", all_pizza_data=all_pizza_data["data"], price_list=price_list,
                               data_length=data_length, plus_sign=len(basket_pizza_name_cost))
    else:
        return render_template("cover.html", all_pizza_data=all_pizza_data["data"], price_list=price_list,
                               data_length=data_length)


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
        total_cost += float(basket_pizza_name_cost[n][2])
    return render_template("basket-page.html", basket=basket_pizza_name_cost, total_cost="{:.2f}".format(total_cost))


@app.route("/test", methods=['POST'])
def checkout_data_preparation():
    list_for_checkout = []
    for data in basket_pizza_name_cost:
        cost_to_find = int(data[2]) / int(data[1])
        search_by_price = stripe.Price.search(query=f"metadata['pizza']:'{data[0]} {int(cost_to_find)}'")
        x = {"price": search_by_price["data"][0]["id"],
             "quantity": data[1],
             }
        list_for_checkout.append(x)
    return list_for_checkout


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    item_list = checkout_data_preparation()

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=item_list,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route('/success')
def success_page():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
