import os
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.username, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(instance.username, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("avatars")

# def path_and_rename(path):
#     def wrapper(instance, filename):
#         ext = filename.split('.')[-1]
#         # get filename
#         if instance.pk:
#             filename = '{}.{}'.format(instance.username, ext)
#         else:
#             # set filename as random string
#             filename = '{}.{}'.format(instance.username, ext)
#         # return the whole path to the file
#         return os.path.join(path, filename)
#     return wrapper


class Document(models.Model):
    username = models.CharField(max_length=128, default='')
    docfile = models.FileField(upload_to=path_and_rename,
                               null=True, blank=True,
                               default="avatars/default.png")
