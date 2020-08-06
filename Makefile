build: down
	@docker-compose build --no-cache --force-rm --pull

initdb:
	@docker-compose up -d ymdb_db
	@sleep 5
	@- docker-compose exec ymdb_db psql -U postgres -c "drop database ymdb;"
	@docker-compose exec ymdb_db psql -U postgres -f /home/sql/schema.sql

up:
	@docker-compose up

upd:
	@docker-compose up -d

down:
	@docker-compose down --remove-orphans --volumes

test: down
	@docker-compose up -d
	@sleep 5
	@- pytest
	@make down
