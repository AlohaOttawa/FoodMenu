from django.shortcuts import render, get_object_or_404
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


def menu_list_view(request):  #same as class view above but more complex
    queryset = MenuItem.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "menuitem/list.html", context)

class MenuDetailView(DetailView):
    queryset = MenuItem.objects.all()
    template_name = "menuitem/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MenuDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


def menu_detail_view(request, pk=None, *args, **kwargs):  #same as class view above but more complex
    # instance = MenuItem.objects.get(id=pk)
    instance = get_object_or_404(MenuItem, pk=pk)
    context = {
        "object": instance
    }
    return render(request, "menuitem/detail.html", context)