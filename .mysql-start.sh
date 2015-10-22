#!/usr/bin/env bash
docker stop mysql_dev
docker rm `docker ps --no-trunc -aq`
docker run -p 3307:3306 -e MYSQL_ROOT_PASSWORD=P@ssword123 --name mysql_dev -d mysql:latest
