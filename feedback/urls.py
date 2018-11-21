from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^feedback', views.user_feedback),
	url(r'^$', views.index),
]
