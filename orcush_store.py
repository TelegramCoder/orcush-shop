from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orcush_store.db"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form["description"]
        product = Product(name=name, price=price, description=description)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_product.html")

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        product = Product.query.get_or_404(product_id)
        # Add product to cart logic here
        return redirect(url_for("cart"))
    return render_template("cart.html")

if __name__ == "__main__":
    app.run(debug=True)
