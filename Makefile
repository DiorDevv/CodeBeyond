
make run:
	python manage.py runserver

make mig:
	python manage.py makemigrations
	python manage.py migrate




make superuser:
	python manage.py createsuperuser