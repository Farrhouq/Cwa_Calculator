"""base_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from tkinter import N
from django.contrib import admin
from django.urls import path, include
from base.views import delete_all, final,  inter,  home, logoutUser, new, refresh, register,  to_randomize, tr2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home' ),
    path('two', to_randomize, name='two'),
    path('three', to_randomize, name='three'),
    path('inter', inter, name='inter'),
    path('tr2', tr2, name='tr2'),
    path('new', new, name='new'),
    path('final', final, name='final'),
    path('', include('django.contrib.auth.urls')),
    path('register', register, name='register'),
    path('logout2', logoutUser, name='logout2'),
    path('refresh', refresh, name='refresh'),
    path('delete_all', delete_all, name='delete_all'),
]
