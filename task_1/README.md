# Облік котів у MongoDB

Консольний Python-скрипт для CRUD-операцій з колекцією `cats` у базі `cats_db`.
Початкове наповнення містить шістьох котів і створюється з `init-mongo.js`.

## Потрібно для запуску

- Docker Desktop із запущеним Docker Engine.
- Python 3.9 або новіший.

## Запуск MongoDB

У терміналі перейдіть до каталогу `task_1` і запустіть MongoDB:

```bash
cd task_1
docker compose up -d --wait
```

Docker завантажить образ `mongo:7`, відкриє MongoDB на `localhost:27017` і
створить базу `cats_db`, колекцію `cats` та шість початкових документів.
Сховище зберігається у Docker volume `mongodb_data`.

## Запуск Python-скрипта

З каталогу `task_1` встановіть залежність і запустіть меню:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Скрипт підключається до `mongodb://localhost:27017/`. Для іншої адреси MongoDB
можна задати змінну середовища `MONGODB_URI`.

У меню можна додавати котів, переглядати всіх або шукати за ім'ям, оновлювати
вік, додавати характеристику, видаляти кота або очищати колекцію.

## Перегляд даних у MongoDB

У MongoDB Compass використайте адресу `mongodb://localhost:27017/`, після чого
відкрийте `cats_db` → `cats`.

Або перегляньте документи через `mongosh`:

```bash
docker exec -it cats-mongodb mongosh cats_db --eval 'db.cats.find().pretty()'
```

## Повторне застосування початкових даних

MongoDB виконує файли з `/docker-entrypoint-initdb.d` лише під час першого
запуску на порожньому сховищі. Якщо контейнер уже ініціалізовано, виконайте
скрипт вручну з каталогу `task_1`:

```bash
docker exec -i cats-mongodb mongosh --quiet < init-mongo.js
```

Скрипт додає відсутніх котів і не створює повторні записи з такими самими
іменами.

## Зупинка MongoDB

```bash
docker compose down
```

Команда зупиняє контейнер, але зберігає дані. `docker compose down -v` також
видаляє volume з даними MongoDB.
