from django.conf.urls import url

from .views import fake_view

urlpatterns = [url(r'^testurl/$', fake_view, name='testurl')]
