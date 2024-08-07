#!/bin/sh

minio server --console-address ":9090" /data &
MINIO_PID=$!

echo "Ожидание запуска сервера MinIO..."
sleep 20

echo "Настройка алиаса MinIO..."
mc alias set myminio http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
if [ $? -ne 0 ]; then
    echo "Не удалось установить алиас"
    exit 1
fi

echo "Создание бакета..."
mc mb myminio/"$MINIO_STORAGE_MEDIA_BUCKET_NAME"
if [ $? -ne 0 ]; then
    echo "Не удалось создать бакет"
    exit 1
fi

echo "Установка политики доступа для бакета на публичную..."
mc anonymous set public myminio/"$MINIO_STORAGE_MEDIA_BUCKET_NAME"
if [ $? -ne 0 ]; then
    echo "Не удалось установить политику доступа для бакета"
    exit 1
fi

echo "Настройка завершена."

wait $MINIO_PID
