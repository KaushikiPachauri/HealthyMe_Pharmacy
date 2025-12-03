# HealthyMe Pharmacy - Single File Full App
# Author: Kaushiki Pachauri
# Tech: Python (Flask), SQLAlchemy, HTML, CSS, JS
# Run: python HealthyMe_Pharmacy.py
# Then open http://127.0.0.1:5000 in your browser

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

app = Flask(__name__)

# -----------------------------
# DATABASE SETUP (SQLite)
# -----------------------------
class Base(DeclarativeBase):
    pass

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(150))
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    liked = Column(Boolean, default=False)
    image = Column(String(300))

engine = create_engine("sqlite:///database.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Add sample data if database empty
session = Session()
if not session.query(Medicine).first():
    meds = [
        Medicine(name='Paracetamol 500mg', brand='Acme Pharma', description='Pain reliever and fever reducer', price=20, stock=100),
        Medicine(name='Cetirizine 10mg', brand='AllergyCare', description='Antihistamine for allergy relief', price=30, stock=50),
        Medicine(name='Amoxicillin 500mg', brand='BioMed', description='Antibiotic (prescription required)', price=120, stock=30)
    ]
    session.add_all(meds)
    session.commit()
session.close()


# -----------------------------
# BACKEND ROUTES (API)
# -----------------------------
@app.route('/api/medicines')
def get_medicines():
    q = request.args.get('q', '').lower()
    session = Session()
    meds = session.query(Medicine).all()
    if q:
        meds = [m for m in meds if q in m.name.lower() or (m.brand and q in m.brand.lower())]
    data = [{
        'id': m.id,
        'name': m.name,
        'brand': m.brand,
        'description': m.description,
        'price': m.price,
        'stock': m.stock,
        'liked': m.liked,
        'image': m.image
    } for m in meds]
    session.close()
    return jsonify(data)

@app.route('/api/medicines/<int:med_id>/like', methods=['POST'])
def toggle_like(med_id):
    session = Session()
    med = session.get(Medicine, med_id)
    if not med:
        session.close()
        return jsonify({'error': 'Not found'}), 404
    med.liked = not med.liked
    session.commit()
    data = {'id': med.id, 'liked': med.liked}
    session.close()
    return jsonify(data)

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    items = request.json.get('items', [])
    session = Session()
    for it in items:
        med = session.get(Medicine, it['id'])
        if not med or med.stock < it['qty']:
            session.close()
            return jsonify({'error': f'{med.name if med else "Unknown"} out of stock'}), 400
    for it in items:
        med = session.get(Medicine, it['id'])
        med.stock -= it['qty']
    session.commit()
    session.close()
    return jsonify({'status': 'success', 'message': 'Order placed (mock)'})

# -----------------------------
# FRONTEND (HTML + CSS + JS)
# -----------------------------
@app.route('/')
def home():
    return """
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <title>HealthyMe Pharmecy</title>
  <style>
    body{font-family:Arial, sans-serif;margin:0;padding:0;background:#f6f8fa;}
    header{background:#2196F3;color:white;padding:10px;display:flex;align-items:center;gap:10px;}
    input{padding:6px;width:200px;border:none;border-radius:4px;}
    button{padding:6px 10px;border:none;border-radius:4px;background:#1976D2;color:white;cursor:pointer;}
    #medList{display:flex;flex-wrap:wrap;gap:15px;padding:15px;}
    .med{background:white;border-radius:8px;padding:10px;width:220px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}
    .med h4{margin:5px 0;}
    #cartPanel{position:fixed;right:10px;top:70px;width:300px;background:white;border:1px solid #ccc;padding:10px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.2);display:none;}
  </style>
</head>
<body>
  <header>
    <h2 style='margin:0;'>HealthyMe Pharmecy</h2>
    <input id='search' placeholder='Search medicine...'>
    <button onclick='searchMeds()'>Search</button>
    <button onclick='toggleCart()'>🛒 Cart (<span id='cartCount'>0</span>)</button>
  </header>

  <main id='medList'></main>

  <div id='cartPanel'>
    <h3>Your Cart</h3>
    <div id='cartItems'></div>
    <button onclick='checkout()'>Checkout</button>
    <button onclick='toggleCart()'>Close</button>
  </div>

  <script>
    let cart = [];

    async function fetchMeds(q=''){
      let url = '/api/medicines';
      if(q) url += '?q='+encodeURIComponent(q);
      const res = await fetch(url);
      return res.json();
    }

    async function renderMeds(q=''){
      const meds = await fetchMeds(q);
      const list = document.getElementById('medList');
      list.innerHTML = '';
      meds.forEach(m=>{
        const div = document.createElement('div');
        div.className='med';
        div.innerHTML = `
          <h4>${m.name}</h4>
          <small>${m.brand||''}</small>
          <p>${m.description||''}</p>
          <b>₹ ${m.price}</b> | Stock: ${m.stock}<br>
          <button onclick='likeMed(${m.id}, this)'>${m.liked?'♥':'♡'}</button>
          <button onclick='addToCart(${m.id})'>Add to cart</button>
        `;
        list.appendChild(div);
      });
    }

    async function likeMed(id,btn){
      const res = await fetch('/api/medicines/'+id+'/like',{method:'POST'});
      const data = await res.json();
      btn.textContent = data.liked ? '♥':'♡';
    }

    function addToCart(id){
      const item = cart.find(i=>i.id===id);
      if(item) item.qty++; else cart.push({id, qty:1});
      document.getElementById('cartCount').textContent = cart.reduce((a,i)=>a+i.qty,0);
    }

    function toggleCart(){
      const panel=document.getElementById('cartPanel');
      panel.style.display = panel.style.display==='none' || panel.style.display===''?'block':'none';
      const items=document.getElementById('cartItems');
      items.innerHTML = cart.map(i=>`<div>Item ID ${i.id} x ${i.qty}</div>`).join('');
    }

    async function checkout(){
      if(cart.length===0){alert('Cart empty');return;}
      const res = await fetch('/api/cart/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:cart})});
      const data = await res.json();
      alert(data.message||data.error);
      if(data.status==='success'){cart=[];document.getElementById('cartCount').textContent='0';toggleCart();}
    }

    function searchMeds(){
      const q=document.getElementById('search').value;
      renderMeds(q);
    }

    renderMeds();
  </script>
</body>
</html>
"""

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    print("✅ HealthyMe Pharmecy running on http://127.0.0.1:5000")
    app.run(debug=True)
