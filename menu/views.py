from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import MenuItem

# Create your views here.

class MenuListView(ListView):
    queryset = MenuItem.objects.all()
    template_name = "menuitem/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(MenuListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return MenuItem.objects.all()


def menu_list_view(request):  #same as class view above but more complex
    queryset = MenuItem.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "menuitem/list.html", context)

class MenuDetailView(DetailView):
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