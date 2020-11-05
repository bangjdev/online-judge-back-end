import os
from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.db import models

from online_judger_backend.settings import AVATAR_FOLDER


def get_time_stamp():
    time_obj = datetime.now()
    return time_obj.strftime("%Y-%m-%d_%H-%M-%S")


def get_file_path(instance, filename):
    upload_to = os.path.join(AVATAR_FOLDER)
    extension = os.path.splitext(filename)[1]
    filename = get_time_stamp() + "_" + instance.user.username
    final_filename = '{}{}'.format(filename, extension)

    return os.path.join(upload_to, final_filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username")
    avatar = models.ImageField(default='avatars/default.jpg', upload_to=get_file_path)

    def __str__(self):
        return "User profile: " + self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if (img.height > 500) or (img.width > 500):
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
