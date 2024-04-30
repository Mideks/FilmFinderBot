# Используйте официальный образ Python 3.9
FROM python:3.9

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте текущий каталог в рабочую директорию в контейнере
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запустите приложение
CMD ["python", "main.py"]
