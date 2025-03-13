Создание файла переменных окружения

1. Перейти в директорию `cd 3`
2. Создать файл `.env` и заполнить его содержимое по примеру `.env.example` 

Для запуска clickhouse

1. Перейти в директорию `cd 3/clickhouse`
2. Создать файл `tables.sql`. Скопировать содержимое `tables.example.sql`. Добавить имя пользователя и пароль.  
3. Запустить команду `docker build -t my-clickhouse .` для сборки образа
4. Запустить контейнер ` docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 my-clickhouse`

Кроме того, пришлось добавить `pydantic` и `pydantic-settings` в `requirements.txt` для создания файла конфигурации

