# PalleteShop 🎨

Интернет-магазин строительных материалов с системой онлайн-чатов и корзиной покупок.

## 🚀 Возможности

- **Каталог продуктов** с фильтрацией и поиском
- **Детальные страницы товаров** с каруселью изображений
- **Корзина покупок** с управлением количеством
- **Онлайн-чаты** с клиентами для менеджеров
- **Email-уведомления** о новых сообщениях
- **Админ-панель** для управления товарами и заказами
- **Адаптивный дизайн** для всех устройств

## 📋 Технологии

- **Backend**: Django 5.2.8, PostgreSQL
- **Frontend**: Bootstrap 5.3.2, HTMX
- **Deployment**: Docker, Docker Compose, Nginx, Gunicorn
- **Email**: SMTP (Mail.ru)

## 🔧 Быстрый старт (разработка)

### Предварительные требования

- Python 3.11+
- PostgreSQL 15+
- Git

### Установка

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/khasanyanovk/PalleteShop.git
   cd PalleteShop
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   # Отредактируйте .env с вашими настройками
   ```

5. **Применение миграций**
   ```bash
   python manage.py migrate
   ```

6. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

7. **Загрузка тестовых данных (опционально)**
   ```bash
   python manage.py populate_products
   ```

8. **Запуск сервера разработки**
   ```bash
   python manage.py runserver
   ```

Сайт будет доступен по адресу: http://127.0.0.1:8000/

## 🐳 Деплой с Docker

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+

### Быстрый запуск

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/khasanyanovk/PalleteShop.git
   cd PalleteShop
   ```

2. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   # Отредактируйте .env для продакшна
   ```

3. **Сборка и запуск**
   ```bash
   docker compose build
   docker compose up -d
   ```

Сайт будет доступен по адресу: https://localhost/

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 👤 Автор

**Khasanov Kirill**

- GitHub: [@khasanyanovk](https://github.com/khasanyanovk)

## 🙏 Благодарности

- Django Documentation
- Bootstrap Team
- Docker Community

---

**Сделано с ❤️ для упрощения онлайн-торговли**
