from django.db import models
from django.db.models.signals import pre_save

from carts.models import Cart
from DJ2.utils import unique_order_id_generator

# Create your models here

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class Order(models.Model):
    order_id        = models.CharField(max_length=50, blank=True)
    # billing profile
    # shipping address
    # billing address
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=50, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total           = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

# generate Order ID
# generate the order total => Use SIGNAL