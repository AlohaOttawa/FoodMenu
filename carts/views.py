from django.shortcuts import render, redirect
from menu.models import MenuItem
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

    # return redirect(menuitem_obj.get_absolute_url())  -> original test to see if it works


    # request.session["cart_id"] = "12"
            # cart_id = request.session.get("cart_id", None)
            # qs = Cart.objects.filter(id=cart_id)
            # if qs.count() == 1:
            #     print("Cart ID exists")
            #     cart_obj = qs.first()
            #     if request.user.is_authenticated and cart_obj.user is None:
            #         cart_obj.user = request.user
            #         cart_obj.save()
            # else:
            #     cart_obj = Cart.objects.new(user=request.user)
            #     request.session["cart_id"] = cart_obj.id


    # print(dir(request.session))
    # cart_id = request.session.get("cart_id", None)
    # print(request.session['cart_id'])

    #  if cart_id is None:   # and isinstance(cart_id, int)   user later
    #     print("create new cart")
    #    request.session['cart_id'] = 12  # Sets the value
          # pass
    #  else:
    #    print("Cart ID exists")
    #    print(cart_id)

                # print(request.session)  # on the request
                # print(dir(request.session))
                # request.session.set_expiry(300)  # exctly 5 mins
                # key = request.session.session_key
                # print(key)

                # request.session["user"] = request.user.username
    # return render(request, "carts/home.html", {})
