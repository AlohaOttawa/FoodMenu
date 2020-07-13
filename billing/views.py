from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url

# Create your views here.
import stripe
stripe.api_key = "sk_test_C8dhHUK0Q9ByFzNOuQ10QHyi00tS0LViDj"
STRIPE_PUB_KEY = "pk_test_W9demQ8ttDK68G9qs3kb3z3i00kMEeETKZ"

def payment_method_view(request):
    # template view with context.  Use the new one below for now for handlnig POST
    # use the one below for returning JSON now (to make it work)
    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, "billing/payment-method.html", {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Card was added"})
    raise HttpResponse("error", status_code=401)

