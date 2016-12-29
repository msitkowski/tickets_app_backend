# -*- coding: utf-8 -*-
"""Tickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import views
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register(r'ticket', views.TicketViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'usertickets', views.UserTicketsViewSet)
router.register(r'account', views.AccountViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', auth_views.obtain_auth_token),
    url(r'^', include(router.urls))
]
