# TeamFinder

Проект TeamFinder — это социальная платформа для поиска команд и участников для проектов. Пользователи могут создавать проекты, добавлять участников, отмечать проекты как избранные и просматривать список других участников.

## Технологии

- Python 3
- Django
- PostgreSQL
- Docker / Docker Compose
- Django templates

## Быстрый старт

### 1. Скопируйте пример `.env`

В корне проекта есть файл `.env_example`. Скопируйте его в `.env` и заполните значения:

```bash
copy .env_example .env
```

### 2. Пример содержимого `.env`

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=db
POSTGRES_PORT=5432

TASK_VERSION=1
```

### 3. Постоянные переменные

- `DJANGO_SECRET_KEY` — секретный ключ Django
- `DJANGO_DEBUG` — режим разработки (`True`/`False`)
- `POSTGRES_DB` — имя базы данных PostgreSQL
- `POSTGRES_USER` — пользователь PostgreSQL
- `POSTGRES_PASSWORD` — пароль PostgreSQL
- `POSTGRES_HOST` — хост PostgreSQL (`db` при запуске через Docker Compose)
- `POSTGRES_PORT` — порт PostgreSQL
- `TASK_VERSION` — версия шаблонов, которую использует проект

## Локальный запуск через Docker Compose

### 1. Соберите и запустите контейнеры

```bash
docker compose up --build -d
```

### 2. Остановить контейнеры

```bash
docker compose down
```

### 3. Адрес приложения

Откройте в браузере:

```text
http://localhost:8000
```

### 4. Админка Django

```text
http://localhost:8000/admin/
```

### 5. Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

## Запуск миграций

Если контейнеры уже запущены, миграции выполняются автоматически при старте веб-сервиса. Для ручного запуска используйте:

```bash
docker compose exec web python manage.py migrate
```

Если вы запускаете проект без Docker, активируйте виртуальное окружение и выполните:

```bash
python manage.py migrate
```

## Тестовые данные

В проекте нет специального скрипта для заполнения тестовыми данными. Рекомендуется создать администратора и добавить тестовые проекты и пользователей через админку или интерфейс:

```bash
docker compose exec web python manage.py createsuperuser
```

## Запуск без Docker

Если вы хотите запустить проект локально без контейнеров, выполните:

1. Создайте виртуальное окружение и активируйте его
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте `.env` и заполните параметры
4. Запустите миграции:
   ```bash
   python manage.py migrate
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## Полезные заметки

- Для локального Docker-хоста в `.env` хост базы данных должен быть `db`.
- Если порт `5432` занят на машине, можно изменить проброс портов в `docker-compose.yml` и соответствующую переменную `POSTGRES_PORT`.
- В `ALLOWED_HOSTS` разрешены хосты из переменной окружения.

## Структура проекта

- `team_finder/` — настройки Django
- `projects/` — приложения для управления проектами
- `users/` — приложение для работы с пользователями и авторизацией
- `templates_var1/` — шаблоны Django
- `static/` — статические файлы
- `media/` — загруженные медиa-файлы
- `docker-compose.yml` — конфигурация Docker Compose
- `.env_example` — пример переменных окружения
