Для запуска БД

1. Перейти в директорию cd 1/db
2. Запустить команду `docker build -t my_postgres .` для сборки образа
3. Запустить контейнер `docker run -d --name my_postgres_container --env-file .env -p 5432:5432 my_postgres`

Кроме того, пришлось установить pydantic-settings для создания файла конфигурации

