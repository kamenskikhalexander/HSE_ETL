FROM postgres:17

RUN apt-get update

COPY create_db.sql /sql/
COPY create_db.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/create_db.sh
