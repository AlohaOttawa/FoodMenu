from django.db import models

# Create your models here.

class MenuItem(models.Model):   # Menu category
    title       = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5, default=5.99)

    def __str__(self):
        return self.title