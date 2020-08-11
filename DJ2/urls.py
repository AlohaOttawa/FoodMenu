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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from .views import home_page, about_page, contact_page
from billing.views import payment_method_view, payment_method_createview
from marketing.views import MarketingPreferenceUpdateView

        # from carts.views import cart_home, cart_update

        # from menu.views import (
        #     MenuListView,
        #     menu_list_view,
        #     MenuDetailView,
        #     MenuDetailSlugView,
        #     menu_detail_view,
        #     MenuFeaturedListView,
        #     MenuFeaturedDetailView
        #     )




# app_name = 'menu'

urlpatterns = [
    path('bootstrap/', TemplateView.as_view(template_name="bootstrap/bootexample.html")),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('register/guest/', guest_register_view, name='guest_register'),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('cart/', include(("carts.urls", 'cart'))),
        # path('cart/', cart_home, name='cart'),
        # path('cart/update', cart_update, name='update'),
    path('register/', RegisterView.as_view(), name='register'),
    path('menuitems/', include(("menu.urls", 'menuitems'))),
    path('search/', include(("search.urls", 'search'))),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    # path('menuitems/', MenuListView.as_view()),
    # path('featured/', MenuFeaturedListView.as_view()),
    # re_path('featured/(?P<pk>\d+)/$', MenuFeaturedDetailView.as_view(), name='details'),
    # path('menuitems-fbv/', menu_list_view),
    # # re_path(r'^menuitems/(?P<pk>\d+)/$', MenuDetailView.as_view(), name='details'),
    # re_path(r'^menuitems/(?P<slug>[\w-]+)/$', MenuDetailSlugView.as_view(), name='details'),
    # re_path(r'^menuitems-fbv/(?P<pk>\d+)/$', menu_detail_view, name='details'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)