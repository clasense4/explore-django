from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

PHOTO_STATUS = [
    ('d', 'Draft'),
    ('p', 'Published'),
]

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    captions = models.TextField()
    file = models.ImageField(blank=False, null=False)
    image_small = ImageSpecField(
                                    source='file',
                                    processors=[ResizeToFill(640, 480)],
                                    format='JPEG',
                                    options={'quality': 60}
                                )
    image_medium = ImageSpecField(
                                    source='file',
                                    processors=[ResizeToFill(1920, 1280)],
                                    format='JPEG',
                                    options={'quality': 80}
                                )
    image_large = ImageSpecField(
                                    source='file',
                                    processors=[ResizeToFill(2400, 1600)],
                                    format='JPEG',
                                    options={'quality': 90}
                                )
    status = models.CharField(max_length=1, choices=PHOTO_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name