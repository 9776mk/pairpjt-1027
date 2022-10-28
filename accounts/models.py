from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(200, 300)],
        format='JPEG',
        options={'quality' : 50},
    )
    status_message = models.CharField(max_length=100)