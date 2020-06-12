from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

# bring in the user
User = settings.AUTH_USER_MODEL

# an email account like something@gmail.com can have a million profiles
# but the user should have only 1 profile so active will be used to deactivate
# the excess profiles whenever anonymous / email user converts to authenticated user

# Create your models here.

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # tbd Customer_ID in Stripe or some other 3rd party payment processor

    def __str__(self):
        return self.email

# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("ACTUAL API REQUEST Send to Stripe or some other payment processor")
#         instance.customer_id = newID
#         instance.save()


# when user is Created, use the signal below to create the billing profile automatically
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)
