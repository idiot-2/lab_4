# Звіт з лабораторної роботи 3

## Розробка базового вебпроєкту

### Інформація про команду
- Назва команди: Ті Самі Програмісти

- Учасники:
  - Терещук Дмитро (роль: Front-end dev.)
  - Антонюк Андрій (роль: Support dev.)
  - Корець Ярослав (роль: DB dev.)

## Завдання

### Обрана предметна область

Магазин ключів ігор Steam

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [+] Рівень 1: Створено сторінки "Головна" та "Про нас"
- [+] Рівень 2: Додано мінімум дві додаткові статичні сторінки з меню та адаптивною версткою

## Хід виконання роботи

Обговорили ідею для сайту, розподілили ролі на кожного та написали код на VSCode 
 за допомогою шаблонів та використання ШІ як зразку
### Підготовка середовища розробки

Опишіть процес встановлення та налаштування:

- Версія Python: 3.14
- Встановлення Flask: створення віртуального середовища для роботи і встановлення фласку: 
"python -m venv venv
venv\Scripts\Activate.ps1
pip install Flask"
- Інші використані інструменти: -

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
project/
├── app.py
├── templates/
│   ├── about.html
│   ├── admin.html
│   ├── base.html
│   └── ...
├── routes/
│   ├── __pycache__
│   ├── __init__.py
│   └── admin.py
│   └── ...
└── lab-reports/
    └── lab03-report-student-kcepka.md
```

### Опис реалізованих сторінок

#### Головна: 
Титульна сторінка сайту

#### Магазин: 
Список товарів магазину

#### Кошик: 
Перелік товарів доданих до кошику

#### Про нас: 
Сторінка з описом команди що створила сайт

#### Зворотній зв'язок: 
Сторінка для залишку відгуку

#### Адмін: 
Сторінка для керування замовленнями, перегляду відгуків

## Ключові фрагменти коду



### Маршрутизація в Flask

Наведіть приклад налаштування маршрутів у файлі `app.py`:

```python
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
```

### Базовий шаблон

Наведіть фрагмент базового шаблону `base.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .bar {
            transition: all 0.3s ease-in-out;
        }

        /* Dark theme: black background, light text */
        body {
            background-color: #000000;
            color: #e6e6e6;
        }
</head>
<body>
    <main class="flex-grow container mx-auto px-4 py-8">
        <div class="card-dark shadow-md rounded-lg p-6">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="bg-black text-white py-4 mt-auto border-t-2 border-purple-600">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2025 SteamKeysForYou. Всі права захищені.</p>
        </div>
    </footer>
</body>
</html>
```

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Терещук Дмитро: Створив базовий шаблон для сайту, оформив його дизайн
- Антонюк Андрій: Удосконалював код, виправляв помилки в його роботі
- Корець Ярослав: Реалізував базу данних

## Скріншоти


### Головна сторінка

![Головна сторінка](https://drive.google.com/file/d/1FFMMdHz4GnO9iW9Ab7zHlgDfe9pDDtHw/view?usp=drive_link)

### Сторінка "Про нас"

![Сторінка Про нас](https://drive.google.com/file/d/1qgFj_LKiJqUWqSWTn5rfo28PGVKv5HCB/view?usp=drive_link)

### Сторінка "Кошик"

![Сторінка "Кошик"](https://drive.google.com/file/d/1NRKWRNTvpMGTmz1ePt9EAmnyrWYHf1Rx/view?usp=drive_link)

#### Сторінка "Зворотній зв'язок"

![Сторінка "Зворотній зв'язок"](https://drive.google.com/file/d/1Rn79ofpTdxQaLOOOQK6t-6caOCfQcUGp/view?usp=drive_link)

### Висновки

Опишіть:

- Отримали досвід роботи з Flask
- Для подальшої розробки можна додати варіант придбання готових аккаунтів з набором ігор

Очікувана оцінка: 9

Обґрунтування: Ми придумали актуальну ідею, реалізували хороший дизайн та оптимізований код зі своєю базою данних
