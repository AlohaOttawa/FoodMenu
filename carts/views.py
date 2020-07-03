from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from menu.models import MenuItem
from orders.models import Order
from .models import Cart


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # menuitems = cart_obj.menuitems.all()  # queryset / list of items [<object>, <object>]
    menuitems = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.name,
        "price": x.price
        }
        for x in cart_obj.menuitems.all()] # serialize the data

    cart_data = {"menuitems": menuitems, "subtotal": cart_obj.subtotal, "total":cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    # test print(request.POST)
    item_id = request.POST.get("menuitem_id")
    if item_id is not None:
        try:
            menuitem_obj = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            print("Menu Item is gone")
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if menuitem_obj in cart_obj.menuitems.all():
            cart_obj.menuitems.remove(menuitem_obj)
            added = False
        else:
            cart_obj.menuitems.add(menuitem_obj)
            added = True

        request.session["cart_item_count"] = cart_obj.menuitems.count()

        # async javascript and JSON
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.menuitems.count(),
            }
            return JsonResponse(json_data, status=200)  # HTTP Response 400 is error
            # return JsonResponse({"message": "Error something happened"}, status=400)
    return redirect("cart:home")





def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.menuitems.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    # Call the model manager vs the moved function below it
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    # reset addresses for user to pick from
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session["cart_item_count"] = 0
            del request.session["cart_id"]
        return redirect("cart:success")


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }

    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
