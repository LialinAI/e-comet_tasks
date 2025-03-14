FROM clickhouse/clickhouse-server:latest

COPY table.sql /docker-entrypoint-initdb.d/

WORKDIR /docker-entrypoint-initdb.d/

CMD ["/entrypoint.sh"]
