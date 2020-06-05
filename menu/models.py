import os
import random

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

# Create your models here.

from .utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 32323523)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "menuitems/{new_filename}/{final_filename}".format(
        new_filename = new_filename,
        final_filename = final_filename
        )


class MenuItemQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

class MenuItemManager(models.Manager):
    def get_queryset(self):
        return MenuItemQuerySet(self.model, using=self.db)

    def all(self):
        return self.get_queryset().active()

    def features(self):             # MenuItem.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)  # MenuItem.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None
 #      return self.get_queryset().filter(id = id)  # MenuItem.object equivalent


# generate slug before Menu Item is saved





class MenuItem(models.Model):   # Menu category
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)  # for url referencing purposes
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5, default=5.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = MenuItemManager()


    def get_absolute_url(self):
        # return "/menuitems/{slug}/".format(slug=self.slug)
        # above is same as below but now uses the logical shortcut vs hardcoded menuitems
        return reverse("menuitems:details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def menuitem_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(menuitem_pre_save_receiver, sender=MenuItem)