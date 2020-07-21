from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
# from django.core.urlresolvers import reverse
from django.urls import reverse

from accounts.models import GuestEmail

# bring in the user
User = settings.AUTH_USER_MODEL

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
import stripe
stripe.api_key = "sk_test_C8dhHUK0Q9ByFzNOuQ10QHyi00tS0LViDj"

# an email account like something@gmail.com can have a million profiles
# but the user should have only 1 profile so active will be used to deactivate
# the excess profiles whenever anonymous / email user converts to authenticated user

# Create your models here.

class BillingProfileManager(models.Manager):
        def new_or_get(self, request):
            user = request.user

            guest_email_id = request.session.get("guest_email_id")

            # created = False and obj=none is for model not from view
            created = False
            obj = None
            if user.is_authenticated:
                # This is a logged in user and recalls payment info
                # obj, created = BillingProfile.objects.get_or_create( --- from view use model code below
                obj, created = self.model.objects.get_or_create(
                    user=user,
                    email=user.email
                )
            elif guest_email_id is not None:
                # This uses an email no user is logged in. auto reload payment info
                guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
                obj, created = self.model.objects.get_or_create(
                    email=guest_email_obj.email
                )
            else:
                pass
            return obj, created

class BillingProfile(models.Model):
    user            = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    email           = models.EmailField()
    active          = models.BooleanField(default=True)
    update          = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    stripe_cust_id  = models.CharField(max_length=120, null=True, blank=True)
        # Stripe Customer_ID in Stripe or some other 3rd party payment processor

    # bring the new functions above to be referenceable for the class
    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do_charge(self, order_obj, card)

    def get_cards(self):    # OOP add filter property all below in card manager
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse("billing-payment-method")

    @property
    def has_card(self):     # instance.has_card
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

        # inactivate the cards so that user is required to enter
        # so the card nbr is not reused for next guest user
    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.stripe_cust_id and instance.email:
        print("ACTUAL API REQUEST Send to Stripe or some other payment processor")
        # call Stripe API to return Stripe customer id based on CRV19 email
        customer = stripe.Customer.create(
            email = instance.email
        )
        print(customer)
        # customer.id or customer.stripe_id ??
        instance.stripe_cust_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


# when user is Created, use the signal below to create the billing profile automatically
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)

class CardManager(models.Manager):
        # Overide to include only active = True.  Don't pull in inactive cards
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

        # def add_new(self, billing_profile, stripe_card_response):
    def add_new(self, billing_profile, token):
            # use the if-token to handle in the class.  Previous was managed via view args
            # if str(stripe_card_response.object) == "card":
        if token:
            stripe_card_response = stripe.Customer.create_source(
                billing_profile.stripe_cust_id,
                source=token,
            )
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_cust_id=stripe_card_response.id,
                brand=stripe_card_response.brand,
                country=stripe_card_response.country,
                exp_month=stripe_card_response.exp_month,
                exp_year=stripe_card_response.exp_year,
                last4=stripe_card_response.last4
            )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_cust_id      = models.CharField(max_length=120, null=True, blank=True)
    brand               = models.CharField(max_length=120, null=True, blank=True)
    country             = models.CharField(max_length=120, null=True, blank=True)
    exp_month           = models.IntegerField(null=True, blank=True)
    exp_year            = models.IntegerField(null=True, blank=True)
    last4               = models.CharField(max_length=4, null=True, blank=True)
    default             = models.BooleanField(default=True)
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)

def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)

post_save.connect(new_card_post_save_receiver, sender=Card)

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
# stripe.Charge.create(
#   amount=2000,
#   currency="cad",
#   source="tok_visa",
#   description="My First Test Charge (created for API docs)",
# )


class ChargeManager(models.Manager):
    def do_charge(self, billing_profile, order_obj, card=None):    # Charge.objects.do_charge()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"

        created_charge = stripe.Charge.create(
            amount      = int(order_obj.total * 100),    # need to multiply to remove decimal places on stripe side
            currency    = "usd",
            customer    = billing_profile.stripe_cust_id,
            source      = card_obj.stripe_cust_id,
            metadata    = {"order_id": order_obj.order_id},
        )
        new_charge_obj = self.model(
            billing_profile = billing_profile,
            stripe_cust_id  = created_charge.id,
            paid            = created_charge.paid,
            refunded        = created_charge.refunded,
            outcome         = created_charge.outcome,
            outcome_type    = created_charge.outcome["type"],
            seller_message  = created_charge.outcome["seller_message"],
            risk_level      = created_charge.outcome["risk_level"],
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message

class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_cust_id  = models.CharField(max_length=120, null=True, blank=True)
    paid            = models.BooleanField(default=False)
    refunded        = models.BooleanField(default=False)
    outcome         = models.TextField(null=True, blank=True)
    outcome_type    = models.CharField(max_length=120, null=True, blank=True)
    seller_message  = models.CharField(max_length=120, null=True, blank=True)
    risk_level      = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()



