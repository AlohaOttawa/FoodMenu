# moved to model manager -> from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from menu.models import MenuItem

# Create your views here.

class SearchMenuView(ListView):
    # queryset = MenuItem.objects.all()
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchMenuView, self).get_context_data(*args, **kwargs)

            # original for below   context['query'] = self.request.GET.get('q')
        query = self.request.GET.get('q')
        context['query'] = query
            # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)  # method dictionary to obtain ['q'] search otherwise return None

        if query is not None:
            # not needed.  Updated model and return -> lookups = Q(title__icontains=query) | Q(description__contains=query)
            # updated models -> return MenuItem.objects.filter(lookups).distinct()
            return MenuItem.objects.search(query)
        return MenuItem.objects.features()


    '''
    icontains = contains it and case insensitive
    iexact = has to be exact match, case insensitive
    
    '''