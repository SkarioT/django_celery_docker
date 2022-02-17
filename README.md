####Inline code


+ Clone project
`$ git clone https://gitlab.com/SkarioT/django_postgresql_celery_redis_docker.git`

+ Change directory:
+ `$cd django_postgresql_celery_redis_docker/`


+ Build project:
`$ sudo docker-compose up --build`
+ Open new window & exec command:
    + Change directory:
    + `$cd django_postgresql_celery_redis_docker/`
	+ `sudo docker-compose exec webapp bash`
	+ Change directory
    + `$ cd src\`
	+ `$ python manage.py makemigrations`
	+ `$ python manage.py migrate`
	+ `$ python manage.py createsuperuser`
	+ `$ exit`
+ Return first window and stop project (ctrl+c).
+ Exec command :
`$ sudo docker-compose down`
+ Run demo-prodactions project:
`$ sudo  docker-compose up -d`
