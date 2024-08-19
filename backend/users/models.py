from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from io import BytesIO
from PIL import Image
from django.core.files import File
from uuid import uuid4
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)

    objects = UserManager()

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to="profile_pictures/", blank=True)
    thumbnail = models.ImageField(upload_to='profile_pictures/thumbnail/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_thumbnail(self):
        if not self.thumbnail and self.profile_picture:
            self.thumbnail = self.make_thumbnail(self.profile_picture)
            self.save()
        if settings.DEBUG:
            return 'http://localhost:8000' + self.thumbnail.url
        return self.thumbnail.url

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=str(uuid4()) + '.jpg')

        return thumbnail
