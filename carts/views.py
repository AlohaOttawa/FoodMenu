from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
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

            # user = request.user  ... not needed in the model view manager now
            # billing_profile = None ... not needed managed in model view manager now
    login_form = LoginForm()
    guest_form = GuestForm()

    # Call the model manager vs the moved function below it
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    # move the below to the Billing model manager
            # guest_email_id = request.session.get("guest_email_id")
            #
            # if user.is_authenticated:
            #     # This is a logged in user and recalls payment info
            #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            #         user=user,
            #         email=user.email
            #     )
            # elif guest_email_id is not None:
            #     # This uses an email no user is logged in. auto reload payment info
            #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            #     billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
            #          email=guest_email_obj.email
            #     )
            # else:
            #     pass


    if billing_profile is not None:

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)


                # order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
                # if order_qs.count() == 1:
                #     order_obj = order_qs.first()
                # else:
                #         # move this code to the orders.model pre_save create_order_id
                #         # deactivate all old orders with the same cart
                #         # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
                #         # if old_order_qs.exists():
                #         #     old_order_qs.update(active=False)
                #     order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)



    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }

    return render(request, "carts/checkout.html", context)
    # return render(request, "carts/checkout.html", {"object": order_obj})