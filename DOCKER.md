# Docker Setup Guide

Complete guide for running the Finhub ETL system with Docker.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available for containers

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   ETL Pipeline  │────▶│    MySQL     │     │  RabbitMQ   │
│   (Scheduler)   │     │   Database   │     │   Message   │
└─────────────────┘     └──────────────┘     │   Broker    │
                              ▲               └──────┬──────┘
                              │                      │
                        ┌─────┴──────┐              │
                        │   Worker   │◀─────────────┘
                        │ (Consumer) │
                        └────────────┘
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

**Required variables:**
```env
FINHUB_API_KEY=your_actual_api_key_here
MYSQL_PASSWORD=secure_password_here
```

### 2. Start All Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Verify Setup

```bash
# Check MySQL is ready
docker-compose exec mysql mysql -u finhub_user -p -e "SHOW DATABASES;"

# Check RabbitMQ
curl http://localhost:15672/api/overview
# Default: guest/guest

# Check migrations ran
docker-compose logs etl-migrations

# Check worker is consuming
docker-compose logs worker
```

## 📦 Services

### MySQL Database
- **Port**: 3306
- **User**: finhub_user (configurable)
- **Database**: finhub_etl
- **Data**: Persisted in `mysql_data` volume

### RabbitMQ
- **AMQP Port**: 5672
- **Management UI**: http://localhost:15672
- **Default Login**: guest/guest
- **Data**: Persisted in `rabbitmq_data` volume

### ETL Pipeline
- Runs scheduled jobs
- Fetches data from Finnhub API
- Stores in MySQL
- Can publish tasks to RabbitMQ

### Worker
- Consumes tasks from RabbitMQ
- Processes data fetching and storage
- Auto-scales horizontally

### ETL Migrations
- Runs once on startup
- Applies Alembic migrations
- Auto-exits after completion

### phpMyAdmin (Optional)
- **Port**: 8080
- **URL**: http://localhost:8080
- Enable with: `docker-compose --profile tools up -d`

## 🔧 Common Commands

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart worker

# View logs
docker-compose logs -f worker
docker-compose logs -f etl-pipeline

# Scale workers
docker-compose up -d --scale worker=3
```

### Database Operations

```bash
# Run migrations
docker-compose run --rm etl-migrations

# Access MySQL CLI
docker-compose exec mysql mysql -u finhub_user -p finhub_etl

# Backup database
docker-compose exec mysql mysqldump -u root -p finhub_etl > backup.sql

# Restore database
docker-compose exec -T mysql mysql -u root -p finhub_etl < backup.sql
```

### Worker Operations

```bash
# View worker logs
docker-compose logs -f worker

# Scale workers (horizontal scaling)
docker-compose up -d --scale worker=5

# Restart workers
docker-compose restart worker

# Enter worker container
docker-compose exec worker bash
```

### Debugging

```bash
# Enter a container
docker-compose exec etl-pipeline bash
docker-compose exec worker bash

# Check service health
docker-compose ps

# View resource usage
docker stats

# Clean up everything (WARNING: deletes data)
docker-compose down -v
```

## 🔍 Monitoring

### RabbitMQ Management UI

Access at: http://localhost:15672

- Monitor queue depth
- View message rates
- Check consumer status
- Manage exchanges and queues

### MySQL Monitoring

```bash
# Show running processes
docker-compose exec mysql mysql -u root -p -e "SHOW PROCESSLIST;"

# Check table sizes
docker-compose exec mysql mysql -u root -p finhub_etl -e "
SELECT
  table_name AS 'Table',
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'finhub_etl'
ORDER BY (data_length + index_length) DESC;
"
```

### Container Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f worker

# Last 100 lines
docker-compose logs --tail=100 etl-pipeline

# Since specific time
docker-compose logs --since 2024-01-01T00:00:00
```

## 🛠️ Development Workflow

### Local Development with Docker

```bash
# Start dependencies only
docker-compose up -d mysql rabbitmq

# Run ETL pipeline locally
cd etl-pipeline
poetry install
poetry run python -m finhub_etl.main

# Run worker locally
cd worker
poetry install
poetry run python -m worker.main
```

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker-compose build etl-pipeline
docker-compose up -d etl-pipeline

# Rebuild all
docker-compose build
docker-compose up -d
```

### Running Tests

```bash
# Run tests in container
docker-compose run --rm etl-pipeline pytest

# With coverage
docker-compose run --rm etl-pipeline pytest --cov
```

## 📊 Performance Tuning

### Worker Scaling

```bash
# Automatic scaling based on queue depth
docker-compose up -d --scale worker=5

# Environment variable
WORKER_CONCURRENCY=10 docker-compose up -d
```

### MySQL Optimization

Add to `docker-compose.yaml` under mysql service:

```yaml
command:
  - --max_connections=200
  - --innodb_buffer_pool_size=1G
  - --query_cache_size=32M
```

### RabbitMQ Tuning

```yaml
environment:
  RABBITMQ_VM_MEMORY_HIGH_WATERMARK: 1GB
  RABBITMQ_DISK_FREE_LIMIT: 2GB
```

## 🔒 Security Best Practices

### 1. Change Default Passwords

```bash
# Generate strong passwords
openssl rand -base64 32

# Update .env
MYSQL_ROOT_PASSWORD=<generated_password>
MYSQL_PASSWORD=<generated_password>
RABBITMQ_PASSWORD=<generated_password>
```

### 2. Use Docker Secrets (Production)

```yaml
secrets:
  mysql_password:
    file: ./secrets/mysql_password.txt

services:
  mysql:
    secrets:
      - mysql_password
    environment:
      MYSQL_PASSWORD_FILE: /run/secrets/mysql_password
```

### 3. Network Isolation

```bash
# Only expose necessary ports
# Remove port mappings for internal services
```

### 4. Run as Non-Root

Both Dockerfiles already use non-root users (etluser, worker).

## 🚨 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check port conflicts
netstat -tuln | grep -E '3306|5672|15672'
```

### Worker Not Consuming

```bash
# Check RabbitMQ connection
docker-compose logs worker | grep -i rabbit

# Check queue exists
docker-compose exec rabbitmq rabbitmqctl list_queues
```

### Database Connection Fails

```bash
# Check MySQL is healthy
docker-compose ps mysql

# Test connection
docker-compose exec etl-pipeline python -c "
from finhub_etl.database.core import engine
import asyncio
asyncio.run(engine.connect())
print('Connected!')
"
```

### Out of Memory

```bash
# Check memory usage
docker stats

# Limit container memory
docker-compose.yaml:
  services:
    worker:
      mem_limit: 512m
      mem_reservation: 256m
```

## 🔄 Backup & Restore

### Backup

```bash
# Database backup
docker-compose exec mysql mysqldump \
  -u root -p finhub_etl \
  --single-transaction \
  --routines \
  --triggers > backup_$(date +%Y%m%d).sql

# Backup volumes
docker run --rm \
  -v finhub-mysql-data:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/mysql_backup.tar.gz /data
```

### Restore

```bash
# Restore database
docker-compose exec -T mysql mysql -u root -p finhub_etl < backup.sql

# Restore volume
docker run --rm \
  -v finhub-mysql-data:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/mysql_backup.tar.gz -C /
```

## 📈 Production Deployment

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yaml finhub

# Scale services
docker service scale finhub_worker=5
```

### Using Kubernetes

See `k8s/` directory for Kubernetes manifests (if available).

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify configuration: `.env` file
3. Check service health: `docker-compose ps`
4. Review this guide

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MySQL Docker Hub](https://hub.docker.com/_/mysql)
- [RabbitMQ Docker Hub](https://hub.docker.com/_/rabbitmq)
