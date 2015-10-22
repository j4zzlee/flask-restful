#!/usr/bin/env bash
docker stop `docker ps`
docker rm `docker ps --no-trunc -aq`
docker-compose up