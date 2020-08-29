build: down
	@docker-compose build --no-cache --force-rm --pull

initdb:
	@docker-compose up -d ymdb_db
	@sleep 5
	@- docker-compose exec ymdb_db psql -U postgres -c "drop database $$PGDATABASE;"
	@- docker-compose exec ymdb_db psql -U postgres -c "create database $$PGDATABASE;"
	@docker-compose exec ymdb_db psql -U postgres -d $$PGDATABASE -f /home/sql/schema.sql

initdb_test:
	@docker-compose up -d ymdb_db
	@sleep 5
	@- docker-compose exec ymdb_db psql -U postgres -c "drop database ymdb_test;"
	@- docker-compose exec ymdb_db psql -U postgres -c "create database ymdb_test;"
	@docker-compose exec ymdb_db psql -U postgres -d ymdb_test -f /home/sql/schema.sql

up:
	@docker-compose up

upd:
	@docker-compose up -d

down:
	@docker-compose down --remove-orphans --volumes

test: build initdb_test upd
	@sleep 5
	@- export PYTHONPATH=$$PWD && \
		export DB_HOST=127.0.0.1 && \
		export PGDATABASE=ymdb_test && \
		pytest
	@make down

db:
	@docker-compose up -d ymdb_db

pgdump: db
	@docker-compose exec ymdb_db pg_dump -U postgres -d ymdb --disable-dollar-quoting --inserts -a
