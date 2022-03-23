#!/usr/bin/env bash

rm .env
echo 'SECRET_KEY=$SECRET_KEY' >> .env
echo 'POSTGRES_USER=$POSTGRES_USER' >> .env
echo 'POSTGRES_PASSWORD=$POSTGRES_PASSWORD' >> .env
echo 'POSTGRES_HOST=$POSTGRES_HOST' >> .env
echo 'POSTGRES_PORT=$POSTGRES_PORT' >> .env
echo 'POSTGRES_DB=$POSTGRES_DB' >> .env
sudo docker pull vladoplavsic/projects:hammer-systems-test
sudo docker kill hammer || true
sudo docker rm hammer || true
docker create --name hammer  -t vladoplavsic/projects:hammer-systems-test
docker cp .env hammer:/backend/.env
docker commit hammer -t vladoplavsic/projects:hammer-systems-test
sudo docker run -d -p 1337:1337 --name hammer -t vladoplavsic/projects:hammer-systems-test /bin/bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:1337"