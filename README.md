# Booking System

Система бронювання кімнат на Django.

## 📌 Опис
Цей проект представляє з себе систему бронювань кімнат, є можливість переглядати свої бронювання, усі кімнати, бронювання кімнат.

Якщо у вас будуть права Адміна через /admin ви зможете переглядати всі бронювання та міняти їх статус, також переглядати користувачів.

## 🚀 Технології
- Python 3.x
- Django 5.x
- PostgreSQL / SQLite
- HTML, CSS (Bootstrap)
- Gunicorn (для деплою)
- Render (хостинг)

## ⚙️ Встановлення
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/yourusername/booking_system.git
   cd booking_system
   
2. Створіть віртуальне середовище:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv/Scripts/Activate   # Windows
   
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   
4. Проведіть міграції:
   ```bash
   python manage.py migrate
   
5. Створіть суперкористувача:
   ```bash
   python manage.py createsuperuser

6. Запустіть сервер:
   ```bash
   python manage.py runserver

## 🌐 Використання

- Перейдіть за адресою: http://127.0.0.1:8000/

- Увійдіть як адмін, щоб додавати кімнати та переглядати бронювання всіх користувачів.

- Користувачі можуть бронювати кімнати безпосередньо на сайті.

## 🌐 Демонстрація
- Проєкт задеплоєний на Render:
- 👉 https://booking-system-v4j4.onrender.com/

## 📬 Контакти
   - Автор: Роман
   - Email: romankits08@gmail.com
