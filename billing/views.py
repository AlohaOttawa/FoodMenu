from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url

# Create your views here.
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_C8dhHUK0Q9ByFzNOuQ10QHyi00tS0LViDj")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_W9demQ8ttDK68G9qs3kb3z3i00kMEeETKZ")

stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, Card

def payment_method_view(request):
    # template view with context.  Use the new one below for now for handlnig POST
    # use the one below for returning JSON now (to make it work)
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

         # Call the model manager
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if not billing_profile:
        return redirect("/cart")

    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, "billing/payment-method.html", {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        # same as above for ajax.  Called regardless of where its called from
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if not billing_profile:
            return HttpResponse({"message": "Cannot find user"}, status_code=401)

        token = request.POST.get("token")

        if token is not None:
                # stripe_card_response = stripe.Customer.create_source(
                #     billing_profile.stripe_cust_id,
                #     source=token,
                # )
                # move the below (and token) into the class rather than managing it in the view
                # new_stripe_card = Card.objects.add_new(billing_profile, stripe_card_response)

            new_stripe_card = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Card was added"})
    raise HttpResponse("error", status_code=401)

