from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharmacy.db"
db = SQLAlchemy(app)

# ------------------------ DATABASE MODELS ------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    medicine_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)

# ------------------------ CREATE TABLES ------------------------

def create_tables():
    db.create_all()
    if Medicine.query.count() == 0:
        db.session.add(Medicine(name="Paracetamol", price=20))
        db.session.add(Medicine(name="Vitamin C", price=50))
        db.session.add(Medicine(name="Cough Syrup", price=80))
        db.session.commit()

# ------------------------ ROUTES ------------------------

@app.route("/")
def home():
    return render_template_string("""
        <h2>Welcome to HealthyMe Pharmacy 💊</h2>
        <a href="/signup">Signup</a> | <a href="/login">Login</a>
    """)

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already taken!", "error")
            return redirect("/signup")

        hashed = generate_password_hash(password)
        db.session.add(User(username=username, password=hashed))
        db.session.commit()
        flash("Signup successful! Please login.", "success")
        return redirect("/login")

    return render_template_string("""
        <h2>Signup</h2>
        <form method="POST">
            Username: <input name="username"><br><br>
            Password: <input name="password" type="password"><br><br>
            <button type="submit">Signup</button>
        </form>
    """)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password!", "error")
            return redirect("/login")

        session["user_id"] = user.id
        return redirect("/shop")

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br><br>
            Password: <input name="password" type="password"><br><br>
            <button type="submit">Login</button>
        </form>
    """)

# Shop Page
@app.route("/shop")
def shop():
    if "user_id" not in session:
        return redirect("/login")

    meds = Medicine.query.all()

    return render_template_string("""
        <h2>Available Medicines</h2>
        {% for m in meds %}
            <p>
                {{ m.name }} - ₹{{ m.price }}
                <a href="/add_to_cart/{{ m.id }}">Add to Cart</a>
            </p>
        {% endfor %}
        <br><a href="/cart">View Cart</a>
    """, meds=meds)

# Add to Cart
@app.route("/add_to_cart/<int:med_id>")
def add_to_cart(med_id):
    if "user_id" not in session:
        return redirect("/login")

    db.session.add(Cart(user_id=session["user_id"], medicine_id=med_id))
    db.session.commit()
    flash("Added to cart!", "success")
    return redirect("/shop")

# Cart
@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/login")

    items = db.session.query(Cart, Medicine).join(
        Medicine, Cart.medicine_id == Medicine.id
    ).filter(Cart.user_id == session["user_id"]).all()

    return render_template_string("""
        <h2>Your Cart 🛒</h2>
        {% for cart, med in items %}
            <p>{{ med.name }} - ₹{{ med.price }} × {{ cart.quantity }}</p>
        {% endfor %}
        <br>
        <a href="/shop">Back to Shop</a>
    """, items=items)

# ------------------------ RUN SERVER ------------------------

if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True, port=5001)
