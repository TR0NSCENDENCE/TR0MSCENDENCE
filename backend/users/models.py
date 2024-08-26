from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from .managers import UserManager
from io import BytesIO
from PIL import Image
from django.core.files import File
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)

    username_validator = UnicodeUsernameValidator()

    activation_uuid = models.UUIDField(unique=True, default=uuid4)

    username = models.CharField(
        _("username"),
        max_length=16,
        unique=True,
        help_text=_(
            "Required. 16 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    objects = UserManager()

    def __str__(self):
        return self.username

def get_default_pacman_data():
    return {}

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField(User, blank=True)
    online_status = models.BooleanField(default=False)
    profile_picture = models.ImageField(default='default.jpg', upload_to="profile_pictures/", blank=True)
    thumbnail = models.ImageField(upload_to='profile_pictures/thumbnail/', blank=True, null=True)
    pacman_data = models.JSONField(default=get_default_pacman_data)

    def __str__(self):
        return self.user.username

    def get_thumbnail(self):
        if not self.thumbnail and self.profile_picture:
            self.thumbnail = self.make_thumbnail(self.profile_picture)
            self.save()
        if settings.DEBUG:
            return 'http://localhost:8000' + self.thumbnail.url
        return self.thumbnail.url

    def make_thumbnail(self, image, size=(200, 200)):
        with Image.open(image) as img:
            img_width, img_height = img.size
            aspect_ratio_img = img_width / img_height
            aspect_ratio_target = size[0] / size[1]

            if aspect_ratio_img > aspect_ratio_target:
                new_width = int(img_height * aspect_ratio_target)
                new_height = img_height
                top = 0
                bottom = img_height
                left = (img_width - new_width) / 2
                right = (img_width + new_width) / 2
            else:
                new_width = img_width
                new_height = int(img_width / aspect_ratio_target)
                top = (img_height - new_height) / 2
                bottom = (img_height + new_height) / 2
                left = 0
                right = img_width

            img_resized = img.crop((left, top, right, bottom)).resize(size).convert('RGB')

            thumb_io = BytesIO()
            img_resized.save(thumb_io, 'JPEG', quality=85)

            thumbnail = File(thumb_io, name=str(uuid4()) + '.jpg')
            return thumbnail
