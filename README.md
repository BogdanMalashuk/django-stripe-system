# Django Stripe System

Сервис на Django с оплатой товаров через Stripe

---

## 🚀 Функциональность

- Оплата товара/заказа через Stripe (USD/Euro)
- Создание заказа с несколькими товарами
- Добавление скидок и налогов к заказу
- CRUD моделей через админ-панель
- Получение ID stripe-сессии через запрос

---

## 🛠 Используемые технологии

Django 5.2.4

Stripe

Docker 

PostgreSQL

Render.com (для деплоя)

Stripe CLI (для вебхуков и отслеживания оплаты заказа)

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```
git clone https://github.com/BogdanMalashuk/django-stripe-system.git
cd django-stripe-system
```

### 2. Установить зависимости

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Создать .env файл

```
DEBUG=True/False
SECRET_KEY=some_key
ALLOWED_HOSTS=some_hosts

POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_HOST=db_host
POSTGRES_PORT=db_port

STRIPE_WEBHOOK_SECRET=stripe_wh_secret
STRIPE_SECRET_KEY=some_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=some_stripe_publish_key
DATABASE_URL=postgres://username:password:port/dbname

```

### 4. Применить миграции

```
python manage.py makemigrations
python manage.py migrate
```

### 5. Создать суперюзера и запустить сервер

```
python manage.py createsuperuser
python manage.py runserver
```

### 6. Запустить отслеживание вебхуков успешной оплаты заказа
```
stripe listen --events payment_intent.succeeded --forward-to localhost:8000/webhook/
```
---

