from django.urls import path, re_path

from .views import (
    MenuListView,
    # menu_list_view,
    MenuDetailView,
    MenuDetailSlugView,
    # menu_detail_view,
    # MenuFeaturedListView,
    # MenuFeaturedDetailView
    )



urlpatterns = [
    path('', MenuListView.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/$', MenuDetailSlugView.as_view(), name='details'),
]
