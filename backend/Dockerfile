# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем локали
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем редакторы (опционально)
RUN apt-get update && \
    apt-get install -y --no-install-recommends nano mc && \
    rm -rf /var/lib/apt/lists/*

# Копируем проект
COPY . .

# Команда запуска через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
