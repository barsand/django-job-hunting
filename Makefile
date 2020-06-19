all: clean install run

install:
	python3.7 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	python3.7 src/manage.py migrate
	python3.7 src/manage.py makemigrations jobs
	python3.7 src/manage.py sqlmigrate jobs 0001
	python3.7 src/manage.py migrate
	python3.7 src/manage.py createsuperuser
	python3.7 src/manage.py runserver

run:
	. venv/bin/activate
	python3.7 src/manage.py runserver

clean:
	rm -Rf src/jobs/migrations src/db.sqlite3

