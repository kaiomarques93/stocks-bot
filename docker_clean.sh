#!/bin/bash

var="$(sudo docker ps -aq)"
var1="$(sudo docker image ls -aq)"
var2="$(sudo docker volume ls -q)"

if [ -z "$var" ]
then
      echo "There are no containers"
else
	sudo docker container stop $(sudo docker container ls -aq) 
	sudo docker rm $(sudo docker ps -aq)
fi

if [ -z "$var1" ]
then
	echo "There are no images"
else
	sudo docker rmi  $(sudo docker image ls -aq)
fi

if [ -z "$var2" ]
then
	echo "There no volumes"
else
	sudo docker volume rm $(sudo docker volume ls -q)
fi
