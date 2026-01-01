import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ismail_123'

db_path = '/tmp/shop.db'

if not os.path.exists('/tmp'):
    os.makedirs('/tmp')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    image_url = db.Column(db.Text)
    description = db.Column(db.Text)
    affiliate_link = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.before_request
def make_session_permanent():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    entered_password = request.args.get('password') or request.form.get('password')
    
    if entered_password != "2025":
        return '''
            <div style="text-align: center; padding: 100px 20px; font-family: sans-serif; direction: ltr;">
                <h2 style="color: #1a1a1a;">Admin Login</h2>
                <form method="POST" style="display: inline-block; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <input type="password" name="password" placeholder="Enter Password" style="padding: 12px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; width: 200px;"><br>
                    <button type="submit" style="background: #000; color: #fff; border: none; padding: 10px 25px; border-radius: 8px; font-weight: bold; cursor: pointer;">Login</button>
                </form>
                <p><a href="/" style="color: #666; text-decoration: none; font-size: 0.9rem;">Back to Store</a></p>
            </div>
        '''

    if request.method == 'POST' and 'name' in request.form:
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







