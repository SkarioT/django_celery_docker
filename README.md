An example of the implementation of the service for sending SMS to clients of various operators and time zones. With the ability to send messages, in accordance with the time zone of the client.
Messages are sent via API to a remote SMS Gate.

On Docker-compose:
 - Django + API (django rest framework)
 - selery-beats (for delayed sending)
 - Redis (for delayed dispatch)
 - PostgreSQL (database)


Example deploy to AWS EC2
http://ec2-18-159-113-171.eu-central-1.compute.amazonaws.com:8000/docs/

How to install:

+ Clone project
`$ git clone https://github.com/SkarioT/django_celery_docker.git`

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
