from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flasgger import Swagger
from models import init_db, get_products, create_user, verify_user
import seed_data
import os

# Імпорт блюпрінтів
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.dot import dot_bp
from routes.api_v1 import api_v1_bp as api_v1_bp   # <-- api_v1
from routes.api_v2 import api_v2_bp             # <--  api_v2
from routes.errors import errors_bp             # <-- глобальні хендлери

# -------------------------------
# Створення Flask‑додатку
# -------------------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # для роботи з сесіями

# -------------------------------
# Swagger / Flasgger configuration
# -------------------------------
swagger_template = {
    "info": {
        "title": "Lab05 Shop API",
        "description": "API for products and orders (Lab05, with validation, versions, error handling)",
        "version": "2.0.0"
    },
    "schemes": ["http", "https"]
}
Swagger(app, template=swagger_template)

# -------------------------------
# Ініціалізація бази даних
# -------------------------------
# init_db()  # moved to conftest
# try:
#     if not os.environ.get('TESTING') and not get_products():
#         seed_data.seed_products()
# except Exception:
#     pass  # щоб не падало при старті

# -------------------------------
# Реєстрація блюпрінтів
# -------------------------------
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(dot_bp)
app.register_blueprint(api_v1_bp)   # <-- v1
app.register_blueprint(api_v2_bp)   # <-- v2
app.register_blueprint(errors_bp)   # <-- errors

# -------------------------------
# Маршрути для сайту
# -------------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/api-demo")
def api_demo():
    return render_template("api-demo.html")

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

@app.route('/health')
def health_check():
    if os.environ.get('TESTING'):
        return jsonify(status="ok", database="test"), 200
    try:
        conn = get_db_connection()
        # Проста перевірка — отримати таблиці
        conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
        conn.close()
        return jsonify(status="ok", database="reachable"), 200
    except Exception as e:
        return jsonify(status="error", database="unreachable", error=str(e)), 500

# -------------------------------
# Запуск
# -------------------------------
if __name__ == '__main__':
    init_db()
    if not get_products():
        seed_data.seed_products()
    app.run(debug=True)
