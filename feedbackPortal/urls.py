"""feedbackPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the () fincludeunction: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from . import settings
from django.conf.urls.static import static


import feedback.urls, faculty.urls

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$',LogoutView.as_view(), {'next_page': '/login/'}),
    url(r'^faculty/', include(faculty.urls)),
    url(r'^', include(feedback.urls)),
    url(r'^admin/', admin.site.urls),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
