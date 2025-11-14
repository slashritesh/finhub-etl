# Makefile for Finhub ETL Docker Operations
# Quick commands for common Docker tasks

.PHONY: help build up down restart logs clean migrate worker-scale db-backup db-restore

# Default target
help:
	@echo "Finhub ETL Docker Commands"
	@echo "=========================="
	@echo "  make build          - Build all Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs (all services)"
	@echo "  make logs-worker    - View worker logs"
	@echo "  make logs-etl       - View ETL pipeline logs"
	@echo "  make clean          - Remove all containers and volumes (WARNING: deletes data)"
	@echo "  make migrate        - Run database migrations"
	@echo "  make worker-scale N=3 - Scale workers to N instances"
	@echo "  make db-shell       - Access MySQL shell"
	@echo "  make db-backup      - Backup database to backup.sql"
	@echo "  make db-restore     - Restore database from backup.sql"
	@echo "  make rabbitmq-ui    - Open RabbitMQ management UI"
	@echo "  make phpmyadmin     - Start phpMyAdmin"
	@echo "  make status         - Show service status"
	@echo "  make stats          - Show resource usage"

# Build all images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d
	@echo "Services started! Check status with: make status"

# Stop all services
down:
	docker-compose down

# Restart all services
restart:
	docker-compose restart

# View all logs
logs:
	docker-compose logs -f

# View worker logs
logs-worker:
	docker-compose logs -f worker

# View ETL pipeline logs
logs-etl:
	docker-compose logs -f etl-pipeline

# Clean everything (WARNING: deletes data)
clean:
	@echo "WARNING: This will delete all containers, volumes, and data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "Cleaned!"; \
	fi

# Run database migrations
migrate:
	docker-compose run --rm etl-migrations

# Scale workers (usage: make worker-scale N=5)
worker-scale:
	@docker-compose up -d --scale worker=$(N)
	@echo "Scaled workers to $(N) instances"

# Access MySQL shell
db-shell:
	docker-compose exec mysql mysql -u finhub_user -p finhub_etl

# Backup database
db-backup:
	@echo "Backing up database..."
	@docker-compose exec mysql mysqldump -u root -p finhub_etl > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup complete: backup_$$(date +%Y%m%d_%H%M%S).sql"

# Restore database from backup.sql
db-restore:
	@echo "Restoring database from backup.sql..."
	@docker-compose exec -T mysql mysql -u root -p finhub_etl < backup.sql
	@echo "Restore complete!"

# Open RabbitMQ management UI
rabbitmq-ui:
	@echo "Opening RabbitMQ Management UI..."
	@xdg-open http://localhost:15672 2>/dev/null || open http://localhost:15672 2>/dev/null || start http://localhost:15672

# Start phpMyAdmin
phpmyadmin:
	docker-compose --profile tools up -d phpmyadmin
	@echo "phpMyAdmin started at http://localhost:8080"

# Show service status
status:
	docker-compose ps

# Show resource usage
stats:
	docker stats --no-stream

# Development commands
dev-etl:
	@echo "Starting dependencies only (MySQL + RabbitMQ)..."
	docker-compose up -d mysql rabbitmq
	@echo "Run ETL locally: cd etl-pipeline && poetry run python -m finhub_etl.main"

dev-worker:
	@echo "Starting dependencies only (MySQL + RabbitMQ)..."
	docker-compose up -d mysql rabbitmq
	@echo "Run worker locally: cd worker && poetry run python -m worker.main"

# Quick rebuild
rebuild-etl:
	docker-compose build etl-pipeline
	docker-compose up -d etl-pipeline

rebuild-worker:
	docker-compose build worker
	docker-compose up -d worker
