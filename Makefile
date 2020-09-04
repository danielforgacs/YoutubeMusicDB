build: down
	@docker-compose build --no-cache --force-rm --pull

build-cached: down
	@docker-compose build

initdb:
	@docker-compose up -d ymdb_postgres
	@sleep 5
	@- docker-compose exec ymdb_postgres psql -U postgres -c "drop database ymdb;"
	@- docker-compose exec ymdb_postgres psql -U postgres -c "create database ymdb;"
	@docker-compose exec ymdb_postgres psql -U postgres -d ymdb -f /home/sql/schema.sql

initdb-test:
	@docker-compose up -d ymdb_postgres
	@sleep 5
	@- docker-compose exec ymdb_postgres psql -U postgres -c "drop database ymdb_test;"
	@- docker-compose exec ymdb_postgres psql -U postgres -c "create database ymdb_test;"
	@docker-compose exec ymdb_postgres psql -U postgres -d ymdb_test -f /home/sql/schema.sql

up:
	@docker-compose up

upd:
	@docker-compose up -d

down:
	@docker-compose down --remove-orphans --volumes

test: down build
	@docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
	@sleep 5
	@- export PYTHONPATH=$$PWD && \
		export DB_HOST=127.0.0.1 && \
		export PGDATABASE=ymdb_test && \
		export DBACCESS_RPC_HOST=0.0.0.0 && \
		pytest | tee tests/testlog_$$(date +%Y-%m-%d_%H-%M-%S).log
	@make down

test-nobuild:
	@docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
	@sleep 5
	@- export PYTHONPATH=$$PWD && \
		export DB_HOST=127.0.0.1 && \
		export PGDATABASE=ymdb_test && \
		export DBACCESS_RPC_HOST=0.0.0.0 && \
		pytest | tee tests/testlog_$$(date +%Y-%m-%d_%H-%M-%S).log
	@make down

db:
	@docker-compose up -d ymdb_postgres

pgdump: db
	@docker-compose exec ymdb_postgres pg_dump -U postgres -d ymdb --disable-dollar-quoting --inserts -a


sqlfile:
	@docker-compose exec ymdb_postgres psql -U postgres -d $$PGDATABASE -f /home/sql/$(file)
