FROM python:3.9-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . /app/

# Переменные окружения
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Запуск Flask
CMD ["flask", "run"]
