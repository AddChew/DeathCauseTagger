from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView

from tagger.views import RegisterView, LoginView

app_name = 'tagger'

urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name = 'register'),
    re_path(r'login/$', LoginView.as_view(), name = 'login'),
    re_path(r'token/refresh/$', TokenRefreshView.as_view(), name = 'token_refresh'),
]