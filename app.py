from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ismail_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(500))

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args.get('password') != "2025":
        return redirect('/')

    if request.method == 'POST':
        new_p = Product(
            name=request.form['name'],
            price=request.form['price'],
            image_url=request.form['image_url'],
            description=request.form['description']
        )
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for('admin', password="2025"))
        
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete/<int:id>')
def delete(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('admin', password="2025"))

@app.route('/buy/<int:id>')
def buy(id):
    p = Product.query.get_or_404(id)
    return render_template('buy.html', product=p)

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    product_name = request.form.get('product_name')
    
    whatsapp_msg = f"https://wa.me/212607367119?text=طلب جديد:%0Aالاسم: {name}%0Aالهاتف: {phone}%0Aالعنوان: {address}%0Aالمنتج: {product_name}"
    return redirect(whatsapp_msg)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('index'))

@app.route('/cart')
def show_cart():
    if 'cart' not in session or len(session['cart']) == 0:
        return render_template('cart.html', items=[], total=0)
    items = Product.query.filter(Product.id.in_(session['cart'])).all()
    total = sum(item.price for item in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)