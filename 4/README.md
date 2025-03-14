Для запуска clickhouse

1. Перейти в директорию `cd 4/clickhouse`
2. Создать файл `table.sql`. Скопировать содержимое `table.example.sql`. Добавить имя пользователя и пароль.  
3. Запустить команду `docker build -t my-clickhouse .` для сборки образа
4. Запустить контейнер ` docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 my-clickhouse`

Подключался к clickhouse через DBeaver