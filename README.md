docker-compose build

docker-compose up

docker-compose exec web python manage.py migrate --noinput 

docker-compose exec web python manage.py createsuperuser