FROM python:3.13-slim

# Настройка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей и установка
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование исходного кода проекта
COPY . /app/

# Запуск миграций и запуск сервера Daphne (для поддержки WebSockets)
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8054 chat_project.asgi:application"]
