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
4. [jq](https://stedolan.github.io/jq/)

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

On local, use the commands below to execute the test and coverage report

```
cd src
coverage run --source='.' manage.py test photos/tests && coverage report && coverage html
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 6.678s

OK
Destroying test database for alias 'default'...
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
djangophotos/__init__.py                           0      0   100%
djangophotos/asgi.py                               4      4     0%
djangophotos/settings.py                          27      0   100%
djangophotos/urls.py                              11      0   100%
djangophotos/wsgi.py                               4      4     0%
manage.py                                         12      2    83%
photos/__init__.py                                 0      0   100%
photos/admin.py                                    3      0   100%
photos/apps.py                                     3      3     0%
photos/migrations/0001_initial.py                  7      0   100%
photos/migrations/0002_auto_20200802_1017.py       4      0   100%
photos/migrations/__init__.py                      0      0   100%
photos/models.py                                  19      1    95%
photos/permissions.py                              6      1    83%
photos/serializers.py                             23      0   100%
photos/tests/test_photo.py                       167      0   100%
photos/tests/test_user.py                         32      0   100%
photos/urls.py                                     6      0   100%
photos/views.py                                   85      2    98%
------------------------------------------------------------------
TOTAL                                            413     17    96%

```

On docker running, use the commands below

```
# Execute test inside docker
docker exec -it django-photos_web_1 python manage.py test photos
```

## API

We will use a simple curl command to interact with the API.

### Register new user

This API is designed to not have anonymous user access, so a new user is required.

```
curl -X POST \
    http://localhost:8000/registration/ \
    -H "Content-Type: application/json" \
    -d '{"username":"fajri2","password1":"passwordfajri2","password2":"passwordfajri2"}' \
    | jq -r "."
```

### Get JWT Token

This token lifetime is 3000 seconds.

```
export USER_TOKEN=$(curl -X POST -H "Content-Type: application/json" -d '{"username":"fajri2","password":"passwordfajri2"}' http://localhost:8000/api-token-auth/ | jq -r ".token")
echo $USER_TOKEN
```

### Post a photo

A photo is categorized into 2 statuses. Published and draft. Published photo can be seen by any authenticated user. Draft photo can be seen only by the owner. Published photo also will appear on `api/v1/photos/hashtag`. Also `published_at` is null when the status is d / draft. The image will be uploaded to `media` directory.

```
# Locate the image or use the sample in tests directory
cd src/photos/tests
curl -X POST \
  http://localhost:8000/api/v1/photos \
  -H "Authorization: JWT ${USER_TOKEN}" \
  -H "content-type: multipart/form-data" \
  -F name="nemo aquarium" \
  -F file=@nemo.jpg \
  -F "captions=Nemo Aquarium #ikan #nemo #aquarium" \
  -F status=p | jq -r "."

curl -X POST \
  http://localhost:8000/api/v1/photos \
  -H "Authorization: JWT ${USER_TOKEN}" \
  -H "content-type: multipart/form-data" \
  -F name="Sapi perah" \
  -F file=@sapi.jpg \
  -F "captions=Sapi kurban itu harus yang terbaik #sapi #kurban" \
  -F status=d | jq -r "."
```

### Get all photos, filter by status and sort by published_at

Now we have 2 photos, we can check that using this command. When this operation executed, the image will be generated using `imagekit` library into several processed images. Small, medium and large. The image later will be created into `CACHE` directory. By default, the order is ascending, add `sort=desc` to sort in descending order.

```
curl -X GET \
  http://localhost:8000/api/v1/photos \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

curl -X GET \
  http://localhost:8000/api/v1/photos?status=p \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

curl -X GET \
  http://localhost:8000/api/v1/photos?status=d \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

curl -X GET \
  http://localhost:8000/api/v1/photos?sort=desc \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

curl -X GET \
  http://localhost:8000/api/v1/photos?status=p&sort=desc \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

curl -X GET \
  http://localhost:8000/api/v1/photos?status=d&sort=desc \
  -H "Authorization: JWT ${USER_TOKEN}" | jq -r "."

```