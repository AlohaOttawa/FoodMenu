from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView

from carts.models import Cart

# from analytics.signals import object_viewed_signal

from analytics.mixins import ObjectViewedMixin


from .models import MenuItem

# Create your views here.

class MenuFeaturedListView(ListView):
    template_name = "menuitem/list.html"

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return MenuItem.objects.features()



class MenuFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = MenuItem.objects.features()
    template_name = "menuitem/featured-detail.html"

    # def get_queryset(self, *args, **kwargs ):
    #     request = self.request
    #     return MenuItem.objects.featured()





class MenuListView(ListView):
    queryset = MenuItem.objects.all()
    template_name = "menuitem/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(MenuListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(MenuListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return MenuItem.objects.all()


def menu_list_view(request):  #same as class view above but more complex
    queryset = MenuItem.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "menuitem/list.html", context)



class MenuDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = MenuItem.objects.all()
    template_name = "menuitem/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MenuDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")

        # instance = get_object_or_404(MenuItem, slug=slug, active=True)

        try:
            instance = MenuItem.objects.get(slug=slug, active=True)
        except MenuItem.DoesNotExist:
            raise Http404("Not found ...")
        except MenuItem.MultipleObjectsReturned:
            qs = MenuItem.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("some other error")

        # analytics.py.  Send the class when sending the signal
        # sender of the view as class, instance, and request
        # function based views need to do this for every function
        # but mixins allow to bypass using a class definition only once
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request )

        return instance


class MenuDetailView(ObjectViewedMixin, DetailView):
    # queryset = MenuItem.objects.all()
    template_name = "menuitem/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MenuDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        pk = self.kwargs.get('pk')
        return MenuItem.objects.filter(pk = pk)

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")
        instance = MenuItem.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Menu Item does NOT exist!")
        return instance


def menu_detail_view(request, pk=None, *args, **kwargs):  #same as class view above but more complex
    # instance = MenuItem.objects.get(id=pk)
    # instance = get_object_or_404(MenuItem, pk=pk)
    # try:
    #     instance = MenuItem.objects.get(id=pk)
    # except MenuItem.DoesNotExist:
    #     print("item does not exist")
    #     raise Http404("Menu Item does NOT exist!")
    # except:
    #     print("Some other problem")


    instance = MenuItem.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Menu Item does NOT exist!")


    # qs = MenuItem.objects.filter(id=pk)
    # print(qs)
    # print(instance)
    #
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Menu item does NOT exists!")

    context = {
        "object": instance
    }
    return render(request, "menuitem/detail.html", context)