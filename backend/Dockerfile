# Используем официальный Python-образ
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y build-essential gcc

# Установка рабочей директории
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Переменные окружения (можно переопределять через docker-compose)
ENV MONGO_URI=mongodb://mongo:27017/
ENV JWT_SECRET_KEY=supersecretkey
ENV JWT_ALGORITHM=HS256

# Открываем порт
EXPOSE 8000

# Запуск FastAPI через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
