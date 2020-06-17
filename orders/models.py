import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from billing.models import BillingProfile

from carts.models import Cart
from DJ2.utils import unique_order_id_generator

# Create your models here

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


# moved from carts.view to custom model manager here
class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile,
                cart=cart_obj,
                active=True
            )
        # below is view based coding.  Above is model based coding
        # qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)

        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile,
                    cart=cart_obj
                )
            created = True
         #b below is view based coding from the cart.view  Above is the model coding
         # obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    order_id        = models.CharField(max_length=50, blank=True)
    # billing profile
    # shipping address
    # billing address
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=50, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=5.99, max_digits=10, decimal_places=2)
    total           = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    active          = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    # bring the object above into the Order class
    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        display_format_total = format(new_total, ".2f")
        self.total = display_format_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id = cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("Running")
    if created:
        print("updating for the first time")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)


# generate Order ID
# generate the order total => Use SIGNAL