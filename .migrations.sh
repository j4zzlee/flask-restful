#!/usr/bin/env bash

echo 'Running migrations:' $1

if [ $2 == 'local' ]
then
    echo 'Running local migrations'
    cd api/app
    python migrations.py db $1
else
    echo 'Running docker migrations'
    docker-compose run web python /var/www/app/migrations.py db $1
fi






