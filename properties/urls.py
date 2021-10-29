from django.urls import path
from django.conf.urls import url

from . import views

app_name = "users"
urlpatterns = [
	path('fetch_props/', views.UpdateProperties.as_view(), name='fetch_props'),
]