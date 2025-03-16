 #!/bin/bash

mkdir -p /tmp/sql

psql -v ON_ERROR_STOP=1 -U "postgres" -f /tmp/sql/create_db.sql

rm -rf /tmp/sql
