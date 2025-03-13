Создание файла переменных окружения

1. Перейти в директорию `cd 1`
2. Создать файл `.env` и заполнить его содержимое по примеру `.env.example` 

Для запуска postgres

1. Перейти в директорию `cd 1/db`
2. Создать файл `.env` и заполнить его содержимое по примеру `.env.example` 
3. Запустить команду `docker build -t my_postgres .` для сборки образа
4. Запустить контейнер `docker run -d --name my_postgres_container --env-file .env -p 5432:5432 my_postgres`

Кроме того, пришлось добавить `pydantic-settings` в `requirements.txt` для создания файла конфигурации

