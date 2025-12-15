from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flasgger import Swagger
from models import init_db, get_products, create_user, verify_user, get_db_connection, get_all_promo_codes
import seed_data

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
app = Flask(__name__, static_folder='img', static_url_path='/img')
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
init_db()
try:
    if not get_products():
        seed_data.seed_products()
    if not get_all_promo_codes():
        seed_data.seed_promo_codes()
except Exception:
    pass  # щоб не падало при старті

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
    










@app.route("/account")
def account():
    return render_template("account.html")



from flask import request, redirect, url_for, render_template


@app.route("/change_name", methods=["POST"])
def change_name():
    new_name = request.form.get("new_name")
    user_id = session.get("user_id")
    if new_name and user_id:
        conn = get_db_connection()
        conn.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, user_id))
        conn.commit()
        conn.close()
        session["username"] = new_name  # обновляем в сессии
    return redirect(url_for("account"))


@app.route("/change_email", methods=["POST"])
def change_email():
    new_email = request.form.get("new_email")
    user_id = session.get("user_id")
    if new_email and user_id:
        conn = get_db_connection()
        conn.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        conn.commit()
        conn.close()
        session["email"] = new_email  # если хочешь хранить email в сессии
    return redirect(url_for("account"))




























@app.route('/health')
def health_check():
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
    app.run(debug=True)
