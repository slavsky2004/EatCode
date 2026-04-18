#!/bin/bash

echo "🐳 Собираем Docker образ..."
docker build -t kalori-app .

echo "🚀 Запускаем контейнер..."
docker run -d \
  --name kalori-app \
  --restart unless-stopped \
  -p 8080:80 \
  kalori-app

echo "✅ Приложение запущено на http://localhost:8080"
echo "Остановить: docker stop kalori-app && docker rm kalori-app"
