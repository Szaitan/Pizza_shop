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

YOUR_DOMAIN = 'http://127.0.0.1:5000' #Remmeber to change it at the very end!!!


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
        return redirect(url_for("main_page"))

    all_pizza_data = stripe.Product.list()
    print(all_pizza_data)

    price_list = []
    for data in all_pizza_data["data"]:
        price_list.append(stripe.Price.retrieve(data["default_price"]))
    print(price_list)
    data_length = len(price_list)
    return render_template("cover.html", all_pizza_data=all_pizza_data["data"], price_list=price_list,
                           data_length=data_length)

    #
    # all_pizza_data = Pizza.query.all()
    # if len(basket_pizza_name_cost) != 0:
    #     return render_template("cover.html", all_pizza_data=all_pizza_data, plus_sign=len(basket_pizza_name_cost))
    # else:
    #     return render_template("cover.html", all_pizza_data=all_pizza_data)


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


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Nvh0SBIq7Xx10KpDgRiiTQI',
                    'quantity': 1,
                },
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Nvgz5BIq7Xx10KpJMMhykt3',
                    'quantity': 2,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


if __name__ == "__main__":
    app.run(debug=True)
