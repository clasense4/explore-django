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
export ec2_public_hostname=$(curl http://169.254.169.254/latest/meta-data/public-hostname)
echo "DJANGO_ALLOWED_HOSTS=$ec2_public_hostname" | sudo tee -a src/.env.prod >/dev/null
sudo cat src/.env.prod
sudo docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
sudo docker exec -it explore-django_web_1 python manage.py migrate