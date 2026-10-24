from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# -------------------------
# Product Model
# -------------------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    category = db.Column(db.String(100), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=0)

    price = db.Column(db.Float, nullable=False)

    description = db.Column(db.Text)

    image = db.Column(db.String(250), default="default.png")

    def __repr__(self):
        return f"<Product {self.name}>"


# -------------------------
# Admin Model
# -------------------------
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"