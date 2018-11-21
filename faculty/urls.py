from django.conf.urls import url, include
from feedback import views


urlpatterns = [
	url(r'^$', views.index),
]
