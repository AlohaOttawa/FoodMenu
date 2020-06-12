from django.shortcuts import render, redirect
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
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "carts/checkout.html", {"object": order_obj})