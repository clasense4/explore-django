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

Photo

All endpoint need to be authenticated using jwt

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


### Development
```
docker run --rm -it \
  -v $PWD/src:/root/src \
  -p 8000:8000 \
  django-photos bash
```