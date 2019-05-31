# -*- coding: utf-8 -*-
from django.conf import settings


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='fake_app.urls',
        MIDDLEWARE=['header_filter.HeaderFilterMiddleware'],
    )
