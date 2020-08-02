#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y git zip curl wget apt-transport-https ca-certificates software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update -y
apt-cache policy docker-ce
sudo apt install docker-ce -y

sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker --version
docker-compose --version

cd /home/ubuntu
git clone https://github.com/clasense4/explore-django.git
cd explore-django
sudo docker-compose up -d --build
sudo docker exec -it explore-django_web_1 python manage.py migrate