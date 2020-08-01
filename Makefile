initdb:
	@docker-compose up -d db
	@docker-compose exec db psql -U postgres -f /home/sql/schema.sql

up:
	@docker-compose up -d

down:
	@docker-compose down --remove-orphans --volumes
