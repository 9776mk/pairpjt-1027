from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=30)
    movie_name = models.CharField(max_length=30)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    image = models.ImageField(upload_to='images/', blank=True)

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Review, on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)