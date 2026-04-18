# Dockerfile
FROM nginx:alpine

# Копируем наш HTML файл в nginx
COPY index.html /usr/share/nginx/html/index.html

# Копируем конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
