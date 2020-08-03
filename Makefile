build: down
	@docker-compose build --no-cache --force-rm --pull

initdb:
	@docker-compose up -d db
	@docker-compose exec db psql -U postgres -c "drop database ymdb;"
	@docker-compose exec db psql -U postgres -f /home/sql/schema.sql

up: down
	@docker-compose up

down:
	@docker-compose down --remove-orphans --volumes
