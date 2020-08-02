# Django Photos

A simple django application to manage photos

## Features

- Post a photo
- Save photos as draft
- Edit photo captions
- Delete photos
- List photos (all, my photos, my drafts)
- ASC/DESC Sort photos on publishing date
- Filter photos by user
- JWT authentication
- Remove the dimension/size limit, and store the original photo, but serve only proportional
- Resized/cropped photos based on pre-defined dimensions
- Support #tags in captions, and filtering on the same


## Requirement

1. Python 3.8.5 with virtualenv, can be installed using [pyenv](https://github.com/pyenv/pyenv)
2. Docker 18.09.5
3. Docker compose 1.25.4

### Development

```
# Check python version, required 3.8.5
python --version
Python 3.8.5

# Create virtualenv and activate
virtualenv -p `which python` .venv
source .venv/bin/activate

# Install dependencies
pip install -r src/requirements.txt

# Import environment variables
cd src
export $(cat .env.local | xargs)

# Uncomment the `web` service on the `docker-compose.yml`
# So the compose only running the `db` service
docker-compose up --build

# Test django installation
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Development with Docker

```
# Start (with daemon mode add `-d`) or build (add `--build`) the docker images
docker-compose up --build
docker exec -it django-photos_web_1 python manage.py migrate
docker exec -it django-photos_web_1 python manage.py createsuperuser
```

The docker environment is supported for auto reload.

### Tests

On local, use the commands below

```
cd src && coverage run --source='.' manage.py test photos/tests && coverage html
```

On docker running, use the commands below

```
# Execute test inside docker
docker exec -it django-photos_web_1 python manage.py test photos
```
