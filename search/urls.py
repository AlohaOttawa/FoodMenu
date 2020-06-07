from django.urls import path, re_path

from .views import (
    SearchMenuView
    # menu_list_view,
    # MenuDetailView,
    # MenuDetailSlugView,
    # menu_detail_view,
    # MenuFeaturedListView,
    # MenuFeaturedDetailView
    )



urlpatterns = [
    path('', SearchMenuView.as_view(), name='query'),
]