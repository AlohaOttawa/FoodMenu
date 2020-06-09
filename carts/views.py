from django.shortcuts import render
from .models import Cart

# def cart_create(user=None):
#      cart_obj    =   Cart.objects.create(user=None)
#      print("New cart created")
#      return cart_obj




def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)


    return render(request, "carts/home.html", {})
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
