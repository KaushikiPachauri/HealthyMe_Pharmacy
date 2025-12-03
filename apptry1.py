<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Friends Pharmeasy Store</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"><style>
  
/* General Reset */
  
* {
  
    margin: 0;
  
    padding: 0;
  
    box-sizing: border-box;
  
    font-family: 'Montserrat', sans-serif;
  
}
  
body {
  
    background: linear-gradient(to right, #e2e2e2, #c9d6ff);
  
    display: flex;
  
    flex-direction: column;
  
    align-items: center;
  
    justify-content: flex-start;
  
    min-height: 100px;
  
    padding: 20px;
  
    position: relative;
  
}
  

  
/* Header with Logo */
  
.header {
  
    position: fixed;
  
    top: 20px;
  
    left: 20px;
  
    display: flex;
  
    align-items: center;
  
    gap: 10px;
  
    z-index: 1001;
  
}
  
.header img {
  
    width: 60px;
  
    height: 60px;
  
    object-fit: contain;
  
    border-radius: 8px;
  
}
  
.header h1 {
  
    font-size: 18px;
  
    font-weight: 700;
  
    color: #333;
  
}
  

  
/* Cart Icon */
  
#cartIcon {
  
    position: fixed;
  
    top: 20px;
  
    right: 20px;
  
    cursor: pointer;
  
    font-size: 28px;
  
    z-index: 1000;
  
}
  
#cartIcon span {
  
    background: #6C63FF;
  
    color: #fff;
  
    border-radius: 50%;
  
    padding: 2px 8px;
  
    font-size: 14px;
  
    vertical-align: top;
  
}
  

  
/* Search Bar */
  
#searchContainer {
  
    margin: 100px 0 20px;
  
    width: 80%;
  
    max-width: 600px;
  
    display: flex;
  
    justify-content: center;
  
}
  
#searchContainer input {
  
    width: 100%;
  
    padding: 10px 15px;
  
    border-radius: 8px;
  
    border: none;
  
    font-size: 16px;
  
    outline: none;
  
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  
}
  

  
/* Container for Login/Signup Forms */
  
.container {
  
    position: relative;
  
    width: 768px;
  
    max-width: 100%;
  
    min-height: 480px;
  
    background: #fff;
  
    border-radius: 30px;
  
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.35);
  
    overflow: hidden;
  
    margin-bottom: 30px;
  
}
  

  
/* Forms */
  
form {
  
    display: flex;
  
    flex-direction: column;
  
    justify-content: center;
  
    align-items: center;
  
    padding: 50px 40px;
  
    height: 100%;
  
    background-color: #fff;
  
}
  
form h1 {
  
    font-weight: 700;
  
    margin-bottom: 20px;
  
}
  
form input {
  
    width: 100%;
  
    padding: 10px 15px;
  
    margin: 8px 0;
  
    border: none;
  
    border-radius: 8px;
  
    background-color: #eee;
  
    font-size: 14px;
  
    outline: none;
  
}
  
form button {
  
    margin-top: 20px;
  
    padding: 12px;
  
    width: 100%;
  
    border: none;
  
    background: #6C63FF;
  
    color: #fff;
  
    font-size: 16px;
  
    border-radius: 5px;
  
    cursor: pointer;
  
}
  
form button:hover {
  
    background: #574fd6;
  
}
  

  
.social-icons {
  
    display: flex;
  
    justify-content: space-around;
  
    margin: 20px 0;
  
}
  
.social-icons a {
  
    display: inline-flex;
  
    justify-content: center;
  
    align-items: center;
  
    width: 40px;
  
    height: 40px;
  
    border: 1px solid #ccc;
  
    border-radius: 50%;
  
    font-size: 20px;
  
    color: #555;
  
    transition: 0.3s;
  
}
  
.social-icons a:hover {
  
    color: #6C63FF;
  
}
  

  
span {
  
    font-size: 12px;
  
    color: #777;
  
    margin-bottom: 10px;
  
}
  
a {
  
    font-size: 12px;
  
    color: #6C63FF;
  
    text-decoration: none;
  
    margin-top: 10px;
  
}
  
a:hover {
  
    text-decoration: underline;
  
}
  

  
/* Form Containers */
  
.form-container {
  
    position: absolute;
  
    top: 0;
  
    height: 100%;
  
    width: 50%;
  
    transition: all 0.6s ease-in-out;
  
}
  
.sign-in { left: 0; z-index: 2; }
  
.container.active .sign-in { transform: translateX(100%); }
  
.sign-up { left: 0; opacity: 0; z-index: 1; }
  
.container.active .sign-up { transform: translateX(100%); opacity: 1; z-index: 5; }
  

  
/* Toggle Panels */
  
.toggle-container {
  
    position: absolute;
  
    top: 0;
  
    left: 50%;
  
    width: 50%;
  
    height: 100%;
  
    overflow: hidden;
  
    border-radius: 150px 0 0 100px;
  
    z-index: 1000;
  
    transition: all 0.6s ease-in-out;
  
}
  
.container.active .toggle-container { transform: translateX(-100%); border-radius: 0 150px 100px 0; }
  

  
.toggle {
  
    background: linear-gradient(to right, #5c6bc0, #512da8);
  
    color: #fff;
  
    position: relative;
  
    left: -100%;
  
    width: 200%;
  
    height: 100%;
  
    transition: all 0.6s ease-in-out;
  
}
  
.container.active .toggle { transform: translateX(50%); }
  

  
.toggle-panel {
  
    position: absolute;
  
    width: 50%;
  
    height: 100%;
  
    display: flex;
  
    flex-direction: column;
  
    align-items: center;
  
    justify-content: center;
  
    padding: 0 30px;
  
    text-align: center;
  
    top: 0;
  
}
  
.toggle-left { transform: translateX(-200%); }
  
.container.active .toggle-left { transform: translateX(0); }
  
.toggle-right { right: 0; transform: translateX(0); }
  
.container.active .toggle-right { transform: translateX(200%); }
  

  
/* Products Display */
  
.product-display {
  
    display: none;
  
    flex-direction: column;
  
    align-items: center;
  
    width: 100%;
  
    margin-bottom: 30px;
  
}
  
.product-display h2 { margin-bottom: 20px; }
  
.product-gallery {
  
    display: flex;
  
    flex-wrap: wrap;
  
    justify-content: center;
  
    gap: 20px;
  
}
  
.product-item {
  
    background: #fff;
  
    border-radius: 10px;
  
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  
    padding: 15px;
  
    text-align: center;
  
    width: 180px;
  
    cursor: pointer;
  
}
  
.product-item img {
  
    width: 100%;
  
    border-radius: 10px;
  
    margin-bottom: 10px;
  
    transition: transform 0.3s;
  
}
  
.product-item img:hover {
  
    transform: scale(1.05);
  
}
  
.product-name {
  
    font-weight: 600;
  
    font-size: 14px;
  
    color: #333;
  
    margin-bottom: 5px;
  
}
  
.product-price {
  
    font-size: 13px;
  
    color: #666;
  
    margin-bottom: 10px;
  
}
  
.quantity-control {
  
    display: flex;
  
    justify-content: center;
  
    align-items: center;
  
    margin-top: 5px;
  
}
  
.quantity-control button {
  
    padding: 5px 10px;
  
    margin: 0 5px;
  
    border: none;
  
    background: #6C63FF;
  
    color: #fff;
  
    border-radius: 5px;
  
    cursor: pointer;
  
}
  
.quantity-control span {
  
    font-size: 16px;
  
    font-weight: 600;
  
}
  

  
/* Cart Section */
  
.cart-section {
  
    display: none;
  
    margin-top: 30px;
  
    width: 80%;
  
    max-width: 700px;
  
    background: #fff;
  
    padding: 20px;
  
    border-radius: 10px;
  
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  
}
  
.cart-section h2 { margin-bottom: 15px; }
  
.cart-items { min-height: 50px; margin-bottom: 15px; }
  
.cart-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  
.cart-total { font-size: 18px; margin-bottom: 15px; }
  

  
.cart-buttons {
  
    display: flex;
  
    gap: 10px;
  
}
  

  
#checkoutBtn, #resetBtn {
  
    flex: 1;
  
    padding: 12px;
  
    border: none;
  
    border-radius: 5px;
  
    color: #fff;
  
    cursor: pointer;
  
}
  
#checkoutBtn { background: #6C63FF; }
  
#checkoutBtn:hover { background: #574fd6; }
  
#resetBtn { background: #f44336; }
  
#resetBtn:hover { background: #d32f2f; }
  

  
/* Popup Modal */
  
#imageModal {
  
    display: none;
  
    position: fixed;
  
    z-index: 2000;
  
    padding-top: 60px;
  
    left: 0;
  
    top: 0;
  
    width: 100%;
  
    height: 100%;
  
    overflow: auto;
  
    background-color: rgba(0,0,0,0.8);
  
}
  
#imageModal img {
  
    margin: auto;
  
    display: block;
  
    max-width: 80%;
  
    max-height: 80%;
  
    border-radius: 10px;
  
}
  
#imageModal span {
  
    position: absolute;
  
    top: 30px;
  
    right: 50px;
  
    color: white;
  
    font-size: 40px;
  
    font-weight: bold;
  
    cursor: pointer;
  
}
  
</style></head><body><!-- Logo Header --><div class="header"><img src="logo.png" alt="Friends Logo">

<h1>Friends Pharmeasy Store</h1>

</div><!-- Cart Icon --><div id="cartIcon"><i class="fa-solid fa-cart-shopping"></i>

<span id="cartCount">0</span>

</div><!-- Login/Signup Forms --><div class="container" id="container"><!-- (Login/Signup content remains same) -->

<div class="form-container sign-up">

    <form>

        <h1>Create Account</h1>

        <input type="text" placeholder="Name" required />

        <input type="email" placeholder="Email" required />

        <input type="password" placeholder="Password" required />

        <button type="button" id="signUpBtn">Sign Up</button>

    </form>

</div>



<div class="form-container sign-in" id="signinContainer">

    <form id="signInForm">

        <h1>Sign In</h1>

        <input type="email" placeholder="Email" required />

        <input type="password" placeholder="Password" required />

        <button type="submit">Sign In</button>

    </form>

</div>



<div class="toggle-container">

    <div class="toggle">

        <div class="toggle-panel toggle-left">

            <h1>Welcome Back!</h1>

            <button class="hidden" id="login">Sign In</button>

        </div>

        <div class="toggle-panel toggle-right">

            <h1>Hello, Friend!</h1>

            <button class="hidden" id="register">Sign Up</button>

        </div>

    </div>

</div>

</div><!-- Search Bar --><div id="searchContainer"><input type="text" id="searchInput" placeholder="Search products...">

</div><!-- Products Section --><div class="product-display" id="productDisplay"><h2>Medical Products Store</h2>

<div class="product-gallery" id="productGallery">

    <div class="product-item">

        <img src="Atom.jpg" alt="Atom Protein Powder">

        <p class="product-name">Atom Protein Powder</p>

        <p class="product-price">MRP: ₹1999</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Cyrup.webp" alt="Cyrup Syrup">

        <p class="product-name">Cyrup Syrup</p>

        <p class="product-price">MRP: ₹249</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Everherb .png" alt="Aloevera Juice">

        <p class="product-name">Aloevera Juice</p>

        <p class="product-price">MRP: ₹549</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Atom.jpg" alt="Atom Mass Gainer">

        <p class="product-name">Atom Mass Gainer</p>

        <p class="product-price">MRP: ₹2499</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="intramuscular-injection_thumb-1-732x549-1.jpg" alt="intramuscular-injection_thumb-1-732x549-1">

        <p class="product-name">intramuscular-injection_thumb-1-732x549-1</p>

        <p class="product-price">MRP: ₹149</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Ipca Acne.png" alt="Ipca Acne">

        <p class="product-name">Ipca Acne</p>

        <p class="product-price">MRP: ₹549</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="kevinanabolic-1800x1800-1--500x500.webp" alt="Anabolic Mass Gainer">

        <p class="product-name">Anabolic Mass Gainer</p>

        <p class="product-price">MRP: ₹4999</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>        

    <div class="product-item">

        <img src="Medicine.png" alt="Peraceta">

        <p class="product-name">Peraceta</p>

        <p class="product-price">MRP: ₹269</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Men'S Diabetic.png" alt="Men'S Diabestic Sleepers">

        <p class="product-name">Men'S Diabestic Sleepers</p>

        <p class="product-price">MRP: ₹449</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="Neurobion.png" alt="Neurobion">

        <p class="product-name">Neurobion</p>

        <p class="product-price">MRP: ₹119</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

    <div class="product-item">

        <img src="ylfuylfxrh0cvzrxopf3.avif" alt="Saridon">

        <p class="product-name">Saridon</p>

        <p class="product-price">MRP: ₹239</p>

        <div class="quantity-control">

            <button class="decrease">-</button>

            <span class="quantity">0</span>

            <button class="increase">+</button>

        </div>

    </div>

</div>

</div><!-- Cart Section --><div class="cart-section" id="cartSection"><h2>Shopping Cart</h2>

<div class="cart-items" id="cartItems">

    <p>Your cart is empty</p>

</div>

<div class="cart-total">

    <strong>Total: ₹<span id="cartTotal">0</span></strong>

</div>

<div class="cart-buttons">

    <button id="checkoutBtn">Checkout</button>

    <button id="resetBtn">Reset</button>

</div>

</div><!-- Image Popup Modal --><div id="imageModal"><span id="closeModal">&times;</span>

<img id="modalImage" src="" alt="Popup Image">

</div><script>
  
// Toggle Forms
  
const container = document.getElementById('container');
  
const registerBtn = document.getElementById('register');
  
const loginBtn = document.getElementById('login');
  
registerBtn?.addEventListener('click', () => container.classList.add("active"));
  
loginBtn?.addEventListener('click', () => container.classList.remove("active"));
  

  
// Sign In
  
const signInForm = document.getElementById('signInForm');
  
const productDisplay = document.getElementById('productDisplay');
  
const cartSection = document.getElementById('cartSection');
  
signInForm.addEventListener('submit', function(e){
  
    e.preventDefault();
  
    container.style.display = 'none';
  
    productDisplay.style.display = 'flex';
  
    cartSection.style.display = 'block';
  
    updateCart();
  
});
  

  
// Cart Logic
  
const cartItems = document.getElementById('cartItems');
  
const cartTotal = document.getElementById('cartTotal');
  
const cartCount = document.getElementById('cartCount');
  

  
function updateCart() {
  
    let total = 0;
  
    let totalItems = 0;
  
    cartItems.innerHTML = '';
  
    const products = document.querySelectorAll('.product-item');
  
    products.forEach(item => {
  
        const name = item.querySelector('img').alt;
  
        const price = parseInt(item.querySelector('.product-price').textContent.replace('MRP: ₹',''));
  
        const quantity = parseInt(item.querySelector('.quantity').textContent);
  
        if(quantity > 0){
  
            const div = document.createElement('div');
  
            div.classList.add('cart-item');
  
            div.innerHTML = <p>${name} x ${quantity}</p><p>₹${price * quantity}</p>;
  
            cartItems.appendChild(div);
  
            total += price * quantity;
  
            totalItems += quantity;
  
        }
  
    });
  
    if(total === 0) cartItems.innerHTML = '<p>Your cart is empty</p>';
  
    cartTotal.textContent = total;
  
    cartCount.textContent = totalItems;
  
}
  

  
// Quantity Buttons
  
document.querySelectorAll('.product-item').forEach(item => {
  
    const dec = item.querySelector('.decrease');
  
    const inc = item.querySelector('.increase');
  
    const qty = item.querySelector('.quantity');
  

  
    dec.addEventListener('click', () => {
  
        let q = parseInt(qty.textContent);
  
        if(q > 0) q--;
  
        qty.textContent = q;
  
        updateCart();
  
    });
  

  
    inc.addEventListener('click', () => {
  
        let q = parseInt(qty.textContent);
  
        q++;
  
        qty.textContent = q;
  
        updateCart();
  
    });
  
});
  

  
// Checkout
  
document.getElementById('checkoutBtn').addEventListener('click', () => {
  
    if(cartCount.textContent > 0){
  
        alert('Checkout Successful! Total: ₹' + cartTotal.textContent);
  
    } else {
  
        alert('Your cart is empty!');
  
    }
  
});
  

  
// ✅ Reset Button Functionality
  
document.getElementById('resetBtn').addEventListener('click', () => {
  
    document.querySelectorAll('.quantity').forEach(q => q.textContent = '0');
  
    updateCart();
  
    alert('Cart has been reset!');
  
});
  

  
// Toggle cart section
  
document.getElementById('cartIcon').addEventListener('click', () => {
  
    if(cartSection.style.display === 'none' || cartSection.style.display === ''){
  
        cartSection.style.display = 'block';
  
    } else {
  
        cartSection.style.display = 'none';
  
    }
  
});
  

  
// Search Functionality
  
const searchInput = document.getElementById('searchInput');
  
const productGallery = document.getElementById('productGallery');
  
searchInput.addEventListener('input', () => {
  
    const searchTerm = searchInput.value.toLowerCase();
  
    const products = productGallery.querySelectorAll('.product-item');
  
    products.forEach(product => {
  
        const name = product.querySelector('img').alt.toLowerCase();
  
        product.style.display = name.includes(searchTerm) ? 'block' : 'none';
  
    });
  
});
  

  
// Image Popup Modal
  
const modal = document.getElementById('imageModal');
  
const modalImg = document.getElementById('modalImage');
  
const closeModal = document.getElementById('closeModal');
  

  
document.querySelectorAll('.product-item img').forEach(img => {
  
    img.addEventListener('click', () => {
  
        modal.style.display = 'block';
  
        modalImg.src = img.src;
  
    });
  
});
  

  
closeModal.addEventListener('click', () => {
  
    modal.style.display = 'none';
  
});
  
window.addEventListener('click', (e) => {
  
    if(e.target === modal){
  
        modal.style.display = 'none';
  
    }
  
});
  
</script></body></html>
