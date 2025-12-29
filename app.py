import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ismail_123'

# التعديل السحري هنا: كنفرضوا على السيرفر يكتب فـ باريس
db_folder = '/app/db'

# إلا كنا فـ Koyeb، كنستعملو الخزنة، وإلا كنستعملو ملف محلي للتيست
if os.environ.get('KOYEB_SERVICE_ID'):
    if not os.path.exists(db_folder):
        try:
            os.makedirs(db_folder)
        except:
            pass
    db_path = os.path.join(db_folder, 'shop.db')
else:
    db_path = 'shop.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(500))
    affiliate_link = db.Column(db.String(500))

with app.app_context():
    db.create_all()

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
    entered_password = request.args.get('password') or request.form.get('password')
    
    if entered_password != "2025":
        return '''
            <div style="text-align: center; padding: 100px 20px; font-family: sans-serif; direction: ltr;">
                <h2 style="color: #1a1a1a;">Admin Login</h2>
                <form method="POST">
                    <input type="password" name="password" placeholder="Enter Password" style="padding: 12px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; width: 200px;"><br>
                    <button type="submit" style="background: #000; color: #fff; border: none; padding: 10px 25px; border-radius: 8px; font-weight: bold; cursor: pointer;">Login</button>
                </form>
            </div>
        '''

    if request.method == 'POST' and 'name' in request.form:
        new_p = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            image_url=request.form['image_url'],
            description=request.form['description'],
            affiliate_link=request.form['affiliate_link']
        )
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for('index'))
        
    products = Product.query.all()
    return render_template('admin.html', products=products, title="Admin Panel")

@app.route('/buy/<int:id>')
def buy(id):
    p = Product.query.get_or_404(id)
    return render_template('buy.html', product=p, title=p.name)

@app.route('/delete/<int:id>')
def delete(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



