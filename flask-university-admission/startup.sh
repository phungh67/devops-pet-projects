#!/bin/bash

database_name=$1

echo "Start up service..."
echo "Check if the database is up and running..."

if [ "$(docker container inspect -f '{{.State.Running}}' $database_name )" = "running" ];
then
    echo "The database is correctly started..."
else
    echo "Starting the database..."
    docker start $database_name
fi
