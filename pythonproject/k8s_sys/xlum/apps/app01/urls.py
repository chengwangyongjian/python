"""xlum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
from django.contrib import admin

from app01.views import LoginView, LogoutView, CreateUserView, CreateNamespaceView, DeleteUserView, AddExtraNamespaceView, index,details

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^create_user/', CreateUserView.as_view(), name='create_user'),
    url(r'^create_namespace/', CreateNamespaceView.as_view(), name='create_namespace'),
    url(r'^extra_namespace/', AddExtraNamespaceView.as_view(), name='extra_namespace'),
    url(r'^index/(?P<zone>\w+)/', index, name='index'),
    url(r'^delete/(?P<group>\w+)/', DeleteUserView.as_view(), name='delete'),
    url(r'^details/(?P<zone>\w+)/(?P<selected_group>\w+)(?:/(?P<selected_namespace>.*))?', details, name='details'),
]
