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
- Implement batch upload, edit, delete, publish API for photos
- Support #tags in captions, and filtering on the same


## Requirement

1. Python 3.8.5 with virtualenv, can be installed using [pyenv](https://github.com/pyenv/pyenv)
2. Docker 18.09.5
3. Docker compose 1.25.4

### Development

This step is required for enabling code completion on vscode. Can skip if not needed.

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
export $(cat .env.dev | xargs)

# Test django installation
python manage.py runserver
```

Now the local is fine, let's prepare for a dockerize environment.

```
# Start (with daemon mode add `-d`) or build (add `--build`) the docker images
docker-compose up
```

The docker environment is supported for auto reload.

### Tests

On local, use the commands below

```
cd src && python manage.py test photos
```

On docker running, use the commands below

```
# Check docker name
$(docker ps | grep django | awk '{print $12}')
# Execute test inside docker
docker exec -it $(docker ps | grep django | awk '{print $12}') python manage.py test photos
```

## API

### Photo

> All endpoint need to be authenticated using jwt

```
POST /auth
return access_token & refresh_token

GET /photos
    /photos/{id}
    /photos/me
    /photos/drafts
    /photos/draft/{id}

POST /photos -> able to publish directly or save as draft
return id

POST /photos/draft
return id

DELETE /photos/{id}
return id
```