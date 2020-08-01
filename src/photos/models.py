from django.db import models
from django.contrib.auth.models import User

PHOTO_STATUS = [
    ('d', 'Draft'),
    ('p', 'Published'),
]

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    captions = models.TextField()
    file = models.ImageField(blank=False, null=False)
    status = models.CharField(max_length=1, choices=PHOTO_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name