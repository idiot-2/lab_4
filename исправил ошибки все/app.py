from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db, get_products, create_user, verify_user, get_db_connection, get_all_promo_codes
import seed_data

# Імпорт блюпрінтів
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.dot import dot_bp
from routes.api_v1 import api_v1_bp
from routes.api_v2 import api_v2_bp
from routes.errors import errors_bp

app = Flask(__name__, static_folder='img', static_url_path='/img')
app.secret_key = 'your_secret_key'

# Swagger
swagger_template = {
    "info": {
        "title": "Lab05 Shop API",
        "description": "API for products and orders",
        "version": "2.0.0"
    },
    "schemes": ["http", "https"]
}
Swagger(app, template=swagger_template)

# Ініціалізація БД
init_db()
try:
    if not get_products():
        seed_data.seed_products()
    if not get_all_promo_codes():
        seed_data.seed_promo_codes()
except Exception:
    pass

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(dot_bp)
app.register_blueprint(api_v1_bp)
app.register_blueprint(api_v2_bp)
app.register_blueprint(errors_bp)

# -------------------------------
# Маршрути сайту
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
                session['email'] = email.strip()
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
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            error = 'Неправильне ім\'я або пароль.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# -------------------------------
# Аккаунт
# -------------------------------
@app.route("/account")
def account():
    # можно передавать заказы и wishlist из базы
    orders = []   # заглушка
    wishlist = [] # заглушка
    return render_template("account.html", orders=orders, wishlist=wishlist)

import sqlite3 # Убедитесь, что это импортировано вверху app.py

# ...

@app.route("/change_name", methods=["POST"])
def change_name():
    new_name = request.form.get("new_name").strip()
    old_password = request.form.get("old_password")
    user_id = session.get("user_id")

    if not user_id or not new_name:
        flash("Неверные данные.", "error")
        return redirect(url_for("account"))

    conn = get_db_connection()
    try:
        user = conn.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
        
        if user and check_password_hash(user["password_hash"], old_password):
            try:
                conn.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, user_id))
                conn.commit()
                session["username"] = new_name
                flash("Имя пользователя успешно обновлено.", "success")
            except sqlite3.IntegrityError:
                flash("Пользователь с таким именем уже существует.", "error")
        else:
            flash("Неправильный пароль.", "error")
            
    finally:
        conn.close() 

    return redirect(url_for("account"))




@app.route("/change_email", methods=["POST"])
def change_email():
    new_email = request.form.get("new_email")
    old_password = request.form.get("old_password")
    user_id = session.get("user_id")
    if new_email and user_id:
        conn = get_db_connection()
        user = conn.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
        if user and check_password_hash(user["password_hash"], old_password):
            conn.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            conn.commit()
            session["email"] = new_email
        conn.close()
    return redirect(url_for("account"))


@app.route("/change_password", methods=["POST"])
def change_password():
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    if not new_password or new_password != confirm_password:
        return redirect(url_for("account"))

    conn = get_db_connection()
    # ИЗМЕНЕНО: SELECT password_hash вместо password
    user = conn.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,)).fetchone()
    # ИЗМЕНЕНО: user["password_hash"] вместо user["password"]
    if user and check_password_hash(user["password_hash"], old_password):
        hashed = generate_password_hash(new_password)
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, user_id)) # Обновляем password_hash
        conn.commit()
    conn.close()
    return redirect(url_for("account"))

# -------------------------------
# Health check
# -------------------------------
@app.route('/health')
def health_check():
    try:
        conn = get_db_connection()
        conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
        conn.close()
        return jsonify(status="ok", database="reachable"), 200
    except Exception as e:
        return jsonify(status="error", database="unreachable", error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
