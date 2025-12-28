from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ismail_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

# Database model with affiliate_link support
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(500))
    affiliate_link = db.Column(db.String(500))

# هاد السطر هو اللي كيصايب الجداول في Koyeb بلا ما يحتاج ملف .db خارجي
with app.app_context():
    db.create_all()

# Initialize Shopping Cart in session
@app.before_request
def make_session_permanent():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products, title="Home")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args.get('password') != "2025":
        return redirect('/')

    if request.method == 'POST':
        new_p = Product(
            name=request.form['name'],
            price=request.form['price'],
            image_url=request.form['image_url'],
            description=request.form['description'],
            affiliate_link=request.form['affiliate_link']
        )
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for('admin', password="2025"))
        
    products = Product.query.all()
    return render_template('admin.html', products=products, title="Admin Panel")

@app.route('/buy/<int:id>')
def buy(id):
    p = Product.query.get_or_404(id)
    return render_template('buy.html', product=p, title=p.name)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    p = Product.query.get_or_404(id)
    cart = session.get('cart', [])
    cart.append({'id': p.id, 'name': p.name, 'price': p.price})
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    items = session.get('cart', [])
    total = sum(item['price'] for item in items)
    return render_template('cart.html', items=items, total=total, title="My Cart")

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

@app.route('/delete/<int:id>')
def delete(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('admin', password="2025"))

if __name__ == '__main__':
    app.run(debug=True)
