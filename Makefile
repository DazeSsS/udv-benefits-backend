db:
	docker compose up -d db

migrate:
	alembic upgrade head

rebuild: build down up

build:
	docker compose build

build_nocache:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

start:
	docker compose start

stop:
	docker compose stop

restart:
	docker compose restart

prune:
	docker system prune