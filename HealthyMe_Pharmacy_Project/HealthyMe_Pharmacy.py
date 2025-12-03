from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharmacy.db"
db = SQLAlchemy(app)

# ----------------------- DATABASE MODELS -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cart_items = db.relationship("Cart", backref="user", lazy=True)
    orders = db.relationship("Order", backref="user", lazy=True)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicine.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    medicine = db.relationship("Medicine")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    medicine_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

# ----------------------- INITIAL SETUP -----------------------
def create_tables():
    db.create_all()
    if not Medicine.query.first():
        meds = [
            Medicine(name="Paracetamol", price=20),
            Medicine(name="Amoxicillin", price=45),
            Medicine(name="Cough Syrup", price=60),
            Medicine(name="Vitamin C", price=35),
        ]
        db.session.bulk_save_objects(meds)
        db.session.commit()

# ----------------------- ROUTES -----------------------
@app.route("/test")
def test():
    return "✅ Flask is working!"

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    medicines = Medicine.query.all()
    return render_template_string(HOME_PAGE, medicines=medicines, username=session["username"])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Please enter username and password.", "warning")
            return redirect(url_for("signup"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("login"))
    return render_template_string(SIGNUP_PAGE)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Please enter username and password.", "warning")
            return redirect(url_for("login"))
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    return render_template_string(LOGIN_PAGE)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/add_to_cart/<int:medicine_id>")
def add_to_cart(medicine_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    cart_item = Cart.query.filter_by(user_id=session["user_id"], medicine_id=medicine_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_item = Cart(user_id=session["user_id"], medicine_id=medicine_id)
        db.session.add(new_item)
    db.session.commit()
    flash("Item added to cart!", "success")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_cart = Cart.query.filter_by(user_id=session["user_id"]).all()
    total = sum(item.medicine.price * item.quantity for item in user_cart)
    return render_template_string(CART_PAGE, cart=user_cart, total=total)

@app.route("/place_order")
def place_order():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_cart = Cart.query.filter_by(user_id=session["user_id"]).all()
    if not user_cart:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))

    total = sum(item.medicine.price * item.quantity for item in user_cart)
    new_order = Order(user_id=session["user_id"], total_amount=total)
    db.session.add(new_order)
    db.session.commit()

    for item in user_cart:
        order_item = OrderItem(order_id=new_order.id, medicine_name=item.medicine.name,
                               quantity=item.quantity, price=item.medicine.price * item.quantity)
        db.session.add(order_item)
        db.session.delete(item)
    db.session.commit()

    flash("Order placed successfully!", "success")
    return redirect(url_for("my_orders"))

@app.route("/my_orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("login"))
    orders = Order.query.filter_by(user_id=session["user_id"]).order_by(Order.date.desc()).all()
    return render_template_string(ORDERS_PAGE, orders=orders)

# ----------------------- STYLED HTML -----------------------
BOOTSTRAP = '''
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
'''

NAVBAR = '''
<nav class="navbar navbar-expand-lg navbar-dark bg-success mb-4">
  <div class="container-fluid">
    <a class="navbar-brand fw-bold" href="/">HealthyMe Pharmacy 💊</a>
    <div class="d-flex">
      {% if session.get("user_id") %}
      <a href="{{url_for('cart')}}" class="btn btn-light me-2">🛒 Cart</a>
      <a href="{{url_for('my_orders')}}" class="btn btn-warning me-2">📦 My Orders</a>
      <a href="{{url_for('logout')}}" class="btn btn-danger">Logout</a>
      {% else %}
      <a href="{{url_for('login')}}" class="btn btn-light me-2">Login</a>
      <a href="{{url_for('signup')}}" class="btn btn-warning">Signup</a>
      {% endif %}
    </div>
  </div>
</nav>
'''

HOME_PAGE = BOOTSTRAP + NAVBAR + '''
<div class="container">
  <h3 class="mb-4 text-success">Welcome, {{username}} 👋</h3>
  <div class="row">
    {% for med in medicines %}
    <div class="col-md-3 mb-3">
      <div class="card shadow-sm">
        <div class="card-body text-center">
          <h5 class="card-title">{{med.name}}</h5>
          <p class="card-text">₹{{med.price}}</p>
          <a href="{{url_for('add_to_cart', medicine_id=med.id)}}" class="btn btn-success">Add to Cart</a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
'''

SIGNUP_PAGE = BOOTSTRAP + NAVBAR + '''
<div class="container mt-5 col-md-4">
  <h3 class="text-center text-success mb-3">Signup</h3>
  <form method="post" class="card p-4 shadow-sm">
    <input name="username" class="form-control mb-3" placeholder="Username" required>
    <input name="password" type="password" class="form-control mb-3" placeholder="Password" required>
    <button type="submit" class="btn btn-success w-100">Signup</button>
  </form>
  <div class="text-center mt-2">
    <a href="{{url_for('login')}}">Already have an account? Login</a>
  </div>
</div>
'''

LOGIN_PAGE = BOOTSTRAP + NAVBAR + '''
<div class="container mt-5 col-md-4">
  <h3 class="text-center text-success mb-3">Login</h3>
  <form method="post" class="card p-4 shadow-sm">
    <input name="username" class="form-control mb-3" placeholder="Username" required>
    <input name="password" type="password" class="form-control mb-3" placeholder="Password" required>
    <button type="submit" class="btn btn-success w-100">Login</button>
  </form>
  <div class="text-center mt-2">
    <a href="{{url_for('signup')}}">Create Account</a>
  </div>
</div>
'''

CART_PAGE = BOOTSTRAP + NAVBAR + '''
<div class="container">
  <h3 class="text-success mb-3">Your Cart 🛒</h3>
  {% if cart %}
  <table class="table table-bordered bg-white shadow-sm">
    <thead><tr><th>Medicine</th><th>Qty</th><th>Price</th></tr></thead>
    <tbody>
    {% for item in cart %}
      <tr><td>{{item.medicine.name}}</td><td>{{item.quantity}}</td><td>₹{{item.medicine.price * item.quantity}}</td></tr>
    {% endfor %}
    </tbody>
  </table>
  <h4 class="text-end text-success">Total: ₹{{total}}</h4>
  <div class="text-end"><a href="{{url_for('place_order')}}" class="btn btn-warning mt-2">Place Order</a></div>
  {% else %}
  <p>Your cart is empty.</p>
  {% endif %}
</div>
'''

ORDERS_PAGE = BOOTSTRAP + NAVBAR + '''
<div class="container">
  <h3 class="text-success mb-3">My Orders 📦</h3>
  {% if orders %}
  {% for order in orders %}
    <div class="card mb-3 shadow-sm">
      <div class="card-body">
        <h5>Order #{{order.id}}</h5>
        <small class="text-muted">{{order.date.strftime("%d-%m-%Y %H:%M")}}</small>
        <ul class="mt-2">
          {% for item in order.items %}
            <li>{{item.medicine_name}} × {{item.quantity}} = ₹{{item.price}}</li>
          {% endfor %}
        </ul>
        <h6 class="text-success">Total: ₹{{order.total_amount}}</h6>
      </div>
    </div>
  {% endfor %}
  {% else %}
  <p>You haven't placed any orders yet.</p>
  {% endif %}
</div>
'''

# ----------------------- MAIN -----------------------
if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)
