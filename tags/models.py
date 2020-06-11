from django.db import models
from django.db.models.signals import pre_save

from DJ2.utils import unique_slug_generator
from menu.models import MenuItem

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    menuitem = models.ManyToManyField(MenuItem, blank=True)

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)