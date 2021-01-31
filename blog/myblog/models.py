from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField("Название", max_length=200)
    url = models.SlugField(max_length=160, unique=True)
    description = RichTextUploadingField("Описание")
    content = RichTextUploadingField("Статья")
    image = models.ImageField("Изображение")
    date_create = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
