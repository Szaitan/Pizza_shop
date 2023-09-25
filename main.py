from flask import Flask, url_for, render_template, redirect
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


@app.route("/")
def main_page():
    db.create_all()
    pizza = Pizza(
        name="Classic",
        price=39.39,
        ingredients="Ham, mushrooms, mozzarella cheese, herb tomato sauce",
        image="500px-Classsic.jpg"
    )
    db.session.add(pizza)
    db.session.commit()
    return render_template("cover.html")


if __name__ == "__main__":
    app.run(debug=True)
