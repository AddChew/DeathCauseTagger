from django.urls import re_path
from tagger.views import RegisterView

app_name = 'tagger'

urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view(), name = 'register')
]