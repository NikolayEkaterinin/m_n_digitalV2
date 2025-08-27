
# Используем официальный образ Nginx
FROM nginx:1.22.1

# Копируем наш файл конфигурации в нужное место внутри контейнера
COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем права на директорию (опционально, если потребуются изменения)
RUN chmod -R 755 /etc/nginx/conf.d /etc/nginx/nginx.conf

# Папка логов (опционально)
VOLUME ["/var/log/nginx"]

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]