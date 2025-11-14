test:
	echo "Finhub ETL pipeline"

start:
	poetry run python src/main.py

# Test handlers - fetch stock symbols from Finnhub API
test-handlers:
	poetry run python tests/handlers.py

# Test store_db - save symbols from JSON to database
test-store-db:
	poetry run python tests/store_db.py

# Run both tests sequentially
test-all:
	@echo "Running handler tests..."
	poetry run python tests/handlers.py
	@echo "\nRunning store_db tests..."
	poetry run python tests/store_db.py
	@echo "\nAll tests completed!"
