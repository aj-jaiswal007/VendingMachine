# restart command to run docker-compose down build and up
restart:
	docker-compose down
	docker-compose build
	docker-compose up

# Runs locally
run:
	uvicorn vendingmachine.main:app --proxy-headers --host localhost --port 8080
