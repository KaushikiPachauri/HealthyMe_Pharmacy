from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
db = SQLAlchemy(app)

# ----------------------- DATABASE MODELS -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cart_items = db.relationship('Cart', backref='user', lazy=True)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    medicine = db.relationship('Medicine')

# ----------------------- INITIAL DATA FUNCTION -----------------------
def create_tables():
    db.create_all()
    if not Medicine.query.first():
        meds = [
            Medicine(name='Paracetamol', price=20),
            Medicine(name='Amoxicillin', price=45),
            Medicine(name='Cough Syrup', price=60),
            Medicine(name='Vitamin C', price=35),
        ]
        db.session.bulk_save_objects(meds)
        db.session.commit()

# ----------------------- ROUTES -----------------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    medicines = Medicine.query.all()
    return render_template_string(HOME_PAGE, medicines=medicines, username=session['username'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template_string(SIGNUP_PAGE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template_string(LOGIN_PAGE)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:medicine_id>')
def add_to_cart(medicine_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cart_item = Cart.query.filter_by(user_id=session['user_id'], medicine_id=medicine_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_item = Cart(user_id=session['user_id'], medicine_id=medicine_id)
        db.session.add(new_item)
    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_cart = Cart.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.medicine.price * item.quantity for item in user_cart)
    return render_template_string(CART_PAGE, cart=user_cart, total=total)

# ----------------------- HTML TEMPLATES -----------------------
HOME_PAGE = '''
<!DOCTYPE html><html><head><title>HealthyMe Pharmacy</title></head><body>
<h2>Welcome, {{username}} 👋</h2>
<a href="{{url_for('cart')}}">🛒 View Cart</a> | 
<a href="{{url_for('logout')}}">Logout</a>
<h3>Medicines Available</h3>
<ul>
{% for med in medicines %}
  <li>{{med.name}} - ₹{{med.price}} 
  <a href="{{url_for('add_to_cart', medicine_id=med.id)}}">[Add to Cart]</a></li>
{% endfor %}
</ul>
</body></html>
'''

SIGNUP_PAGE = '''
<!DOCTYPE html><html><body>
<h2>Signup</h2>
<form method="post">
Username: <input name="username" required><br>
Password: <input name="password" type="password" required><br>
<button type="submit">Signup</button>
</form>
<a href="{{url_for('login')}}">Already have an account? Login</a>
</body></html>
'''

LOGIN_PAGE = '''
<!DOCTYPE html><html><body>
<h2>Login</h2>
<form method="post">
Username: <input name="username" required><br>
Password: <input name="password" type="password" required><br>
<button type="submit">Login</button>
</form>
<a href="{{url_for('signup')}}">Create Account</a>
</body></html>
'''

CART_PAGE = '''
<!DOCTYPE html><html><body>
<h2>Your Cart</h2>
<a href="{{url_for('home')}}">⬅ Back to Medicines</a><br><br>
<ul>
{% for item in cart %}
  <li>{{item.medicine.name}} × {{item.quantity}} = ₹{{item.medicine.price * item.quantity}}</li>
{% endfor %}
</ul>
<h3>Total: ₹{{total}}</h3>
</body></html>
'''

# ----------------------- RUN APP -----------------------
if __name__ == '__main__':
    with app.app_context():
        create_tables()  # ✅ manually create tables before starting server
    app.run(debug=True)
