"""
URL configuration for django_gunicorn_gevent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from django_gunicorn_gevent.apps.core import views

urlpatterns = [
    path("only-http-call/", views.view_http_call, name="view-http-call"),
    path("only-http-do-ten_calls_with_gevent/", views.view_do_ten_http_calls_with_gevent, name="view-http-call-10-g"),
    path("only-database-call/", views.view_database_call, name="view-database-call"),
    path("both-http-and-database-calls/", views.view_http_and_database_calls, name="view-http-and-database-calls"),
]
