from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from menu.models import MenuItem
from orders.models import Order
from .models import Cart

# def cart_create(user=None):
#      cart_obj    =   Cart.objects.create(user=None)
#      print("New cart created")
#      return cart_obj




def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
            # receiver and signals in the model class is managing the below
            # menuitems = cart_obj.menuitems.all()
            # total = 0
            # for item in menuitems:
            #     total += item.price
            #     # print(total)
            #     # print("in cart home")
            # cart_obj.total = total
            # cart_obj.save()
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
        else:
            cart_obj.menuitems.add(menuitem_obj)

        request.session["cart_item_count"] = cart_obj.menuitems.count()

             #cart_obj.menuitems.add(item_Id)
            # to remove is cart_obj.menuitems.remove(menuitem_obj)
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
