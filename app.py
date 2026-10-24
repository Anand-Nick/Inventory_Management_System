from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models import db, Product, Admin
from database import create_database
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "inventory_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = "static/uploads"

db.init_app(app)

create_database(app)

# Create upload folder automatically
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session["admin"] = admin.username

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Username or Password")

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("login"))


# ---------------- DASHBOARD ---------------- #

@app.route("/admin")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    total_products = Product.query.count()

    available_products = Product.query.filter(
        Product.quantity > 10
    ).count()

    low_stock = Product.query.filter(
        Product.quantity.between(1, 10)
    ).count()

    out_of_stock = Product.query.filter(
        Product.quantity == 0
    ).count()

    electronics = Product.query.filter_by(
        category="Electronics"
    ).count()

    groceries = Product.query.filter_by(
        category="Groceries"
    ).count()

    medical = Product.query.filter_by(
        category="Medical"
    ).count()

    clothing = Product.query.filter_by(
        category="Clothing"
    ).count()

    furniture = Product.query.filter_by(
        category="Furniture"
    ).count()

    fruits = Product.query.filter_by(
        category="Fruits"
    ).count()

    stationery = Product.query.filter_by(
        category="Stationery"
    ).count()

    return render_template(
        "admin.html",

        total_products=total_products,

        available_products=available_products,

        low_stock=low_stock,

        out_of_stock=out_of_stock,

        electronics=electronics,

        groceries=groceries,

        medical=medical,

        clothing=clothing,

        furniture=furniture,

        fruits=fruits,

        stationery=stationery
    )


# ---------------- ADD PRODUCT ---------------- #

@app.route("/add", methods=["GET", "POST"])
def add_product():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]

        category = request.form["category"]

        quantity = int(request.form["quantity"])

        price = float(request.form["price"])

        description = request.form["description"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        product = Product(

            name=name,

            category=category,

            quantity=quantity,

            price=price,

            description=description,

            image=filename

        )

        db.session.add(product)

        db.session.commit()

        flash("Product Added Successfully")

        return redirect(url_for("view_products"))

    return render_template("add_product.html")
# ---------------- VIEW PRODUCTS ---------------- #

@app.route("/products")
def view_products():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        "view_products.html",
        products=products
    )


# ---------------- PRODUCT DETAILS ---------------- #

@app.route("/product/<int:id>")
def product_details(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    return render_template(
        "product_details.html",
        product=product
    )


# ---------------- UPDATE PRODUCT ---------------- #

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_product(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]

        product.category = request.form["category"]

        product.quantity = int(request.form["quantity"])

        product.price = float(request.form["price"])

        product.description = request.form["description"]

        image = request.files["image"]

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            product.image = filename

        db.session.commit()

        flash("Product Updated Successfully")

        return redirect(url_for("view_products"))

    return render_template(
        "update_product.html",
        product=product
    )

@app.route("/edit_id/<int:id>", methods=["GET", "POST"])
def edit_id(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        new_id = int(request.form["new_id"])

        # Check if the new ID already exists
        existing = Product.query.get(new_id)

        if existing:
            return "Product ID already exists!"

        # Update the primary key
        product.id = new_id
        db.session.commit()

        return redirect(url_for("view_products"))

    return render_template("edit_id.html", product=product)
# ---------------- DELETE PRODUCT ---------------- #

@app.route("/delete/<int:id>")
def delete_product(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    if product.image:

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            product.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)

    db.session.commit()

    flash("Product Deleted Successfully")

    return redirect(url_for("view_products"))


# ---------------- SEARCH PRODUCT ---------------- #

@app.route("/search", methods=["GET"])
def search_product():

    if "admin" not in session:
        return redirect(url_for("login"))

    keyword = request.args.get("keyword", "")

    products = Product.query.filter(
        Product.name.ilike(f"%{keyword}%")
    ).all()

    return render_template(
        "view_products.html",
        products=products
    )
# ---------------- CATEGORY PAGES ---------------- #

@app.route("/electronics")
def electronics():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Electronics"
    ).all()

    return render_template(
        "electronics.html",
        products=products
    )


@app.route("/groceries")
def groceries():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Groceries"
    ).all()

    return render_template(
        "groceries.html",
        products=products
    )


@app.route("/medical")
def medical():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Medical"
    ).all()

    return render_template(
        "medical.html",
        products=products
    )


@app.route("/clothing")
def clothing():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Clothing"
    ).all()

    return render_template(
        "clothing.html",
        products=products
    )


@app.route("/furniture")
def furniture():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Furniture"
    ).all()

    return render_template(
        "furniture.html",
        products=products
    )


@app.route("/fruits")
def fruits():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Fruits").all()

    return render_template(
        "fruits.html",
        products=products
    )

@app.route("/vegetables")
def vegetables():
    products = Product.query.filter_by(category="Vegetables").all()
    return render_template("vegetables.html", products=products)


@app.route("/stationery")
def stationery():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter_by(
        category="Stationery"
    ).all()

    return render_template(
        "stationery.html",
        products=products
    )


# ---------------- STOCK PAGES ---------------- #

@app.route("/available")
def available_products():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter(
        Product.quantity > 10
    ).all()

    return render_template(
        "available_products.html",
        products=products
    )


@app.route("/lowstock")
def low_stock():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter(
        Product.quantity.between(1, 10)
    ).all()

    return render_template(
        "low_stock.html",
        products=products
    )


@app.route("/outofstock")
def out_of_stock():

    if "admin" not in session:
        return redirect(url_for("login"))

    products = Product.query.filter(
        Product.quantity == 0
    ).all()

    return render_template(
        "out_of_stock.html",
        products=products
    )


# ---------------- ABOUT ---------------- #

@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- CONTACT ---------------- #

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- RUN APPLICATION ---------------- #

if __name__ == "__main__":
    app.run(debug=True)