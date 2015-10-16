#!/usr/bin/env bash
docker stop api01
docker rm `docker ps --no-trunc -aq`
docker run --name api01 -p 5001:80 --link mysql:mysql -d st2forget/flask-restful