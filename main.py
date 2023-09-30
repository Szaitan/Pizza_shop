from flask import Flask, url_for, render_template, redirect, request, flash
from forms import CreateLoginForm, CreateRegisterForm
import os
from flask_sqlalchemy import SQLAlchemy
import stripe
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import email_validator

stripe.api_key = os.environ.get("stripe_api_key")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('app_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

basket_pizza_name_cost = []

YOUR_DOMAIN = 'http://127.0.0.1:5000'  # Remmeber to change it at the very end!!!


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = CreateLoginForm()
    if form.validate_on_submit():
        user_to_check = db.session.query(User).filter_by(email=form.e_mail.data).first()
        if user_to_check is not None:
            if check_password_hash(user_to_check.password, form.password.data):
                login_user(user_to_check)
                return redirect(url_for('main_page'))
            else:
                flash("Wrong Password. Try Again.")
                return redirect(url_for('login_page'))
        else:
            flash("This user does not exists in database. Try again or contact administrator.")
            return redirect(url_for('login_page'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = CreateRegisterForm()
    print(1)
    if form.validate_on_submit():
        print(2)
        print(form.e_mail.data)
        if db.session.query(User).filter_by(email=form.e_mail.data).first() is None:
            print(3)
            # noinspection PyArgumentList

            user_to_add = User(login=form.login.data, email=form.e_mail.data,
                               password=generate_password_hash(form.password.data, salt_length=8))
            db.session.add(user_to_add)
            db.session.commit()
            login_user(user_to_add)
            return redirect(url_for('main_page'))
        else:
            flash("This e-mail already exists in database. Please chose another one.")
            return redirect(url_for('register_page'))
    return render_template('register.html', form=form)


@app.route("/", methods=["POST", "GET"])
def main_page():
    db.create_all()
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
    if len(basket_pizza_name_cost) == 0:
        flash("Before payment, please chose items you would like to buy.")
        return redirect(url_for("pizza_basket"))
    if not current_user.is_authenticated:
        flash("Before payment, please verify yourself or create account.")
        return redirect(url_for("pizza_basket"))
    else:
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
