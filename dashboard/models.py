from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from sorl.thumbnail import ImageField

from dashboard.tasks import get_image_labels


class TimestampModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Picture(TimestampModel):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    image = ImageField(upload_to="images/%Y/%m/")
    user = models.ForeignKey(User, related_name='pictures', null=True, blank=True)
    task_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify("{}-{}".format(self.name, self.id))

        if not self.task_enabled:
            get_image_labels.delay(self.id)
            self.task_enabled = True
            self.save()


class Label(TimestampModel):
    picture = models.ForeignKey(Picture, related_name='labels')
    name = models.CharField(max_length=255)
    score = models.FloatField()


class Landmarks(TimestampModel):
    picture = models.ForeignKey(Picture, related_name='landmarks')
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()


