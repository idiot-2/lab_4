from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, get_products, create_user, verify_user
import seed_data
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.dot import dot_bp
from routes.api import api_bp



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Необхідно для роботи з сесіями
app.register_blueprint(api_bp)

# Ініціалізація бази даних
init_db()

# Якщо в таблиці `products` немає записів — додаємо тестові дані
try:
    if not get_products():
        seed_data.seed_products()
except Exception:
    # Якщо щось піде не так — нехай додатково не падає сервіс при старті
    pass

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(dot_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if not username or not email or not password:
            error = 'Всі поля обов\'язкові.'
        elif password != confirm:
            error = 'Паролі не співпадають.'
        else:
            user_id = create_user(username.strip(), email.strip(), password)
            if user_id:
                session['username'] = username.strip()
                session['user_id'] = user_id
                return redirect(url_for('home'))
            else:
                error = 'Користувач з таким ім\'ям або email вже існує.'
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        user = verify_user(identifier.strip(), password)
        if user:
            session['username'] = user['username']
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            error = 'Неправильне ім\'я або пароль.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
