"""DJ2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path

from menu.views import MenuListView, menu_list_view, MenuDetailView, menu_detail_view


from .views import home_page, about_page, contact_page, login_page, register_page


urlpatterns = [
    path('', home_page),
    path('about/', about_page),
    path('contact/', contact_page),
    path('login/', login_page),
    path('register/', register_page),
    path('menuitems/', MenuListView.as_view()),
    path('menuitems-fbv/', menu_list_view),
    # path('menuitems/(?P<pk>\d+)/', MenuDetailView.as_view()),
    # path('menuitems-fbv/(?P<pk>\d+)/', menu_detail_view),
    # path('', MenuListView.as_view(), name='menuitems'),
    re_path(r'^menuitems/(?P<pk>\d+)/$', MenuDetailView.as_view(), name='details'),
    re_path(r'^menuitems-fbv/(?P<pk>\d+)/$', menu_detail_view, name='details'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)