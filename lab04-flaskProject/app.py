from flask import Flask, render_template, request
from models import init_db, insert_client
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ініціалізація бази даних
init_db()

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)

# --- ГОЛОВНІ СТОРІНКИ ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


# --- РЕЄСТРАЦІЯ КЛІЄНТА ---
@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    insert_client(first_name, last_name, email, phone)

    return "Клієнта успішно зареєстровано!"


if __name__ == '__main__':
    app.run(debug=True)