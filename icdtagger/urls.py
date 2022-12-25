"""icdtagger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path, include


VERSION_PREFIX = 'v1/api'

v1_urlpatterns = [
    re_path(f'^auth/', include(("authentication.urls", "authentication"), namespace = 'auth')),
    re_path(f'^tagger/', include(("tagger.urls", "tagger"), namespace = 'tagger')),
]

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path(fr'^{VERSION_PREFIX}/', include((v1_urlpatterns, 'v1'), namespace = 'v1'))
]
