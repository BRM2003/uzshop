from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from claims.views import *
from claims.face_compare import main_script


def redirect_root_to_shop(request):
    return redirect('/shop')


urlpatterns = [
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('shop', include('goods.urls'), name='shop'),
    path('', redirect_root_to_shop),
    path('order/change/status', change_status),
    path('sqb_test/face_compare', main_script),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
