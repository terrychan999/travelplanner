.PHONY: run clean init

default: run

run:
	rm -rf backend/__pycache__
	cd backend && python app.py

clean:
	rm -rf backend/__pycache__
	rm -rf backend/instance
	rm -rf backend/*.db

init:
	cd backend && python -c "from app import db; db.create_all()"