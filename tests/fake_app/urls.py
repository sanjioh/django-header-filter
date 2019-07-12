from django.conf.urls import url

from .views import DecoratorTestCBV, decorator_test_fbv, middleware_test_fbv

urlpatterns = [
    url(r'^middleware-fbv/$', middleware_test_fbv, name='middleware-fbv'),
    url(r'^decorator-fbv/$', decorator_test_fbv, name='decorator-fbv'),
    url(r'^decorator-cbv/$', DecoratorTestCBV.as_view(), name='decorator-cbv'),
]
