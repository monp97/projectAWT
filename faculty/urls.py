from django.conf.urls import url, include
from faculty import views


urlpatterns = [
	url(r'^$', views.index),
]
