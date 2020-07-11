#!/bin/bash
docker run -d -p 6379:6379 redis:latest
docker run -d -p 5433:5432 -v /home/rj/postgres:/var/lib/postgresql/data -e POSTGRES_PASSWORD=1234 -it postgres:13